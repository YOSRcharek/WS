from rdflib import Graph, Namespace
from rdflib.namespace import RDFS
import os

# === Config générale ===
FUSEKI_UPDATE_URL = "http://localhost:3030/wasteDB/update"
FUSEKI_QUERY_URL = "http://localhost:3030/wasteDB/query"

PREFIX = """PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

RDF_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dechet.ttl")

# === Initialisation du graphe RDF ===
g = Graph()

if os.path.exists(RDF_FILE):
    g.parse(RDF_FILE, format="turtle")

EX = Namespace("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#")

# Bind namespaces
g.bind("ex", EX)
g.bind("rdfs", RDFS)
