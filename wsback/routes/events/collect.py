from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Literal
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
from rdflib import Literal, URIRef
collecte_bp = Blueprint("collecte_bp", __name__)
COLLECTE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Collecte")


# ✅ CREATE (POST)
@collecte_bp.route("/collectes", methods=["POST"])
def add_collecte():
    data = request.json
    collecte_id = "C" + str(len(g) + 1)
    col_ref = EX[collecte_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {col_ref.n3()} a <{COLLECTE_CLASS_URI}> ;
            ex:collecteID "{collecte_id}"^^xsd:string ;
            ex:nombreBenevoles "{data.get('nombreBenevoles', 0)}"^^xsd:integer ;
            ex:quantitecollecte "{data.get('quantitecollecte', 0)}"^^xsd:decimal .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.method = 'POST'
    sparql.query()

    # Ajout local
    g.add((col_ref, RDF.type, COLLECTE_CLASS_URI))
    g.add((col_ref, EX.collecteID, Literal(collecte_id, datatype=XSD.string)))
    g.add((col_ref, EX.nombreBenevoles, Literal(data.get('nombreBenevoles', 0), datatype=XSD.integer)))
    g.add((col_ref, EX.quantitecollecte, Literal(data.get('quantitecollecte', 0), datatype=XSD.decimal)))
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Collecte '{collecte_id}' ajoutée avec succès !"}), 201


# ✅ READ ALL (GET)
@collecte_bp.route("/collectes", methods=["GET"])
def get_all_collectes():
    query = PREFIX + """
    SELECT ?id ?nombreBenevoles ?quantitecollecte
    WHERE {
        ?s a ex:collecte ;
           ex:collecteID ?id ;
           ex:nombreBenevoles ?nombreBenevoles ;
           ex:quantitecollecte ?quantitecollecte .
    }
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    collectes = []
    for r in results["results"]["bindings"]:
        collectes.append({
            "collecteID": r["id"]["value"],
            "nombreBenevoles": int(r["nombreBenevoles"]["value"]),
            "quantitecollecte": float(r["quantitecollecte"]["value"])
        })

    return jsonify(collectes), 200


# ✅ READ ONE (GET BY ID)
@collecte_bp.route("/collectes/<string:collecte_id>", methods=["GET"])
def get_collecte_by_id(collecte_id):
    query = PREFIX + f"""
    SELECT ?nombreBenevoles ?quantitecollecte
    WHERE {{
        ?s a ex:collecte ;
           ex:collecteID "{collecte_id}"^^xsd:string ;
           ex:nombreBenevoles ?nombreBenevoles ;
           ex:quantitecollecte ?quantitecollecte .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return jsonify({"error": f"❌ Collecte '{collecte_id}' non trouvée"}), 404

    r = results["results"]["bindings"][0]
    collecte = {
        "collecteID": collecte_id,
        "nombreBenevoles": int(r["nombreBenevoles"]["value"]),
        "quantitecollecte": float(r["quantitecollecte"]["value"])
    }

    return jsonify(collecte), 200


# ✅ UPDATE (PUT)
@collecte_bp.route("/collectes/<string:collecte_id>", methods=["PUT"])
def update_collecte(collecte_id):
    data = request.json

    delete_old = PREFIX + f"""
    DELETE {{
        ?s ex:nombreBenevoles ?oldB ;
           ex:quantitecollecte ?oldQ .
    }}
    INSERT {{
        ?s ex:nombreBenevoles "{data.get('nombreBenevoles', 0)}"^^xsd:integer ;
           ex:quantitecollecte "{data.get('quantitecollecte', 0)}"^^xsd:decimal .
    }}
    WHERE {{
        ?s a ex:collecte ;
           ex:collecteID "{collecte_id}"^^xsd:string ;
           ex:nombreBenevoles ?oldB ;
           ex:quantitecollecte ?oldQ .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(delete_old)
    sparql.method = 'POST'
    sparql.query()

    return jsonify({"message": f"✏️ Collecte '{collecte_id}' mise à jour avec succès !"}), 200


# ✅ DELETE
@collecte_bp.route("/collectes/<string:collecte_id>", methods=["DELETE"])
def delete_collecte(collecte_id):
    delete_query = PREFIX + f"""
    DELETE WHERE {{
        ?s a ex:collecte ;
           ex:collecteID "{collecte_id}"^^xsd:string ;
           ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(delete_query)
    sparql.method = 'POST'
    sparql.query()

    return jsonify({"message": f"🗑️ Collecte '{collecte_id}' supprimée avec succès !"}), 200
