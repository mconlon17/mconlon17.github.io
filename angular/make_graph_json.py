#!/usr/bin/env/python
"""
    make_graph_json.py -- Given a concordance and the uri of a concept,
    make a json map file ready for display in D3 as a force directed
    graph

    Version 0.0 MC 2014-05-12
    --  Getting started

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
conc = shelve.open("subset")

concept_uri = "http://vivo.ufl.edu/individual/n8300635913" # Pulmonary hyper
concept_uri = "http://vivo.ufl.edu/individual/n2480637734" # ADD
concept_uri = "http://vivo.ufl.edu/individual/n2284306921" # VA
entry = conc[concept_uri]
graph = {"nodes":[], "links":[], "concept": {"name": entry["name"],
                                             "npubs": entry["npubs"],
                                             "uri": concept_uri}}
graph["nodes"].append({"name":entry["name"],"group":1,
                     "npubs":entry["npubs"],
                     "uri":concept_uri})
k = 0
for name,data in entry["concepts"].items():
    k = k + 1
    node = {"name":name,
              "group":1,
              "npubs":data["count"],
              "uri":data["concept_uri"]}
    link = {"source":0,
              "target":k,
              "value":data["count"]}
    graph["nodes"].append(node)
    graph["links"].append(link)

    # Add secondary concepts, yes this could be recursive, but we are stopping
    # at distance 2 for everyone's sanity.  Hmm.  This is quick and dirty.  We
    # really need to look up each new concept and author and connect accordingly

    k0 = k
    concept_uri = str(data["concept_uri"])
    if concept_uri in conc:
        sub_entry = conc[concept_uri]
        s = 0
        for name,data in sub_entry["concepts"].items():
            s = s + 1
            if s > 5:
                continue
            k = k + 1
            node = {"name":name,
                      "group":1,
                      "npubs":data["count"],
                      "uri":data["concept_uri"]}
            link = {"source":k0,
                      "target":k,
                      "value":data["count"]}
            graph["nodes"].append(node)
            graph["links"].append(link)
        s = 0
        for name,data in sub_entry["authors"].items():
            s = s + 1
            if s > 5:
                continue
            k = k + 1
            node = {"name":name,
                      "group":2,
                      "npubs":data["count"],
                      "uri":data["author_uri"]}
            link = {"source":k0,
                      "target":k,
                      "value":data["count"]}
            graph["nodes"].append(node)
            graph["links"].append(link)
    
for name,data in entry["authors"].items():
    k = k + 1
    node = {"name":name,
              "group":2,
              "npubs":data["count"],
              "uri":data["author_uri"]}
    link = {"source":0,
              "target":k,
              "value":data["count"]}
    graph["nodes"].append(node)
    graph["links"].append(link)
json_file = open("graph.json", "w")
print >>json_file, json.dumps(graph, indent=4)
json_file.close()
print >>log_file, datetime.now(), "Finish"
