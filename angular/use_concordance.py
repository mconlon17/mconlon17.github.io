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
import os
import sys
import shelve

from datetime import datetime


log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
concordance = shelve.open("conc2")
print "Concordance has ", len(concordance)," concepts"
for uri, name in concordance.items():
    print uri, name
print >>log_file, datetime.now(), "Finish"
