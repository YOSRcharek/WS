from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Literal
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
from rdflib import Literal, URIRef
formation_bp = Blueprint("formation_bp", __name__)
FORMATION_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/FormationPersonnel")


# ✅ CREATE (POST)
@formation_bp.route("/formations", methods=["POST"])
def add_formation():
    data = request.json
    form_id = "F" + str(len(g) + 1)
    form_ref = EX[form_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {form_ref.n3()} a <{FORMATION_CLASS_URI}> ;
            ex:formationID "{form_id}"^^xsd:string ;
            ex:nombreParticipants "{data.get('nombreParticipants', 0)}"^^xsd:integer ;
            ex:publicCible "{data.get('publicCible', '')}"^^xsd:string ;
            ex:zoneCible "{data.get('zoneCible', '')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.method = 'POST'
    sparql.query()

    # Mise à jour locale
    g.add((form_ref, RDF.type, FORMATION_CLASS_URI))
    g.add((form_ref, EX.formationID, Literal(form_id, datatype=XSD.string)))
    g.add((form_ref, EX.nombreParticipants, Literal(data.get('nombreParticipants', 0), datatype=XSD.integer)))
    g.add((form_ref, EX.publicCible, Literal(data.get('publicCible', ''), datatype=XSD.string)))
    g.add((form_ref, EX.zoneCible, Literal(data.get('zoneCible', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Formation '{form_id}' ajoutée avec succès !"}), 201


# ✅ READ ALL (GET)
@formation_bp.route("/formations", methods=["GET"])
def get_all_formations():
    query = PREFIX + """
    SELECT ?id ?nombreParticipants ?publicCible ?zoneCible
    WHERE {
        ?s a ex:formationPersonnel ;
           ex:formationID ?id ;
           ex:nombreParticipants ?nombreParticipants ;
           ex:publicCible ?publicCible ;
           ex:zoneCible ?zoneCible .
    }
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    formations = []
    for r in results["results"]["bindings"]:
        formations.append({
            "formationID": r["id"]["value"],
            "nombreParticipants": int(r["nombreParticipants"]["value"]),
            "publicCible": r["publicCible"]["value"],
            "zoneCible": r["zoneCible"]["value"]
        })

    return jsonify(formations), 200


# ✅ READ ONE (GET BY ID)
@formation_bp.route("/formations/<string:formation_id>", methods=["GET"])
def get_formation_by_id(formation_id):
    query = PREFIX + f"""
    SELECT ?nombreParticipants ?publicCible ?zoneCible
    WHERE {{
        ?s a ex:formationPersonnel ;
           ex:formationID "{formation_id}"^^xsd:string ;
           ex:nombreParticipants ?nombreParticipants ;
           ex:publicCible ?publicCible ;
           ex:zoneCible ?zoneCible .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return jsonify({"error": f"❌ Formation '{formation_id}' non trouvée"}), 404

    r = results["results"]["bindings"][0]
    formation = {
        "formationID": formation_id,
        "nombreParticipants": int(r["nombreParticipants"]["value"]),
        "publicCible": r["publicCible"]["value"],
        "zoneCible": r["zoneCible"]["value"]
    }

    return jsonify(formation), 200


# ✅ UPDATE (PUT)
@formation_bp.route("/formations/<string:formation_id>", methods=["PUT"])
def update_formation(formation_id):
    data = request.json

    update_query = PREFIX + f"""
    DELETE {{
        ?s ex:nombreParticipants ?oldP ;
           ex:publicCible ?oldC ;
           ex:zoneCible ?oldZ .
    }}
    INSERT {{
        ?s ex:nombreParticipants "{data.get('nombreParticipants', 0)}"^^xsd:integer ;
           ex:publicCible "{data.get('publicCible', '')}"^^xsd:string ;
           ex:zoneCible "{data.get('zoneCible', '')}"^^xsd:string .
    }}
    WHERE {{
        ?s a ex:formationPersonnel ;
           ex:formationID "{formation_id}"^^xsd:string ;
           ex:nombreParticipants ?oldP ;
           ex:publicCible ?oldC ;
           ex:zoneCible ?oldZ .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(update_query)
    sparql.method = 'POST'
    sparql.query()

    return jsonify({"message": f"✏️ Formation '{formation_id}' mise à jour avec succès !"}), 200


# ✅ DELETE
@formation_bp.route("/formations/<string:formation_id>", methods=["DELETE"])
def delete_formation(formation_id):
    delete_query = PREFIX + f"""
    DELETE WHERE {{
        ?s a ex:formationPersonnel ;
           ex:formationID "{formation_id}"^^xsd:string ;
           ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(delete_query)
    sparql.method = 'POST'
    sparql.query()

    return jsonify({"message": f"🗑️ Formation '{formation_id}' supprimée avec succès !"}), 200
