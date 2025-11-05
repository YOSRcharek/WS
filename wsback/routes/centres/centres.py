from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
import requests
centres_bp = Blueprint("centres_bp", __name__)

# === URIs des classes RDF ===
CENTRE_BASE = "http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/"
CLASSES = {
    "centre_de_recyclage": URIRef(CENTRE_BASE + "centre_de_recyclage"),
    "centre_de_compostage": URIRef(CENTRE_BASE + "Centre_de_Compostage"),
    "centre_de_traitement_dangereux": URIRef(CENTRE_BASE + "Centre_de_Traitement_des_Déchets_Dangereux"),
    "usine_recyclage_metaux": URIRef(CENTRE_BASE + "Usine_de_Recyclage_Métaux")
}

# === CREATE ===
@centres_bp.route("", methods=["POST"])
def add_centre():
    data = request.json
    centre_id = "C" + data.get("centerName", "").replace(" ", "_")
    centre_ref = EX[centre_id]
    type_centre = data.get("type", "centre_de_recyclage")
    class_uri = CLASSES.get(type_centre, CLASSES["centre_de_recyclage"])

    # === Construction de la requête INSERT ===
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{centre_ref}> a <{class_uri}> ;
            ex:centerName "{data.get('centerName','')}"^^xsd:string ;
            ex:capacity_center "{data.get('capacity_center','')}"^^xsd:string ;
            ex:energyConsumption "{data.get('energyConsumption','')}"^^xsd:string ;
            ex:location_center "{data.get('location_center','')}"^^xsd:string ;
            ex:typeDeDechetTraite "{data.get('typeDeDechetTraite','')}"^^xsd:string ;
            ex:operation_Status "{data.get('operation_Status','')}"^^xsd:string ;
            ex:recyclingRate "{data.get('recyclingRate','')}"^^xsd:string
    """

    # Ajout des attributs spécifiques selon le type
    if type_centre == "centre_de_compostage":
        insert_query += f' ; ex:tempsCompostage "{data.get("tempsCompostage","")}"^^xsd:string'
    elif type_centre == "centre_de_traitement_dangereux":
        insert_query += f' ; ex:equipementSpecialisee "{data.get("equipementSpecialisee","")}"^^xsd:string'
    elif type_centre == "usine_recyclage_metaux":
        insert_query += f' ; ex:equipmentRecyclagemetaux "{data.get("equipmentRecyclagemetaux","")}"^^xsd:string ; ex:typeDeMetauxTraites "{data.get("typeDeMetauxTraites","")}"^^xsd:string'

    insert_query += " . }"

    # === Exécution dans Fuseki ===
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # === Ajout local RDFLib ===
    g.add((centre_ref, RDF.type, class_uri))
    g.add((centre_ref, EX.centerName, Literal(data.get("centerName",""))))
    g.add((centre_ref, EX.capacity_center, Literal(data.get("capacity_center",""))))
    g.add((centre_ref, EX.energyConsumption, Literal(data.get("energyConsumption",""))))
    g.add((centre_ref, EX.location_center, Literal(data.get("location_center",""))))
    g.add((centre_ref, EX.typeDeDechetTraite, Literal(data.get("typeDeDechetTraite",""))))
    g.add((centre_ref, EX.operation_Status, Literal(data.get("operation_Status",""))))
    g.add((centre_ref, EX.recyclingRate, Literal(data.get("recyclingRate",""))))

    # Champs spécifiques
    if type_centre == "centre_de_compostage":
        g.add((centre_ref, EX.tempsCompostage, Literal(data.get("tempsCompostage",""))))
    elif type_centre == "centre_de_traitement_dangereux":
        g.add((centre_ref, EX.equipementSpecialisee, Literal(data.get("equipementSpecialisee",""))))
    elif type_centre == "usine_recyclage_metaux":
        g.add((centre_ref, EX.equipmentRecyclagemetaux, Literal(data.get("equipmentRecyclagemetaux",""))))
        g.add((centre_ref, EX.typeDeMetauxTraites, Literal(data.get("typeDeMetauxTraites",""))))

    # Sauvegarde du graphe local
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Centre '{centre_id}' ajouté avec succès."})

# === READ ALL ===
@centres_bp.route("", methods=["GET"])
def get_centres():
    query = PREFIX + """
    SELECT ?centre ?type ?centerName ?capacity_center ?energyConsumption
           ?location_center ?typeDeDechetTraite ?operation_Status ?recyclingRate
           ?tempsCompostage ?equipementSpecialisee ?equipmentRecyclagemetaux ?typeDeMetauxTraites
    WHERE {
        ?centre a ?type ;
                 ex:centerName ?centerName ;
                 ex:capacity_center ?capacity_center ;
                 ex:energyConsumption ?energyConsumption ;
                 ex:location_center ?location_center ;
                 ex:typeDeDechetTraite ?typeDeDechetTraite ;
                 ex:operation_Status ?operation_Status ;
                 ex:recyclingRate ?recyclingRate .
        OPTIONAL { ?centre ex:tempsCompostage ?tempsCompostage }
        OPTIONAL { ?centre ex:equipementSpecialisee ?equipementSpecialisee }
        OPTIONAL { ?centre ex:equipmentRecyclagemetaux ?equipmentRecyclagemetaux }
        OPTIONAL { ?centre ex:typeDeMetauxTraites ?typeDeMetauxTraites }
    }
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    centres = []
    for r in results["results"]["bindings"]:
        centre = {k: v["value"] for k, v in r.items()}
        centres.append(centre)

    return jsonify({"count": len(centres), "results": centres})

# === READ ONE ===
@centres_bp.route("/<centre_id>", methods=["GET"])
def get_centre(centre_id):
    centre_ref = EX[centre_id]
    query = PREFIX + f"SELECT ?p ?o WHERE {{ <{centre_ref}> ?p ?o . }}"
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = {}
    for r in results["results"]["bindings"]:
        key = r["p"]["value"].split('#')[-1]
        data[key] = r["o"]["value"]
    return jsonify(data)

# === UPDATE ===
@centres_bp.route("/<centre_id>", methods=["PUT"])
def update_centre(centre_id):
    data = request.json
    centre_ref = EX[centre_id]
    type_centre = data.get("type", "centre_de_recyclage")
    class_uri = CLASSES.get(type_centre, CLASSES["centre_de_recyclage"])

    # Suppression des anciens triplets
    delete_query = PREFIX + f"DELETE WHERE {{ <{centre_ref}> ?p ?o . }}"
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    # === Construction de la requête INSERT pour les nouveaux triplets ===
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{centre_ref}> a <{class_uri}> ;
            ex:centerName "{data.get('centerName','')}"^^xsd:string ;
            ex:capacity_center "{data.get('capacity_center','')}"^^xsd:string ;
            ex:energyConsumption "{data.get('energyConsumption','')}"^^xsd:string ;
            ex:location_center "{data.get('location_center','')}"^^xsd:string ;
            ex:typeDeDechetTraite "{data.get('typeDeDechetTraite','')}"^^xsd:string ;
            ex:operation_Status "{data.get('operation_Status','')}"^^xsd:string ;
            ex:recyclingRate "{data.get('recyclingRate','')}"^^xsd:string
    """

    # Ajout des attributs spécifiques selon le type
    if type_centre == "centre_de_compostage":
        insert_query += f' ; ex:tempsCompostage "{data.get("tempsCompostage","")}"^^xsd:string'
    elif type_centre == "centre_de_traitement_dangereux":
        insert_query += f' ; ex:equipementSpecialisee "{data.get("equipementSpecialisee","")}"^^xsd:string'
    elif type_centre == "usine_recyclage_metaux":
        insert_query += f' ; ex:equipmentRecyclagemetaux "{data.get("equipmentRecyclagemetaux","")}"^^xsd:string ; ex:typeDeMetauxTraites "{data.get("typeDeMetauxTraites","")}"^^xsd:string'

    insert_query += " . }"

    # === Exécution dans Fuseki ===
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # === Mise à jour locale RDFLib ===
    # Suppression des anciens triplets locaux
    for t in list(g.triples((centre_ref, None, None))):
        g.remove(t)

    # Ajout des nouveaux triplets locaux
    g.add((centre_ref, RDF.type, class_uri))
    g.add((centre_ref, EX.centerName, Literal(data.get("centerName",""))))
    g.add((centre_ref, EX.capacity_center, Literal(data.get("capacity_center",""))))
    g.add((centre_ref, EX.energyConsumption, Literal(data.get("energyConsumption",""))))
    g.add((centre_ref, EX.location_center, Literal(data.get("location_center",""))))
    g.add((centre_ref, EX.typeDeDechetTraite, Literal(data.get("typeDeDechetTraite",""))))
    g.add((centre_ref, EX.operation_Status, Literal(data.get("operation_Status",""))))
    g.add((centre_ref, EX.recyclingRate, Literal(data.get("recyclingRate",""))))

    # Champs spécifiques
    if type_centre == "centre_de_compostage":
        g.add((centre_ref, EX.tempsCompostage, Literal(data.get("tempsCompostage",""))))
    elif type_centre == "centre_de_traitement_dangereux":
        g.add((centre_ref, EX.equipementSpecialisee, Literal(data.get("equipementSpecialisee",""))))
    elif type_centre == "usine_recyclage_metaux":
        g.add((centre_ref, EX.equipmentRecyclagemetaux, Literal(data.get("equipmentRecyclagemetaux",""))))
        g.add((centre_ref, EX.typeDeMetauxTraites, Literal(data.get("typeDeMetauxTraites",""))))

    # Sauvegarde du graphe local
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Centre '{centre_id}' mis à jour avec succès."})

# === DELETE ===
@centres_bp.route("/<centre_id>", methods=["DELETE"])
def delete_centre(centre_id):
    centre_ref = EX[centre_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{centre_ref}> ?p ?o . }}"
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    # Suppression locale
    for t in list(g.triples((centre_ref, None, None))):
        g.remove(t)
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Centre '{centre_id}' supprimé avec succès."})


nlp_bp = Blueprint("nlp_bp", __name__)

# === Configuration ===
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


@centres_bp.route("/filtrage_nlp", methods=["POST"])
def filtrage_nlp():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Le prompt est vide"}), 400

    # 🔧 Nouveau prompt système plus strict
    system_prompt = (
        "Tu es un assistant spécialisé en SPARQL. "
        "Ton rôle est de convertir des phrases naturelles en requêtes SPARQL **valide et complète**. "
        "Ne donne **aucune explication**, seulement la requête. "
        "Utilise les préfixes suivants :\n"
        "PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>\n"
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\n"
        "Exemple :\n"
        "Phrase : Montre les centres avec un taux de recyclage supérieur à 70%\n"
        "Réponse :\n"
        "SELECT ?centre ?taux WHERE { ?centre ex:recyclingRate ?taux . FILTER(xsd:float(?taux) > 70) }"
    )

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
    )

    data = response.json()
    sparql_query = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

    if not sparql_query or not sparql_query.lower().startswith("select"):
        return jsonify({
            "error": "La requête générée n'est pas valide",
            "query": sparql_query
        }), 400

    # Exécution SPARQL
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
    except Exception as e:
        return jsonify({
            "error": f"Erreur SPARQL : {str(e)}",
            "query": sparql_query
        }), 500

    return jsonify({
        "query": sparql_query,
        "results": results["results"]["bindings"]
    })
