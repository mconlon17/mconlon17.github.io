#!/usr/bin/env/python
"""
    make_concordance.py -- Examine concepts, people and apers from VIVO,
    build all combinations of occurances as a python shelf.

    make_concordnace2 is intended to be run as a batch process to run daily as
    data availalable to the expert finder

    Version 0.0 MC 2014-03-18
    --  Started at the VIVO 14 Hackathon.  Just a frame for now

    To Do
    --  Everything

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.0"

from vivotools import vivo_sparql_query
from vivotools import get_vivo_uri
from vivotools import assert_resource_property
from vivotools import assert_data_property
from vivotools import update_data_property
from vivotools import get_vivo_value
from vivotools import get_triples
from vivotools import get_publication
import os
import sys
import shelve
import json

from datetime import datetime

def make_concordance(debug=False):
    """
    Extract all the concets in VIVO and organize them into a dictionary
    keyed by concept uri.  Data for the concept includes the concet name and
    all concepts co-occuring withthe concept and the count of the co-occurances
    """
    query = """
    SELECT ?uri ?name
    WHERE {
        ?uri a bibo:AcademicArticle .
        ?uri rdfs:label ?name .
    }"""
    result = vivo_sparql_query(query)

    if 'results' in result and 'bindings' in result['results']:
        rows = result["results"]["bindings"]
    else:
        return concordance
    if debug:
        print query
        if len(rows) >= 2:
            print rows[0],rows[1]
        elif len(rows) == 1:
            print rows[0]
    concordance = shelve.open("concordance2")
    i = 0
    for row in rows:
        name = row['name']['value']
        uri = str(row['uri']['value'])
        publication = get_publication(uri)
        concordance[uri] = {'name':name,'concept_uris': publication['concept_uris']}
        i = i + 1
        print i
        if i > 10:
            break
    if debug:
        print concordance.items()[1:3]
    return concordance

log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
concordance = make_concordance(debug=True)
for key,stuff in concordance.items():
    print key
    print json.dumps(stuff, indent = 4)
print "Concordance has ", len(concordance)," concepts"
print >>log_file, datetime.now(), "Finish"
