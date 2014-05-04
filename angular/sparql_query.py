"""
    sparql_query.py -- issue a SPARQL query to VIVO and return
    the result as a JSON object

    Version 0.1 MC 2013-12-28
    --  Initial version.

"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from vivotools import vivo_sparql_query
from json import dumps
from datetime import datetime

query = """
    # create sets of concept, author, publication

    SELECT ?pub_uri ?pub_name ?concept_uri ?concept_name ?author_uri
        ?author_name
    WHERE {
        ?pub_uri a bibo:AcademicArticle .
        ?pub_uri rdfs:label ?pub_name .
        ?pub_uri vivo:hasSubjectArea ?concept_uri .
        ?concept_uri rdfs:label ?concept_name .
        ?pub_uri vivo:informationResourceInAuthorship ?a .
        ?a vivo:linkedAuthor ?author_uri .
        ?author_uri rdfs:label ?author_name .
    } 
    ORDER BY ?pub_uri ?concept_uri ?author_uri
    OFFSET 0
    LIMIT 10
    """

print datetime.now(), "Start"
data = vivo_sparql_query(query)
print "Items found = ", len(data["results"]["bndings"])
json_file = open('concordance_data.json')
print >>json_file, json.dumps(data, sort_keys=True, indent=4)
print datetime.now(), "Finish"
