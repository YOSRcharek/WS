from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

affiche_bp = Blueprint("affiche_bp", __name__)

AFFICHE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/affiche")


# --- CREATE ---
@affiche_bp.route("/affiches", methods=["POST"])
def add_affiche():
    data = request.json
    aid = data.get("afficheID", f"Affiche_{len(g) + 1}")
    aff_ref = EX[aid]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {aff_ref.n3()} a <{AFFICHE_CLASS_URI}> ;
            ex:contenuimage "{data.get('contenuimage','')}"^^xsd:string ;
            ex:image "{data.get('image','')}"^^xsd:string ;
            ex:partOf ex:{data.get('campaignID','')} .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # Ajout dans RDF local
    g.add((aff_ref, RDF.type, AFFICHE_CLASS_URI))
    g.add((aff_ref, EX.contenuimage, Literal(data.get('contenuimage', ''))))
    g.add((aff_ref, EX.image, Literal(data.get('image', ''))))
    g.add((aff_ref, EX.partOf, EX[data.get('campaignID', '')]))
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Affiche '{aid}' ajoutée avec succès."})


# --- READ ALL ---
@affiche_bp.route("/affiches", methods=["GET"])
def get_all_affiches():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?affiche ?contenuimage ?image ?campaign
        WHERE {
            ?affiche a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/affiche> .
            OPTIONAL { ?affiche ex:contenuimage ?contenuimage }
            OPTIONAL { ?affiche ex:image ?image }
            OPTIONAL { ?affiche ex:partOf ?campaign }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    affiches = []
    for result in results["results"]["bindings"]:
        affiche_data = {k: v["value"] for k, v in result.items()}
        affiches.append(affiche_data)

    return jsonify(affiches)

# --- READ ONE ---
@affiche_bp.route("/affiches/<affiche_id>", methods=["GET"])
def get_affiche(affiche_id):
    aff_ref = EX[affiche_id]
    query = PREFIX + f"""
    SELECT ?p ?o WHERE {{
        <{aff_ref}> ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    affiche = {r["p"]["value"].split("#")[-1]: r["o"]["value"] for r in results["results"]["bindings"]}
    return jsonify(affiche)


# --- UPDATE ---
@affiche_bp.route("/affiches/<affiche_id>", methods=["PUT"])
def update_affiche(affiche_id):
    data = request.json
    aff_ref = EX[affiche_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{aff_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{aff_ref}> a <{AFFICHE_CLASS_URI}> ;
            ex:contenuimage "{data.get('contenuimage','')}"^^xsd:string ;
            ex:image "{data.get('image','')}"^^xsd:string ;
            ex:partOf ex:{data.get('campaignID','')} .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"✅ Affiche '{affiche_id}' mise à jour avec succès."})


# --- DELETE ---
@affiche_bp.route("/affiches/<affiche_id>", methods=["DELETE"])
def delete_affiche(affiche_id):
    aff_ref = EX[affiche_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{aff_ref}> ?p ?o . }}"

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for t in list(g.triples((aff_ref, None, None))):
        g.remove(t)
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"🗑️ Affiche '{affiche_id}' supprimée avec succès."})
