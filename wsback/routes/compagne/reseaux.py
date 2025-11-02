from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

reseaux_bp = Blueprint("reseaux_bp", __name__)

RESEAUX_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/réseaux_sociaux")


# --- CREATE ---
@reseaux_bp.route("/reseaux", methods=["POST"])
def add_reseau():
    data = request.json
    rid = data.get("reseauID", f"Reseau_{len(g) + 1}")
    res_ref = EX[rid]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {res_ref.n3()} a <{RESEAUX_CLASS_URI}> ;
            ex:contenu "{data.get('contenu','')}"^^xsd:string ;
            ex:lien "{data.get('lien','')}"^^xsd:string ;
            ex:nomPlateforme "{data.get('nomPlateforme','')}"^^xsd:string ;
            ex:partOf ex:{data.get('campaignID','')} .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    g.add((res_ref, RDF.type, RESEAUX_CLASS_URI))
    g.add((res_ref, EX.contenu, Literal(data.get('contenu', ''))))
    g.add((res_ref, EX.lien, Literal(data.get('lien', ''))))
    g.add((res_ref, EX.nomPlateforme, Literal(data.get('nomPlateforme', ''))))
    g.add((res_ref, EX.partOf, EX[data.get('campaignID', '')]))
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Réseau '{rid}' ajouté avec succès."})


# --- READ ALL ---
@reseaux_bp.route("/reseaux", methods=["GET"])
def get_all_reseaux():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?reseau ?contenu ?lien ?nomPlateforme ?campaign
        WHERE {
            ?reseau a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/réseaux_sociaux> .
            OPTIONAL { ?reseau ex:contenu ?contenu }
            OPTIONAL { ?reseau ex:lien ?lien }
            OPTIONAL { ?reseau ex:nomPlateforme ?nomPlateforme }
            OPTIONAL { ?reseau ex:partOf ?campaign }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    reseaux = []
    for result in results["results"]["bindings"]:
        reseau_data = {k: v["value"] for k, v in result.items()}
        reseaux.append(reseau_data)

    return jsonify(reseaux)


# --- READ ONE ---
@reseaux_bp.route("/reseaux/<reseau_id>", methods=["GET"])
def get_reseau(reseau_id):
    res_ref = EX[reseau_id]
    query = PREFIX + f"""
    SELECT ?p ?o WHERE {{
        <{res_ref}> ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    reseau = {r["p"]["value"].split("#")[-1]: r["o"]["value"] for r in results["results"]["bindings"]}
    return jsonify(reseau)


# --- UPDATE ---
@reseaux_bp.route("/reseaux/<reseau_id>", methods=["PUT"])
def update_reseau(reseau_id):
    data = request.json
    res_ref = EX[reseau_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{res_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{res_ref}> a <{RESEAUX_CLASS_URI}> ;
            ex:contenu "{data.get('contenu','')}"^^xsd:string ;
            ex:lien "{data.get('lien','')}"^^xsd:string ;
            ex:nomPlateforme "{data.get('nomPlateforme','')}"^^xsd:string ;
            ex:partOf ex:{data.get('campaignID','')} .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"✅ Réseau '{reseau_id}' mis à jour avec succès."})


# --- DELETE ---
@reseaux_bp.route("/reseaux/<reseau_id>", methods=["DELETE"])
def delete_reseau(reseau_id):
    res_ref = EX[reseau_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{res_ref}> ?p ?o . }}"

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for t in list(g.triples((res_ref, None, None))):
        g.remove(t)
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"🗑️ Réseau '{reseau_id}' supprimé avec succès."})
