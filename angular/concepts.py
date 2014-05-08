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

def update_conc(conc, concept, debug=False):
    """
    for a concept, update the entry in the concordance for the concept
    or create a new entry if one does not exist.
    """
    concept_uri = str(concept['uri']['value'])
    concept_name = concept['concept_name']['value']
    npubs = concept['npub']['value']
    if concept_uri in conc:
        entry = conc[concept_uri]
    else:
        entry = {'name' : concept_name,
                 'npubs' : npubs,
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
        ?pub_uri vivo:hasSubjectArea <{uri}> .
        ?pub_uri a bibo:AcademicArticle .
        ?pub_uri vivo:hasSubjectArea ?concept_uri .
        ?concept_uri rdfs:label ?xconcept_name .
        FILTER(str(?concept_uri) !=
            "{uri}")
    }
    GROUP BY ?concept_uri
    ORDER BY DESC(?count)
    """
    query = query.replace("{uri}", concept_uri)
    result = vivo_sparql_query(query)
    if 'results' in result and 'bindings' in result['results']:
        rows = result['results']['bindings']
        print 'concept',len(rows)

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

        query = """
    #
    #   For a specified concept, find all the current UF authors that co-occur with the
    #   specified concept in one or more academic articles.  For each
    #   co-occuring author, return the name, uri and count of papers in which
    #   the author and the specified concept co-occur
    #
    SELECT ?author_uri (MIN(DISTINCT ?xauthor_name) AS ?author_name)
        (COUNT(DISTINCT ?pub_uri) AS ?count)
    WHERE {
        ?pub_uri vivo:hasSubjectArea <{uri}> .
        ?pub_uri a bibo:AcademicArticle .
        ?pub_uri vivo:informationResourceInAuthorship ?a .
        ?a vivo:linkedAuthor ?author_uri .
        ?author_uri a ufVivo:UFCurrentEntity .
        ?author_uri rdfs:label ?xauthor_name .
    }
    GROUP BY ?author_uri
    ORDER BY DESC(?count)
    """
    query = query.replace("{uri}", concept_uri)
    result = vivo_sparql_query(query)
    if 'results' in result and 'bindings' in result['results']:
        rows = result['results']['bindings']
        print 'author',len(rows)

        # Replace concept content with current content

        author_dict = {}
        for row in rows:
            author_name = row['author_name']['value']
            author_dict[author_name] = {'author_uri':
                                          row['author_uri']['value'],
                                          'count':
                                          row['count']['value']}
        entry['authors'] = author_dict
       
 
    conc[concept_uri] = entry
    return conc

log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
concepts = json.load(open("concepts.json"))["results"]["bindings"]
conc = shelve.open("conc", writeback=True)
i = 0
for concept in concepts:
    i = i +1
    if i < 501:
        continue
    print i, concept['concept_name']['value']
    conc = update_conc(conc, concept, debug=True)
    if i >= 510:
        break
print >>log_file, datetime.now(), "conc has", len(conc),"concepts"
keys = conc.keys()
entry = conc[keys[4]]
print keys[4]
print json.dumps(entry, indent=4)
conc.close()
print >>log_file, datetime.now(), "Finish"
