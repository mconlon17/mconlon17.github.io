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

def make_conc(conc, data, debug=False):
    """
    Given concordance, conc, and a json data structure, data, return an
    updated concordance.

    The json object is a list of co-occurrences of paper, concept and author.
    For each co-occurrence, the json object has the uri and label of the paper,
    concept and author.  Sample list item:

    {
    "pub": { "type": "uri" , "value":
        "http://vivo.ufl.edu/individual/n1003284293" } ,
    "pub_name": { "type": "literal" , "value":
        "Influence of Sea Level Rise On Iron Diagenesis in An East ..." } ,
    "concept": { "type": "uri" , "value":
        "http://vivo.ufl.edu/individual/n7781020701" } ,
    "concept_name": { "type": "literal" , "value": "Chemokine CCL2" } ,
    "author": { "type": "uri" , "value":
        "http://vivo.ufl.edu/individual/n2422490614" } ,
    "author_name": { "type": "literal" , "value": "Smith, Christopher G." }
    }
    """

    i = 0
    pubs = {}
    authors = {}
    for item in data:
        pub_uri = str(item['pub']['value'])
        pub_name = item['pub_name']['value']
        concept_uri = str(item['concept']['value'])
        concept_name = item['concept_name']['value']
        author_uri = str(item['author']['value'])
        author_name = item['author_name']['value']
        
        if pub_uri not in pubs:
            pubs[pub_uri] = {'pub_name': pub_name,
                'author_uris' : [author_uri],
                'concept_uris' : [concept_uri]}
        if concept_uri not in pubs[pub_uri]['concept_uris']:
            pubs[pub_uri]['concept_uris'].append(concept_uri)
        if author_uri not in pubs[pub_uri]['author_uris']:
            pubs[pub_uri]['author_uris'].append(author_uri)

        if author_uri not in authors:
            authors[author_uri] = {'author_name': author_name,
                'pub_uris' : [pub_uri],
                'concept_uris' : [concept_uri]}
        if concept_uri not in authors[author_uri]['concept_uris']:
            authors[author_uri]['concept_uris'].append(concept_uri)
        if pub_uri not in authors[author_uri]['pub_uris']:
            authors[author_uri]['pub_uris'].append(pub_uri)
            
        if concept_uri in conc:
            entry = conc[concept_uri]
            if author_uri not in entry['author_uris']:
                entry['author_uris'].append(author_uri)
            if pub_uri not in entry['pub_uris']:
                entry['pub_uris'].append(pub_uri)
        else:
            entry = {
                'concept_name': concept_name,
                'author_uris' : [author_uri],
                'pub_uris': [pub_uri],
                'concept_pairs' : {}
            }
        conc[concept_uri] = entry
    print "Pubs", len(pubs)
    print json.dumps(pubs, indent=4)
    print "Authors", len(authors)
    print json.dumps(authors, indent=4)
    return conc

log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
print >>log_file, datetime.now(), "VIVO Tools version", vt.__version__
print >>log_file, datetime.now(), "Reading concordance data"
data = json.load(open("concordance_data.json"))['results']['bindings']
print >>log_file, datetime.now(), "Concordance data has", len(data), \
      "co-occurances of concept, author and paper"
conc = shelve.open("conc", writeback=True)
conc = make_conc(conc, data, debug=True)
##for key,stuff in conc.items():
##    print >>log_file, datetime.now(), key
##    print >>log_file, datetime.now(), json.dumps(stuff, indent = 4)
print >>log_file, datetime.now(), "conc has ", len(conc)," concepts"
conc.close()
print >>log_file, datetime.now(), "Finish"
