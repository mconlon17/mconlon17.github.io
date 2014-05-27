#!/usr/bin/env/python
"""
    subset_concordance.py -- Little cases to show concordance

    Version 0.1 MC 2014-05-11
    --  Create a subset concordance with controllable cutoffs

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from vivotools import vivo_sparql_query
from vivotools import get_vivo_uri
from vivotools import assert_resource_property
from vivotools import assert_data_property
from vivotools import update_data_property
from vivotools import get_vivo_value
from vivotools import get_triples
from random import randint
import os
import sys
import shelve
import json
import operator

from datetime import datetime

# Concepts must meet cutoff criteria.  If author list is empty, the concept
# is not in the subset.  

author_cutoff = 2 # authors must have at least 2 papers with concept
concept_cutoff = 2 # concept must have at least two papers with concept
pubs_cutoff = 2 # concept must have at least two papers

log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
conc = shelve.open("conc")
subset = shelve.open("subset")

for concept_uri in conc.keys():
    entry = conc[concept_uri]
    authors = dict((k,v) for k,v in entry['authors'].items() \
                    if int(v['count']) >= author_cutoff)
    concepts = dict((k,v) for k,v in entry['concepts'].items() \
                    if int(v['count']) >= concept_cutoff)
    if int(entry['npubs']) >= pubs_cutoff and \
        len(authors) > 0 and \
        len(concepts) > 0:
        entry['authors'] = authors
        entry['concepts'] = concepts
        subset[concept_uri] = entry
        print "accept concept", entry['name'], entry['npubs'], \
              len(entry['authors']), len(entry['concepts'])
    else:
        print "trim concept", entry['name'], entry['npubs'], \
              len(entry['authors']), len(entry['concepts'])

for concept, stuff in sorted(subset.items(), reverse=True,
                             key = lambda x: int(x[1]['npubs'])):
    print concept, stuff['name'], stuff['npubs']
for concept, stuff in sorted(subset.items(), reverse=True,
                             key = lambda x: len(x[1]['authors'])):
    print concept, stuff['name'], len(stuff['authors'])



# Write json for subset

d = {}
for concept, value in subset.items():
  d[concept] = value
json_file = open('subset.json', "w")
print >>json_file, json.dumps(d, indent=4)
json_file.close()
conc.close()
subset.close()
print >>log_file, datetime.now(), "Finish"
