from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from flask_cors import CORS
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

points_collecte_bp = Blueprint("points_collecte_bp", __name__)
CORS(points_collecte_bp)  # Autoriser CORS pour React

# === URIs des classes RDF ===
POINT_BASE = "http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/"
CLASSES = {
    "mobile": URIRef(POINT_BASE + "Point_de_Collecte_Mobile"),
    "poubelle": URIRef(POINT_BASE + "Poubelle_Publique"),
}
PARENT_CLASS = URIRef(POINT_BASE + "Point_de_collecte")

# === CREATE ===
@points_collecte_bp.route("/points_collecte", methods=["POST"])
def add_point_collecte():
    data = request.json
    point_id = "PC_" + data.get("name", "").replace(" ", "_")
    point_ref = EX[point_id]
    type_point = data.get("type", "mobile")
    class_uri = CLASSES.get(type_point, CLASSES["mobile"])

    # Association à un centre si fourni
    centre_id = data.get("centre_id")
    centre_ref = EX[centre_id] if centre_id else None

    # Construction de l'INSERT
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{point_ref}> a <{class_uri}> ;
                       ex:name "{data.get('name','')}"^^xsd:string ;
                       ex:location "{data.get('location','')}"^^xsd:string ;
                       ex:description "{data.get('description','')}"^^xsd:string
    """
    if centre_ref:
        insert_query += f" ; ex:associe_a <{centre_ref}> ."
        insert_query += f" <{centre_ref}> ex:avoir <{point_ref}> ."
    insert_query += " }"

    # Exécution SPARQL
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # Ajout local RDFLib
    g.add((point_ref, RDF.type, class_uri))
    g.add((point_ref, EX.name, Literal(data.get("name",""))))
    g.add((point_ref, EX.location, Literal(data.get("location",""))))
    g.add((point_ref, EX.description, Literal(data.get("description",""))))
    if centre_ref:
        g.add((point_ref, EX.associe_a, centre_ref))
        g.add((centre_ref, EX.avoir, point_ref))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ Point de collecte '{point_id}' ajouté avec succès."})


# === READ ALL ===
@points_collecte_bp.route("/points_collecte", methods=["GET"])
def get_points_collecte():
    query = PREFIX + """
    SELECT ?point ?type ?name ?location ?description ?associe_a
    WHERE {
        ?point a ?type ;
               ex:name ?name ;
               ex:location ?location ;
               ex:description ?description .
        OPTIONAL { ?point ex:associe_a ?associe_a }
        FILTER (?type IN (
            <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Point_de_Collecte_Mobile>,
            <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Poubelle_Publique>
        ))
    }
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    points = [{k: v["value"] for k, v in r.items()} for r in results["results"]["bindings"]]
    return jsonify({"count": len(points), "results": points})


# === READ ONE ===
@points_collecte_bp.route("/points_collecte/<point_id>", methods=["GET"])
def get_point_collecte(point_id):
    point_ref = EX[point_id]
    query = PREFIX + f"SELECT ?p ?o WHERE {{ <{point_ref}> ?p ?o . }}"
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = {r["p"]["value"].split('#')[-1]: r["o"]["value"] for r in results["results"]["bindings"]}
    return jsonify(data)


# === UPDATE ===
@points_collecte_bp.route("/points_collecte/<point_id>", methods=["PUT"])
def update_point_collecte(point_id):
    data = request.json
    point_ref = EX[point_id]
    type_point = data.get("type", "mobile")
    class_uri = CLASSES.get(type_point, CLASSES["mobile"])

    # Centre associé
    centre_id = data.get("centre_id")
    centre_ref = EX[centre_id] if centre_id else None

    # Supprimer anciens triplets
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    # Supprimer les triplets directs du point
    delete_query = PREFIX + f"DELETE WHERE {{ <{point_ref}> ?p ?o . }}"
    sparql.setQuery(delete_query)
    sparql.query()
    # Supprimer le triplet inverse si existant
    old_centres = list(g.objects(point_ref, EX.associe_a))
    for old_c in old_centres:
        delete_inverse = PREFIX + f"DELETE WHERE {{ <{old_c}> ex:avoir <{point_ref}> . }}"
        sparql.setQuery(delete_inverse)
        sparql.query()

    # Supprimer localement
    for t in list(g.triples((point_ref, None, None))):
        g.remove(t)
    for old_c in old_centres:
        g.remove((old_c, EX.avoir, point_ref))

    # INSERT des nouveaux triplets
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{point_ref}> a <{class_uri}> ;
                       ex:name "{data.get('name','')}"^^xsd:string ;
                       ex:location "{data.get('location','')}"^^xsd:string ;
                       ex:description "{data.get('description','')}"^^xsd:string
    """
    if centre_ref:
        insert_query += f" ; ex:associe_a <{centre_ref}> . <{centre_ref}> ex:avoir <{point_ref}> ."
    insert_query += " }"
    sparql.setQuery(insert_query)
    sparql.query()

    # Ajouter localement
    g.add((point_ref, RDF.type, class_uri))
    g.add((point_ref, EX.name, Literal(data.get("name",""))))
    g.add((point_ref, EX.location, Literal(data.get("location",""))))
    g.add((point_ref, EX.description, Literal(data.get("description",""))))
    if centre_ref:
        g.add((point_ref, EX.associe_a, centre_ref))
        g.add((centre_ref, EX.avoir, point_ref))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ Point de collecte '{point_id}' mis à jour avec succès."})


# === DELETE ===
@points_collecte_bp.route("/points_collecte/<point_id>", methods=["DELETE"])
def delete_point_collecte(point_id):
    point_ref = EX[point_id]

    # Récupérer le centre associé
    centre_refs = list(g.objects(point_ref, EX.associe_a))

    # Supprimer triplets dans Fuseki
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    delete_query = PREFIX + f"DELETE WHERE {{ <{point_ref}> ?p ?o . }}"
    sparql.setQuery(delete_query)
    sparql.query()

    # Supprimer les triplets inverses
    for c in centre_refs:
        delete_inverse = PREFIX + f"DELETE WHERE {{ <{c}> ex:avoir <{point_ref}> . }}"
        sparql.setQuery(delete_inverse)
        sparql.query()

    # Supprimer localement
    for t in list(g.triples((point_ref, None, None))):
        g.remove(t)
    for c in centre_refs:
        g.remove((c, EX.avoir, point_ref))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ Point de collecte '{point_id}' supprimé avec succès."})
