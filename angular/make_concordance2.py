#!/usr/bin/env/python
"""
    make_concordance2.py -- Examine concepts, people and papers from VIVO,
    build all combinations of occurances as a python shelf.

    make_concordnace2 is intended to be run as a batch process to run daily as
    data availalable to the expert finder

    Version 0.0 MC 2014-03-18
    --  Started at the VIVO 14 Hackathon.  Just a frame for now

    To Do
    --  Add counts to the ocurrances of papers and people in concepts and
        concept pairs
    --  Scale testing

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
import vivotools as vt
import os
import sys
import shelve
import json

from datetime import datetime

def make_conc(conc, debug=False):
    """
    Extract all the concepts in VIVO and organize them into a dictionary
    keyed by concept uri.  Data for the concept includes the concet name and
    all concepts co-occuring withthe concept and the count of the co-occurances
    """

    query = """
    SELECT ?uri ?name
    WHERE {
        ?uri a bibo:AcademicArticle .
        ?uri rdfs:label ?name .
    }
    LIMIT 1000"""
    result = vivo_sparql_query(query)

    if 'results' in result and 'bindings' in result['results']:
        rows = result["results"]["bindings"]
    else:
        return conc
    if debug:
        print query
        if len(rows) >= 2:
            print rows[0], rows[1]
        elif len(rows) == 1:
            print rows[0]

    i = 0
    for row in rows:
        name = row['name']['value']
        pub_uri = str(row['uri']['value'])
        publication = get_publication(pub_uri, get_authors = True)
        curis = []
        for curi in publication['concept_uris']:
            curis.append(str(curi))
        auris = []
        for auri in publication['author_uris']:
            auris.append(str(auri))
        for curi1 in curis:
            cname1 = get_vivo_value(curi1,'rdfs:label')
            if curi1 not in conc:
                entry = {'name' : cname1,
                    'people' : auris,
                    'pubs' : [pub_uri],
                    'concepts' : {}}
            else:
                entry = conc[curi1]
                print "Add to concept"
                if pub_uri not in entry['pubs']:
                    entry['pubs'].append(pub_uri)
                for auri in auris:
                    if auri not in entry['people']:
                        entry['people'].append(auri)
            for curi2 in curis:
                cname2 = get_vivo_value(curi2,'rdfs:label')
                if curi1 != curi2:
                    if curi2 not in entry['concepts']:
                        entry['concepts'][curi2]= {'name': cname2,
                         'pubs':[pub_uri],
                         'people':auris}
                    else:
                        print "Augment"
                        if pub_uri not in entry['concepts'][curi2]['pubs']:
                           entry['concepts'][curi2]['pubs'].append(pub_uri)
                        for auri in auris:
                           if auri not in entry['concepts'][curi2]['people']:
                               entry['concepts'][curi2]['people'].append(auri)
            conc[curi1] = entry
        i = i + 1
        print i
        if i > 100:
            break
    return conc

log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
conc = shelve.open("conc2", writeback=True)
print >>log_file, datetime.now(), "VIVO Tools version", vt.__version__
conc = make_conc(conc, debug=True)
for key,stuff in conc.items():
    print >>log_file, datetime.now(), key
    print >>log_file, datetime.now(), json.dumps(stuff, indent = 4)
print >>log_file, datetime.now(), "conc has ", len(conc)," concepts"
conc.close()
print >>log_file, datetime.now(), "Finish"
