
from flask_mail import Mail, Message
from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Graph, Namespace, Literal, RDF, URIRef, XSD
from flask_cors import CORS
import re
from config import g, EX, FUSEKI_UPDATE_URL, RDF_FILE
from flask import Blueprint, jsonify, request, current_app
from flask_mail import Message


nlp_bp = Blueprint("nlp_bp", __name__)
CORS(nlp_bp)

# === URIs des classes RDF ===
ONTOLOGY_BASE = "http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/"
CLASSES = {
    "mobile": URIRef(ONTOLOGY_BASE + "Point_de_Collecte_Mobile"),
    "poubelle": URIRef(ONTOLOGY_BASE + "Poubelle_Publique"),
}
CENTRE_REF_DEFAULT = URIRef(ONTOLOGY_BASE + "Cpo")

# === Route pour ajouter un point de collecte ===
# === Route pour ajouter un point de collecte ===
@nlp_bp.route("/points_collecte_nlp", methods=["POST"])
def add_point_collecte_nlp():
    data = request.json
    phrase = data.get("phrase")
    if not phrase:
        return jsonify({"error": "Aucune phrase fournie"}), 400

    # Extraction nom, localisation, centre, type
    match_name = re.search(r'nomm[ée]\s+(.+?)\s+(?:à|assoc|centre|$)', phrase) or re.search(r'nom:([^\s]+)', phrase)
    match_location = re.search(r'à\s+([^\s]+)', phrase) or re.search(r'location:([^\s]+)', phrase)
    match_centre = re.search(r'centre\s+([^\s]+)', phrase) or re.search(r'centre:([^\s]+)', phrase)
    match_type = re.search(r'(mobile|poubelle)', phrase, re.IGNORECASE)

    point_name = match_name.group(1).strip() if match_name else "Point_Collecte_Test"
    location = match_location.group(1) if match_location else "Tunis"
    centre_name = match_centre.group(1) if match_centre else "Cpo"
    point_type = match_type.group(1).lower() if match_type else "mobile"

    # Génération URIs
    point_id = "PC_" + point_name.replace(" ", "_")
    point_ref = URIRef(ONTOLOGY_BASE + point_id)
    centre_ref = URIRef(ONTOLOGY_BASE + centre_name)
    class_uri = CLASSES.get(point_type, CLASSES["mobile"])

    # Requête SPARQL INSERT DATA
    sparql_query = f"""
PREFIX ex: <{ONTOLOGY_BASE}>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

INSERT DATA {{
  <{point_ref}> a <{class_uri}> ;
      ex:name "{point_name}"^^xsd:string ;
      ex:location "{location}"^^xsd:string ;
      ex:description "Point de collecte généré depuis la phrase"^^xsd:string ;
      ex:associe_a <{centre_ref}> .

  <{centre_ref}> ex:avoir <{point_ref}> .
}}
"""

    # Ajout local RDFLib
    g.add((point_ref, RDF.type, class_uri))
    g.add((point_ref, EX.name, Literal(point_name, datatype=XSD.string)))
    g.add((point_ref, EX.location, Literal(location, datatype=XSD.string)))
    g.add((point_ref, EX.description, Literal("Point de collecte généré depuis la phrase", datatype=XSD.string)))
    g.add((point_ref, EX.associe_a, centre_ref))
    g.add((centre_ref, EX.avoir, point_ref))
    g.serialize(destination=RDF_FILE, format="turtle")

    # Exécution SPARQL sur Fuseki
    try:
        sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql.setMethod(POST)
        sparql.setQuery(sparql_query)
        sparql.query()
    except Exception as e:
        return jsonify({
            "error": "SPARQL execution failed",
            "details": str(e),
            "sparql_generated": sparql_query
        }), 500

    # === Envoi du mail ===
    try:
        msg = Message(
            subject="Nouveau point de collecte ajouté",
            recipients=["abdessalemchaouch9217@gmail.com"],  # destinataire réel
            body=f"Le point de collecte '{point_name}' a été ajouté au centre '{centre_name}' à {location}."
        )
        current_app.extensions['mail'].send(msg)
    except Exception as e:
        print("Erreur lors de l'envoi du mail:", e)

    return jsonify({
        "message": f"✅ Point de collecte '{point_name}' ajouté avec succès et associé au centre '{centre_name}'.",
        "sparql_generated": sparql_query
    })

@nlp_bp.route("/points_collecte_filtre", methods=["GET"])
def filter_points_collecte():
    sparql_query = f"""
PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?point ?name ?location ?centre ?capacity
WHERE {{
    ?point a ex:Point_de_Collecte_Mobile ;
           ex:name ?name ;
           ex:location ?location ;
           ex:associe_a ?centre .
    ?centre ex:capacity_center ?capacity .
    FILTER(xsd:integer(?capacity) > 100)
}}
"""
    try:
        from SPARQLWrapper import SPARQLWrapper, JSON
        from config import FUSEKI_QUERY_URL

        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setReturnFormat(JSON)
        sparql.setQuery(sparql_query)
        results = sparql.query().convert()

        points = []
        for result in results["results"]["bindings"]:
            points.append({
                "point_uri": result["point"]["value"],
                "name": result["name"]["value"],
                "location": result["location"]["value"],
                "centre_uri": result["centre"]["value"],
                "capacity": int(result["capacity"]["value"])
            })

        return jsonify({"points_filtered": points})

    except Exception as e:
        return jsonify({
            "error": "SPARQL execution failed",
            "details": str(e),
            "sparql_generated": sparql_query
        }), 500
