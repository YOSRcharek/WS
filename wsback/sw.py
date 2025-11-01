from flask import Flask, jsonify, request
from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
import os

app = Flask(__name__)

# === Fuseki config ===
FUSEKI_UPDATE_URL = "http://localhost:3030/wasteDB/update"
PREFIX = """PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

# === Fichier RDF local pour Protégé ===
RDF_FILE =  r"C:\Users\MSI\Desktop\dechet.ttl"

g = Graph()

# Charger le fichier RDF si il existe
if os.path.exists(RDF_FILE):
    g.parse(RDF_FILE, format="turtle")
g.bind("ex", Namespace("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#"))
g.bind("rdfs", RDFS)
EX = Namespace("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#")

# --- Route pour ajouter un déchet ---
@app.route("/dechets", methods=["POST"])
def add_dechet():
    data = request.json
    name = data["name"]
    dechet_uri = f"ex:{name}"

    # --- 1️⃣ Ajouter dans Fuseki ---
    insert_query = PREFIX + f"""
        INSERT DATA {{
            {dechet_uri} a ex:Dechet ;
                rdfs:label "{data.get('label', name)}" ;
                ex:nomdechet "{data.get('nomdechet', name)}"^^xsd:string ;
                ex:description "{data.get('description', '')}"^^xsd:string ;
                ex:couleur "{data.get('couleur', '')}"^^xsd:string ;
                ex:poids "{data.get('poids', 0)}"^^xsd:float ;
                ex:isrecyclable "{str(data.get('isRecyclable', True)).lower()}"^^xsd:boolean ;
                ex:quantite "{data.get('quantite', 0)}"^^xsd:decimal ;
                ex:generatedDate "{data.get('generatedDate', '')}"^^xsd:date .
        }}
    """
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.method = 'POST'
    sparql.query()

    # --- 2️⃣ Ajouter dans rdflib local pour Protégé ---
    dechet_ref = EX[name]
    g.add((dechet_ref, RDF.type, EX.Dechet))
    g.add((dechet_ref, RDFS.label, Literal(data.get('label', name))))
    g.add((dechet_ref, EX.nomdechet, Literal(data.get('nomdechet', name), datatype=XSD.string)))
    g.add((dechet_ref, EX.description, Literal(data.get('description', ''), datatype=XSD.string)))
    g.add((dechet_ref, EX.couleur, Literal(data.get('couleur', ''), datatype=XSD.string)))
    g.add((dechet_ref, EX.poids, Literal(data.get('poids', 0), datatype=XSD.float)))
    g.add((dechet_ref, EX.isrecyclable, Literal(data.get('isrecyclable', True), datatype=XSD.boolean)))
    g.add((dechet_ref, EX.quantite, Literal(data.get('quantite', 0), datatype=XSD.decimal)))
    g.add((dechet_ref, EX.generatedDate, Literal(data.get('generatedDate', ''), datatype=XSD.date)))

    # Sauvegarder le fichier RDF local
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Déchet '{name}' ajouté dans Fuseki et Protégé !"})

if __name__ == "__main__":
    app.run(debug=True)
