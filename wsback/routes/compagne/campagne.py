from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

campagne_bp = Blueprint("campagne_bp", __name__)

CAMPAGNE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/campagne_de_sensibilisation")


# ============================
# 🔹 CREATE Campagne
# ============================
@campagne_bp.route("/campagnes", methods=["POST"])
def add_campagne():
    data = request.json
    cid = data.get("campaignID", f"Campagne_{len(g) + 1}")
    camp_ref = EX[cid]

    # --- Insertion principale ---
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

    # --- Relation avec événements ---
    events = data.get("evenements", [])
    if events and isinstance(events, list):
        for evt_id in events:
            evt_ref = EX[evt_id]
            link_query = PREFIX + f"""
            INSERT DATA {{
                {camp_ref.n3()} ex:organise {evt_ref.n3()} .
                {evt_ref.n3()} ex:estOrganisePar {camp_ref.n3()} .
            }}
            """
            sparql.setQuery(link_query)
            sparql.setMethod(POST)
            sparql.query()

    return jsonify({"message": f"✅ Campagne '{cid}' ajoutée avec succès."})



# ============================
# 🔹 READ ALL Campagnes
# ============================
@campagne_bp.route("/campagnes", methods=["GET"])
def get_all_campagnes():
    # 1️⃣ Récupérer toutes les campagnes avec leurs propriétés
    query_props = PREFIX + """
    SELECT ?campagne ?descriptioncampa ?startDate ?endDate ?targetAudience ?title
    WHERE {
        ?campagne a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/campagne_de_sensibilisation> .
        OPTIONAL { ?campagne ex:descriptioncampa ?descriptioncampa }
        OPTIONAL { ?campagne ex:startDate ?startDate }
        OPTIONAL { ?campagne ex:endDate ?endDate }
        OPTIONAL { ?campagne ex:targetAudience ?targetAudience }
        OPTIONAL { ?campagne ex:title ?title }
    }
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query_props)
    sparql.setReturnFormat(JSON)
    results_props = sparql.query().convert()

    campagnes_dict = {}
    for r in results_props["results"]["bindings"]:
        camp_uri = r["campagne"]["value"]
        campagneID = camp_uri.split("#")[-1] if "#" in camp_uri else camp_uri.split("/")[-1]

        campagnes_dict[camp_uri] = {
            "campaignID": campagneID,  # 🔹 nom cohérent avec React
            "campagne": camp_uri,
            "descriptioncampa": r.get("descriptioncampa", {}).get("value"),
            "startDate": r.get("startDate", {}).get("value"),
            "endDate": r.get("endDate", {}).get("value"),
            "targetAudience": r.get("targetAudience", {}).get("value"),
            "title": r.get("title", {}).get("value"),
            "evenements": []
        }

    # 2️⃣ Pour chaque campagne, récupérer uniquement ses événements liés via la relation ex:planned
    for camp_uri, camp_data in campagnes_dict.items():
        camp_ref = f"<{camp_uri}>"
        query_events = PREFIX + f"""
        SELECT ?evenement ?nom ?dateDebut ?dateFin ?lieu ?descriptionevent
        WHERE {{
            {camp_ref} ex:planned ?evenement .  # La campagne planifie ces événements
            OPTIONAL {{ ?evenement ex:nomevent ?nom }}
            OPTIONAL {{ ?evenement ex:dateDebut ?dateDebut }}
            OPTIONAL {{ ?evenement ex:dateFin ?dateFin }}
            OPTIONAL {{ ?evenement ex:lieu ?lieu }}
            OPTIONAL {{ ?evenement ex:descriptionevent ?descriptionevent }}
        }}
        """
        sparql.setQuery(query_events)
        results_events = sparql.query().convert()

        evenements = []
        for r in results_events["results"]["bindings"]:
            evenements.append({
                "uri": r["evenement"]["value"],
                "nom": r.get("nom", {}).get("value"),
                "dateDebut": r.get("dateDebut", {}).get("value"),
                "dateFin": r.get("dateFin", {}).get("value"),
                "lieu": r.get("lieu", {}).get("value"),
                "descriptionevent": r.get("descriptionevent", {}).get("value")
            })

        camp_data["evenements"] = evenements

    return jsonify(list(campagnes_dict.values()))

@campagne_bp.route("/campagnes/<campagne_id>", methods=["GET"])
def get_campagne(campagne_id):
    camp_ref = EX[campagne_id]

    # 1️⃣ Récupérer les propriétés de la campagne
    query_props = PREFIX + f"""
    SELECT ?p ?o WHERE {{
        <{camp_ref}> ?p ?o . 
        FILTER(?p != ex:planned)  # On exclut les liens vers les événements ici
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query_props)
    sparql.setReturnFormat(JSON)
    results_props = sparql.query().convert()

    campagne = {}
    for r in results_props["results"]["bindings"]:
        key = r["p"]["value"].split("#")[-1]
        campagne[key] = r["o"]["value"]

    # 2️⃣ Récupérer les événements liés via la relation ex:planned
    query_events = PREFIX + f"""
    SELECT ?evenement ?nom ?dateDebut ?dateFin ?lieu ?descriptionevent
    WHERE {{
        <{camp_ref}> ex:planned ?evenement .  # La campagne planifie ces événements
        OPTIONAL {{ ?evenement ex:nomevent ?nom }}
        OPTIONAL {{ ?evenement ex:dateDebut ?dateDebut }}
        OPTIONAL {{ ?evenement ex:dateFin ?dateFin }}
        OPTIONAL {{ ?evenement ex:lieu ?lieu }}
        OPTIONAL {{ ?evenement ex:descriptionevent ?descriptionevent }}
    }}
    """
    sparql.setQuery(query_events)
    results_events = sparql.query().convert()

    evenements = []
    for r in results_events["results"]["bindings"]:
        evenements.append({
            "uri": r["evenement"]["value"],
            "nom": r.get("nom", {}).get("value"),
            "dateDebut": r.get("dateDebut", {}).get("value"),
            "dateFin": r.get("dateFin", {}).get("value"),
            "lieu": r.get("lieu", {}).get("value"),
            "descriptionevent": r.get("descriptionevent", {}).get("value")
        })

    # Ajouter les événements liés à la campagne dans la réponse
    if evenements:
        campagne["evenements"] = evenements

    campagne["id"] = campagne_id
    return jsonify(campagne)


# ============================
# 🔹 UPDATE Campagne
# ============================
@campagne_bp.route("/campagnes/<campagne_id>", methods=["PUT"])
def update_campagne(campagne_id):
    data = request.json
    camp_ref = EX[campagne_id]

    # Supprimer les anciens triples
    delete_query = PREFIX + f"""
    DELETE WHERE {{ <{camp_ref}> ?p ?o . }}
    """

    # Réinsertion complète des nouvelles valeurs
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{camp_ref}> a <{CAMPAGNE_CLASS_URI}> ;
            ex:title "{data.get('title', '')}"^^xsd:string ;
            ex:descriptioncampa "{data.get('descriptioncampa', '')}"^^xsd:string ;
            ex:contenu "{data.get('contenu', '')}"^^xsd:string ;
            ex:contenuimage "{data.get('contenuimage', '')}"^^xsd:string ;
            ex:image "{data.get('image', '')}"^^xsd:string ;
            ex:lien "{data.get('lien', '')}"^^xsd:string ;
            ex:nomPlateforme "{data.get('nomPlateforme', '')}"^^xsd:string ;
            ex:startDate "{data.get('startDate', '')}"^^xsd:date ;
            ex:endDate "{data.get('endDate', '')}"^^xsd:date ;
            ex:targetAudience "{data.get('targetAudience', '')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)

    # Suppression des anciens triples
    sparql.setQuery(delete_query)
    sparql.query()

    # Insertion des nouveaux
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"✅ Campagne '{campagne_id}' mise à jour avec succès."})

# ============================
# 🔹 GET Événements par Campagne
# ============================
@campagne_bp.route("/campagnes/<campagne_id>/evenements", methods=["GET"])
def get_evenements_by_campagne(campagne_id):
    # Construire la référence de la campagne dans l'URI
    camp_ref = f"<http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#{campagne_id}>"

    # Requête SPARQL avec les détails de l'événement pour la campagne spécifique
    query = f"""
    PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>

    SELECT 
      (STRAFTER(STR(?evenement), "#") AS ?evenementID)
      ?dateDebut
      ?dateFin
      ?descriptionevent
      ?lieu
      ?nomevent
      ?typeEvenement
      ?nombreBenevoles
      ?quantitecollecte
      ?nombreParticipants
      ?publicCible
      ?zoneCible
    WHERE {{
      ?evenement ex:planned {camp_ref} .
      ?evenement ex:dateDebut ?dateDebut .
      ?evenement ex:dateFin ?dateFin .
      ?evenement ex:descriptionevent ?descriptionevent .
      ?evenement ex:lieu ?lieu .
      ?evenement ex:nomevent ?nomevent .
      ?evenement ex:typeEvenement ?typeEvenement .
      ?evenement ex:nombreBenevoles ?nombreBenevoles .
      ?evenement ex:quantitecollecte ?quantitecollecte .
      ?evenement ex:nombreParticipants ?nombreParticipants .
      ?evenement ex:publicCible ?publicCible .
      ?evenement ex:zoneCible ?zoneCible .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    evenements = []
    for result in results["results"]["bindings"]:
        evenement = {k: v["value"] for k, v in result.items()}
        evenements.append(evenement)

    return jsonify(evenements)
# ============================
# 🔹 Associer un événement à une campagne
# ============================
@campagne_bp.route("/campagnes/<campagne_id>/associer_evenement/<evenement_id>", methods=["POST"])
def associer_evenement(campagne_id, evenement_id):
    # Obtenez les références de la campagne et de l'événement
    camp_ref = EX[campagne_id]
    evt_ref = EX[evenement_id]

    # Créer la requête SPARQL pour établir la relation
    link_query = PREFIX + f"""
    INSERT DATA {{
        {camp_ref.n3()} ex:planned {evt_ref.n3()} .  # La campagne planifie cet événement
        {evt_ref.n3()} ex:plannedby {camp_ref.n3()} .  # L'événement est planifié par cette campagne
    }}
    """

    # Effectuer la requête SPARQL pour insérer la relation
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(link_query)
    sparql.setMethod(POST)
    sparql.query()

    return jsonify({"message": f"✅ L'événement '{evenement_id}' a été associé à la campagne '{campagne_id}' avec succès."})


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
