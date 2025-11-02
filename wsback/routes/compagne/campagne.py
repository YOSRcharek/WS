from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

campagne_bp = Blueprint("campagne_bp", __name__)

CAMPAGNE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/campagne_de_sensibilisation")


# --- CREATE ---
@campagne_bp.route("/campagnes", methods=["POST"])
def add_campagne():
    data = request.json
    cid = data.get("campaignID", f"Campagne_{len(g) + 1}")
    camp_ref = EX[cid]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {camp_ref.n3()} a <{CAMPAGNE_CLASS_URI}> ;
            ex:descriptioncampa "{data.get('descriptioncampa','')}"^^xsd:string ;
            ex:startDate "{data.get('startDate','')}"^^xsd:date ;
            ex:endDate "{data.get('endDate','')}"^^xsd:date ;
            ex:targetAudience "{data.get('targetAudience','')}"^^xsd:string ;
            ex:title "{data.get('title','')}"^^xsd:string .

        # Sous-classe Affiche
        ex:Affiche_{cid} a ex:Affiche ;
            ex:contenuimage "{data.get('contenuimage','')}"^^xsd:string ;
            ex:image "{data.get('image','')}"^^xsd:string ;
            ex:partOf {camp_ref.n3()} .

        # Sous-classe RéseauxSociaux
        ex:Reseau_{cid} a ex:ReseauxSociaux ;
            ex:contenu "{data.get('contenu','')}"^^xsd:string ;
            ex:lien "{data.get('lien','')}"^^xsd:string ;
            ex:nomPlateforme "{data.get('nomPlateforme','')}"^^xsd:string ;
            ex:partOf {camp_ref.n3()} .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.setMethod(POST)
    sparql.query()

    # Local RDF
    g.add((camp_ref, RDF.type, CAMPAGNE_CLASS_URI))
    g.add((camp_ref, EX.descriptioncampa, Literal(data.get('descriptioncampa', ''))))
    g.add((camp_ref, EX.startDate, Literal(data.get('startDate', ''), datatype=XSD.date)))
    g.add((camp_ref, EX.endDate, Literal(data.get('endDate', ''), datatype=XSD.date)))
    g.add((camp_ref, EX.targetAudience, Literal(data.get('targetAudience', ''))))
    g.add((camp_ref, EX.title, Literal(data.get('title', ''))))

    aff_ref = EX[f"Affiche_{cid}"]
    g.add((aff_ref, RDF.type, EX.Affiche))
    g.add((aff_ref, EX.contenuimage, Literal(data.get('contenuimage', ''))))
    g.add((aff_ref, EX.image, Literal(data.get('image', ''))))
    g.add((aff_ref, EX.partOf, camp_ref))

    res_ref = EX[f"Reseau_{cid}"]
    g.add((res_ref, RDF.type, EX.ReseauxSociaux))
    g.add((res_ref, EX.contenu, Literal(data.get('contenu', ''))))
    g.add((res_ref, EX.lien, Literal(data.get('lien', ''))))
    g.add((res_ref, EX.nomPlateforme, Literal(data.get('nomPlateforme', ''))))
    g.add((res_ref, EX.partOf, camp_ref))

    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Campagne '{cid}' ajoutée avec succès."})


# --- READ ALL ---
@campagne_bp.route("/campagnes", methods=["GET"])
def get_all_campagnes():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?campagne ?descriptioncampa ?startDate ?endDate ?targetAudience ?title
        WHERE {
            ?campagne a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/campagne_de_sensibilisation> .
            OPTIONAL { ?campagne ex:descriptioncampa ?descriptioncampa }
            OPTIONAL { ?campagne ex:startDate ?startDate }
            OPTIONAL { ?campagne ex:endDate ?endDate }
            OPTIONAL { ?campagne ex:targetAudience ?targetAudience }
            OPTIONAL { ?campagne ex:title ?title }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    campagnes = []
    for result in results["results"]["bindings"]:
        campagne_data = {k: v["value"] for k, v in result.items()}
        campagnes.append(campagne_data)

    return jsonify(campagnes)


# --- READ ONE ---
@campagne_bp.route("/campagnes/<campagne_id>", methods=["GET"])
def get_campagne(campagne_id):
    camp_ref = EX[campagne_id]
    query = PREFIX + f"""
    SELECT ?p ?o WHERE {{
        <{camp_ref}> ?p ?o .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    campagne = {}
    for r in results["results"]["bindings"]:
        key = r["p"]["value"].split("#")[-1]
        campagne[key] = r["o"]["value"]

    return jsonify(campagne)


# --- UPDATE ---
@campagne_bp.route("/campagnes/<campagne_id>", methods=["PUT"])
def update_campagne(campagne_id):
    data = request.json
    camp_ref = EX[campagne_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{camp_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{camp_ref}> a <{CAMPAGNE_CLASS_URI}> ;
            ex:descriptioncampa "{data.get('descriptioncampa','')}"^^xsd:string ;
            ex:startDate "{data.get('startDate','')}"^^xsd:date ;
            ex:endDate "{data.get('endDate','')}"^^xsd:date ;
            ex:targetAudience "{data.get('targetAudience','')}"^^xsd:string ;
            ex:title "{data.get('title','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"Campagne '{campagne_id}' mise à jour avec succès."})


# --- DELETE ---
@campagne_bp.route("/campagnes/<campagne_id>", methods=["DELETE"])
def delete_campagne(campagne_id):
    camp_ref = EX[campagne_id]
    delete_query = PREFIX + f"""
    DELETE WHERE {{
        <{camp_ref}> ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    # Supprimer du graphe local
    for t in list(g.triples((camp_ref, None, None))):
        g.remove(t)

    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Campagne '{campagne_id}' supprimée avec succès."})
