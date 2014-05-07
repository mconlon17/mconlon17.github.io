#!/usr/bin/env/python
"""
    concepts.py -- Examine concepts, and build a concordance for
    expert finding

    Version 0.0 MC 2014-05-07
    --  Just getting started

    To Do
    --  Add an out loop for processing all concepts

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.0"

import os
import sys
import shelve
import json
from vivotools import get_vivo_value
from vivotools import vivo_sparql_query

from datetime import datetime

def update_conc(conc, concept_uri, debug=False):
    """
    for a concept, update the entry in the concordance for the concept
    or create a new entry if one does not exist.
    """
    if concept_uri in conc:
        entry = conc[concept_uri]
    else:
        entry = {'name' : get_vivo_value(concept_uri,'rdfs:label'),
                 'concepts' : {},
                 'authors': {}}

    #   First we get the concordant concepts

    query = """
    #
    #   For a specified concept, find all the concepts that co-occur with the
    #   specified concept in one or more academic articles.  For each
    #   co-occuring concept, return the name, uri and count of papers in which
    #   the concept and the specified concept co-occur
    #
    SELECT ?concept_uri (MIN(DISTINCT ?xconcept_name) AS ?concept_name)
        (COUNT(DISTINCT ?pub_uri) AS ?count)
    WHERE {
        ?pub_uri vivo:hasSubjectArea
            <http://vivo.ufl.edu/individual/n9272944689> .
        ?pub_uri a bibo:AcademicArticle .
        ?pub_uri vivo:hasSubjectArea ?concept_uri .
        ?concept_uri rdfs:label ?xconcept_name .
        FILTER(str(?concept_uri) !=
            "http://vivo.ufl.edu/individual/n9272944689")
    }
    GROUP BY ?concept_uri
    ORDER BY DESC(?count)
    """
    result = vivo_sparql_query(query)
    if 'results' in result and 'bindings' in result['results']:
        rows = result['results']['bindings']
        print len(rows)

        # Replace concept content with current content

        concept_dict = {}
        for row in rows:
            concept_name = row['concept_name']['value']
            concept_dict[concept_name] = {'concept_uri':
                                          row['concept_uri']['value'],
                                          'count':
                                          row['count']['value']}
        entry['concepts'] = concept_dict
          
    #   Second we get the concordant authors
    
    conc[concept_uri] = entry
    return conc

log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
conc = shelve.open("conc", writeback=True)
conc = update_conc(conc, "http://vivo.ufl.edu/individual/n9272944689",
                   debug=True)
print >>log_file, datetime.now(), "conc has ", len(conc)," concepts"
entry = conc["http://vivo.ufl.edu/individual/n9272944689"]
print json.dumps(entry, indent=4)
conc.close()
print >>log_file, datetime.now(), "Finish"
