#!/usr/bin/env/python
"""
    use_concordance.py -- Little cases to show concordance

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
from random import randint
import os
import sys
import shelve
import json
import operator

from datetime import datetime

cutoff = 50
log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
subset = shelve.open("subset")
##print "Concordance has ", len(concordance)," concepts"
##subset = shelve.open("subset")
##entries = dict((name,val) for name,val in concordance.items()\
##                      if int(val['npubs']) > cutoff and \
##               len(val['authors']) > cutoff and len(val['concepts']) > cutoff)
##print len(entries), "concepts with more than", cutoff, \
##      "pubs, authors, and co-occuring concepts"
##for key, val in entries.items():
##    subset[key] = val
##uri = subset.keys()[randint(0,len(subset))]
##stuff = subset[uri]
##print "\nConcept", uri, stuff['name']
##print "Authors", stuff['authors']
##print "Concepts", stuff['concepts']
##subset.close()
for concept, stuff in sorted(subset.items(), reverse=True,
                             key = lambda x: int(x[1]['npubs'])):
    print concept, stuff['name'], stuff['npubs']
for concept, stuff in sorted(subset.items(), reverse=True,
                             key = lambda x: len(x[1]['authors'])):
    print concept, stuff['name'], len(stuff['authors'])
d = {}
for concept, value in subset.items():
  d[concept] = value
json_file = open('subset.json', "w")
print >>json_file, json.dumps(d, indent=4)
json_file.close()
print >>log_file, datetime.now(), "Finish"
