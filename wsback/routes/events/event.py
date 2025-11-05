from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, GET, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, RDF_FILE, FUSEKI_QUERY_URL

evenement_bp = Blueprint("evenement_bp", __name__)
EVENEMENT_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement")


# --- CREATE ---
@evenement_bp.route("/evenements", methods=["POST"])
def add_evenement():
    data = request.json

    # Générer un ID unique pour l'événement
    evenement_id = "E" + str(len(g) + 1)
    evt_ref = EX[evenement_id]

    # Si une campagne est fournie
    campaign_id = data.get("campagneID")  # ✅ corrigé pour correspondre au JSON
    camp_ref = EX[campaign_id] if campaign_id else None

    # --- Insertion dans Fuseki ---
    insert_query = PREFIX + f"""
    INSERT DATA {{
        {evt_ref.n3()} a <{EVENEMENT_CLASS_URI}> ;
            ex:evenementID "{evenement_id}"^^xsd:string ;
            ex:dateDebut "{data.get('dateDebut','')}"^^xsd:date ;
            ex:dateFin "{data.get('dateFin','')}"^^xsd:date ;
            ex:descriptionevent "{data.get('descriptionevent','')}"^^xsd:string ;
            ex:lieu "{data.get('lieu','')}"^^xsd:string ;
            ex:nomevent "{data.get('nomevent','')}"^^xsd:string ;
            ex:typeEvenement "{data.get('typeEvenement','')}"^^xsd:string ;
            ex:nombreBenevoles "{data.get('nombreBenevoles',0)}"^^xsd:integer ;
            ex:quantitecollecte "{data.get('quantitecollecte',0)}"^^xsd:decimal ;
            ex:nombreParticipants "{data.get('nombreParticipants',0)}"^^xsd:integer ;
            ex:publicCible "{data.get('publicCible','')}"^^xsd:string ;
            ex:zoneCible "{data.get('zoneCible','')}"^^xsd:string
<<<<<<< HEAD
            {"; ex:planned " + camp_ref.n3() if camp_ref else ""} ;  # Utilisation de ex:planned
=======
            {"; ex:partOf " + camp_ref.n3() if camp_ref else ""} .
>>>>>>> doua
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.setMethod(POST)
    sparql.query()

    # --- Ajout dans RDF local ---
    g.add((evt_ref, RDF.type, EVENEMENT_CLASS_URI))
    g.add((evt_ref, EX.evenementID, Literal(evenement_id, datatype=XSD.string)))
    g.add((evt_ref, EX.dateDebut, Literal(data.get('dateDebut',''), datatype=XSD.date)))
    g.add((evt_ref, EX.dateFin, Literal(data.get('dateFin',''), datatype=XSD.date)))
    g.add((evt_ref, EX.descriptionevent, Literal(data.get('descriptionevent',''))))
    g.add((evt_ref, EX.lieu, Literal(data.get('lieu',''))))
    g.add((evt_ref, EX.nomevent, Literal(data.get('nomevent',''))))
    g.add((evt_ref, EX.typeEvenement, Literal(data.get('typeEvenement',''))))
    g.add((evt_ref, EX.nombreBenevoles, Literal(data.get('nombreBenevoles',0), datatype=XSD.integer)))
    g.add((evt_ref, EX.quantitecollecte, Literal(data.get('quantitecollecte',0), datatype=XSD.decimal)))
    g.add((evt_ref, EX.nombreParticipants, Literal(data.get('nombreParticipants',0), datatype=XSD.integer)))
    g.add((evt_ref, EX.publicCible, Literal(data.get('publicCible',''))))
    g.add((evt_ref, EX.zoneCible, Literal(data.get('zoneCible',''))))

    # Lier à la campagne localement
    if camp_ref:
<<<<<<< HEAD
        g.add((evt_ref, EX.planned, camp_ref))  # Lier l'événement à la campagne avec ex:planned
        print(f"Événement {evenement_id} lié à la campagne {campaign_id}.")  # Log pour vérifier que la relation est ajoutée
=======
        g.add((evt_ref, EX.partOf, camp_ref))
        # Optionnel : lier la campagne à cet événement
        g.add((camp_ref, EX.hasEvent, evt_ref))
>>>>>>> doua

    # Sauvegarder RDF local
    g.serialize(destination=RDF_FILE, format="turtle")

    msg = f"✅ Événement '{evenement_id}' ajouté avec succès."
    if campaign_id:
        msg += f" Lié à la campagne '{campaign_id}'."

    return jsonify({"message": msg})

# --- READ ALL ---
<<<<<<< HEAD
# --- READ ALL (Liste des événements) ---
=======
>>>>>>> doua
@evenement_bp.route("/evenements", methods=["GET"])
def get_evenements_fuseki():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)

    sparql.setQuery("""
        PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>
        SELECT ?evenement ?nomevent ?dateDebut ?dateFin ?lieu ?descriptionevent ?typeEvenement
               ?nombreBenevoles ?quantitecollecte ?nombreParticipants ?publicCible ?zoneCible ?campaign
        WHERE {
<<<<<<< HEAD
            ?evenement a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement> . 
=======
            ?evenement a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement> .
>>>>>>> doua
            OPTIONAL { ?evenement ex:nomevent ?nomevent }
            OPTIONAL { ?evenement ex:dateDebut ?dateDebut }
            OPTIONAL { ?evenement ex:dateFin ?dateFin }
            OPTIONAL { ?evenement ex:lieu ?lieu }
            OPTIONAL { ?evenement ex:descriptionevent ?descriptionevent }
            OPTIONAL { ?evenement ex:typeEvenement ?typeEvenement }
            OPTIONAL { ?evenement ex:nombreBenevoles ?nombreBenevoles }
            OPTIONAL { ?evenement ex:quantitecollecte ?quantitecollecte }
            OPTIONAL { ?evenement ex:nombreParticipants ?nombreParticipants }
            OPTIONAL { ?evenement ex:publicCible ?publicCible }
            OPTIONAL { ?evenement ex:zoneCible ?zoneCible }
<<<<<<< HEAD
            OPTIONAL { ?evenement ex:plannedBy ?campaign }  # Utilisation de ex:plannedBy
=======
            OPTIONAL { ?evenement ex:partOf ?campaign }
>>>>>>> doua
        }
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

<<<<<<< HEAD
    # Utilisation d'un dictionnaire pour éviter les doublons par evenementID
    events_dict = {}

=======
    events = []
>>>>>>> doua
    for result in results["results"]["bindings"]:
        event_data = {}
        for k, v in result.items():
            if k == "evenement":
<<<<<<< HEAD
                evenementID = v["value"].split('#')[-1]
                event_data["evenementID"] = evenementID  # ID unique de l'événement
            if k == "campaign":
                event_data["campaignID"] = v["value"].split('#')[-1]  # Campaign associé
            else:
                event_data[k] = v["value"]

        # Ajouter l'événement au dictionnaire en utilisant l'ID comme clé pour éviter la duplication
        events_dict[evenementID] = event_data

    # Convertir le dictionnaire en liste
    events = list(events_dict.values())
=======
                event_data["evenementID"] = v["value"].split('#')[-1]  # ✅ Ajouté ici
            if k == "campaign":
                event_data["campaignID"] = v["value"].split('#')[-1]
            else:
                event_data[k] = v["value"]
        events.append(event_data)
>>>>>>> doua

    return jsonify({
        "status": "success",
        "count": len(events),
        "results": events
    })

<<<<<<< HEAD
# --- READ ONE (Détails d'un événement) ---
=======
# --- READ ONE ---
>>>>>>> doua
@evenement_bp.route("/evenements/<evenement_id>", methods=["GET"])
def get_evenement(evenement_id):
    evt_ref = EX[evenement_id]
    query = PREFIX + f"""
    SELECT ?p ?o WHERE {{
        <{evt_ref}> ?p ?o .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = {}
    for r in results["results"]["bindings"]:
        key = r["p"]["value"].split('#')[-1]
        value = r["o"]["value"]
<<<<<<< HEAD
        if key == "plannedBy":  # ✅ campaign (relation plannedBy)
=======
        if key == "partOf":  # ✅ campagne
>>>>>>> doua
            data["campaignID"] = value.split('#')[-1]
        else:
            data[key] = value

    return jsonify(data)

<<<<<<< HEAD
# --- READ ONE (Détails d'un événement avec ID) ---
@evenement_bp.route("/evenements/<evenement_id>/details", methods=["GET"])
def get_evenement_details(evenement_id):
    evt_ref = EX[evenement_id]
    query = PREFIX + f"""
    SELECT ?p ?o WHERE {{
        <{evt_ref}> ?p ?o .
        FILTER(?p != ex:plannedBy)  # Exclure la relation 'plannedBy'
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = {}
    for r in results["results"]["bindings"]:
        key = r["p"]["value"].split('#')[-1]
        value = r["o"]["value"]
        if key == "plannedBy":  # ✅ Campaign associated
            data["campaignID"] = value.split('#')[-1]
        else:
            data[key] = value

    return jsonify(data)

# --- GET --- Récupérer la campagne associée à un événement spécifique
@evenement_bp.route("/evenements/<evenement_id>/campagne", methods=["GET"])
def get_campagne_by_evenement(evenement_id):
    # Créer la référence RDF de l'événement
    evt_ref = EX[evenement_id]
    
    # Requête SPARQL pour obtenir l'ID et le nom (title) de la campagne associée
    query = PREFIX + f"""
    SELECT 
        (STRAFTER(STR(?campagne), "#") AS ?campagneID)
        ?title
    WHERE {{
        ?evenement ex:planned ?campagne .  
        ?campagne ex:title ?title .  # Ajout du nom de la campagne
        FILTER(STRAFTER(STR(?evenement), "#") = "{evenement_id}")
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        
        # Vérifier si une campagne a été trouvée
        if results["results"]["bindings"]:
            campagne_id = results["results"]["bindings"][0]["campagneID"]["value"]
            campagne_title = results["results"]["bindings"][0]["title"]["value"]
            return jsonify({"campagne_id": campagne_id, "campagne_title": campagne_title})
        else:
            return jsonify({"error": "Aucune campagne associée à cet événement."}), 404
    
    except Exception as e:
        print(f"Erreur lors de la requête SPARQL: {e}")
        return jsonify({"error": "Erreur de serveur."}), 500
=======
>>>>>>> doua

# --- UPDATE ---
@evenement_bp.route("/evenements/<evenement_id>", methods=["PUT"])
def update_evenement(evenement_id):
    data = request.json
    evt_ref = EX[evenement_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{evt_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{evt_ref}> a <{EVENEMENT_CLASS_URI}> ;
            ex:dateDebut "{data.get('dateDebut','')}"^^xsd:date ;
            ex:dateFin "{data.get('dateFin','')}"^^xsd:date ;
            ex:descriptionevent "{data.get('descriptionevent','')}"^^xsd:string ;
            ex:lieu "{data.get('lieu','')}"^^xsd:string ;
            ex:nomevent "{data.get('nomevent','')}"^^xsd:string ;
            ex:typeEvenement "{data.get('typeEvenement','')}"^^xsd:string ;
            ex:nombreBenevoles "{data.get('nombreBenevoles',0)}"^^xsd:integer ;
            ex:quantitecollecte "{data.get('quantitecollecte',0)}"^^xsd:decimal ;
            ex:nombreParticipants "{data.get('nombreParticipants',0)}"^^xsd:integer ;
            ex:publicCible "{data.get('publicCible','')}"^^xsd:string ;
            ex:zoneCible "{data.get('zoneCible','')}"^^xsd:string .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()
    return jsonify({"message": f"Événement '{evenement_id}' mis à jour."})

<<<<<<< HEAD
@evenement_bp.route("/evenements/<evenement_id>/associer-citoyen/<citoyen_id>", methods=["POST"])
def associer_citoyen_a_evenement(evenement_id, citoyen_id):
    # Créer l'URI du citoyen et de l'événement
    citoyen_uri = f"http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/citoyen#{citoyen_id}"
    evenement_uri = f"http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement#{evenement_id}"

    # Requête SPARQL pour ajouter la relation Participe
    insert_query = f"""
    PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>

    INSERT DATA {{
        <{citoyen_uri}> ex:participe <{evenement_uri}> .
    }}
    """

    # Exécution de la requête SPARQL
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)  # URL de votre endpoint SPARQL
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)

    try:
        sparql.query()  # Exécution de la requête
        return jsonify({"message": f"✅ Citoyen '{citoyen_id}' associé à l'événement '{evenement_id}' avec succès !"})
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")
        return jsonify({"error": "Erreur serveur."}), 500
    

@evenement_bp.route("/evenements/<evenement_id>/participants", methods=["GET"])
def get_participants_by_evenement(evenement_id):
    # Créer l'URI de l'événement
    evenement_uri = f"http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement#{evenement_id}"

    # Formuler la requête SPARQL pour obtenir les citoyens associés à l'événement
    query = PREFIX + f"""
    SELECT 
        ?citoyen 
        (STRAFTER(STR(?citoyen), "#") AS ?citizenID)  # Extraction de l'ID du citoyen depuis l'URI
        ?neaemcitoyen 
        ?addresscit 
        ?age 
        ?email 
        ?phoneNumber
    WHERE {{
        ?citoyen ex:participe <{evenement_uri}> .  # URI de l'événement
        OPTIONAL {{ ?citoyen ex:neaemcitoyen ?neaemcitoyen . }}
        OPTIONAL {{ ?citoyen ex:addresscit ?addresscit . }}
        OPTIONAL {{ ?citoyen ex:age ?age . }}
        OPTIONAL {{ ?citoyen ex:email ?email . }}
        OPTIONAL {{ ?citoyen ex:phoneNumber ?phoneNumber . }}
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()

        # Vérifier si des citoyens ont été trouvés
        if results["results"]["bindings"]:
            participants = []
            for result in results["results"]["bindings"]:
                # Récupérer le citizenID
                citizen_id = result.get("citizenID", {}).get("value", "Inconnu")

                # Appeler la fonction pour obtenir les détails du citoyen
                citoyen_details = get_citoyen_by_id(citizen_id)

                # Ajouter les détails du citoyen aux participants
                participant = {
                    "citizenID": citizen_id,
                    "namecitoyen": citoyen_details.get("neaemcitoyen", "Inconnu"),
                    "addresscit": citoyen_details.get("addresscit", "Inconnu"),
                    "age": citoyen_details.get("age", "Inconnu"),
                    "email": citoyen_details.get("email", "Inconnu"),
                    "phoneNumber": citoyen_details.get("phoneNumber", "Inconnu")
                }

                participants.append(participant)

            return jsonify({"message": f"Participants de l'événement '{evenement_id}'", "participants": participants})
        else:
            return jsonify({"message": f"Aucun citoyen n'a participé à l'événement '{evenement_id}'."}), 404

    except Exception as e:
        print(f"Erreur lors de la requête SPARQL: {e}")
        return jsonify({"error": "Erreur de serveur."}), 500
def get_citoyen_by_id(citizen_id):
    query = PREFIX + f"""
    SELECT ?citoyen ?citizenID ?namecitoyen ?addresscit ?age ?email ?phoneNumber
    WHERE {{
        ?citoyen ex:citizenID "{citizen_id}"^^xsd:string .  # Assurez-vous que le citizenID correspond exactement
        OPTIONAL {{ ?citoyen ex:namecitoyen ?namecitoyen . }}
        OPTIONAL {{ ?citoyen ex:addresscit ?addresscit . }}
        OPTIONAL {{ ?citoyen ex:age ?age . }}
        OPTIONAL {{ ?citoyen ex:email ?email . }}
        OPTIONAL {{ ?citoyen ex:phoneNumber ?phoneNumber . }}
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()

        # Vérifier si des résultats ont été trouvés
        if results["results"]["bindings"]:
            r = results["results"]["bindings"][0]
            citoyen = {
                "citizenID": citizen_id,
                "namecitoyen": r.get("namecitoyen", {}).get("value", "Inconnu"),
                "addresscit": r.get("addresscit", {}).get("value", "Inconnu"),
                "age": r.get("age", {}).get("value", "Inconnu"),
                "email": r.get("email", {}).get("value", "Inconnu"),
                "phoneNumber": r.get("phoneNumber", {}).get("value", "Inconnu")
            }
            return citoyen
        else:
            return {"message": f"Citoyen '{citizen_id}' non trouvé"}

    except Exception as e:
        print(f"Erreur lors de la requête SPARQL: {e}")
        return {"error": "Erreur de serveur."}

=======
>>>>>>> doua
# --- DELETE ---
@evenement_bp.route("/evenements/<evenement_id>", methods=["DELETE"])
def delete_evenement(evenement_id):
    # --- Créer la référence RDF de l'événement ---
    evt_ref = EX[evenement_id]

    # --- Supprimer dans Fuseki ---
    delete_query = PREFIX + f"""
    DELETE WHERE {{
        <{evt_ref}> ?p ?o .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    # --- Supprimer du graphe rdflib local ---
    triplets_to_remove = list(g.triples((evt_ref, None, None)))
    for t in triplets_to_remove:
        g.remove(t)

    # --- Sauvegarder le fichier Turtle ---
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Événement '{evenement_id}' supprimé avec succès."})

<<<<<<< HEAD
@evenement_bp.route("/citoyens", methods=["GET"])
def get_all_citoyens():
    query = PREFIX + """
    SELECT ?citoyen ?citizenID ?neaemcitoyen ?addresscit ?age ?email ?phoneNumber
    WHERE {
        ?citoyen a ex:Citoyen .  # Assurez-vous que la classe est correcte ici
        OPTIONAL { ?citoyen ex:citizenID ?citizenID . }
        OPTIONAL { ?citoyen ex:neaemcitoyen ?neaemcitoyen . }
        OPTIONAL { ?citoyen ex:addresscit ?addresscit . }
        OPTIONAL { ?citoyen ex:age ?age . }
        OPTIONAL { ?citoyen ex:email ?email . }
        OPTIONAL { ?citoyen ex:phoneNumber ?phoneNumber . }
    }
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        citoyens = []
        
        for result in results["results"]["bindings"]:
            citoyens.append({
                "uri": result.get("citoyen", {}).get("value"),
                "citizenID": result.get("citizenID", {}).get("value", "Inconnu"),
                "neaemcitoyen": result.get("neaemcitoyen", {}).get("value", "Inconnu"),
                "addresscit": result.get("addresscit", {}).get("value", "Inconnu"),
                "age": result.get("age", {}).get("value", "Inconnu"),
                "email": result.get("email", {}).get("value", "Inconnu"),
                "phoneNumber": result.get("phoneNumber", {}).get("value", "Inconnu")
            })

        # Vérifier si la liste est vide et renvoyer un message si nécessaire
        if not citoyens:
            return jsonify({"message": "Aucun citoyen trouvé"}), 404

        return jsonify(citoyens)

    except Exception as e:
        print(f"Erreur lors de la requête SPARQL: {e}")
        return jsonify({"error": "Erreur de serveur."}), 500

=======
>>>>>>> doua
@evenement_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():
    try:
        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setReturnFormat(JSON)

        # 🟢 1️⃣ Nombre total d'événements
        sparql.setQuery(f"""
            {PREFIX}
            SELECT (COUNT(?evenement) AS ?count)
            WHERE {{ ?evenement a ex:evenement . }}
        """)
        total_events = int(sparql.query().convert()["results"]["bindings"][0]["count"]["value"])

        # 🟢 2️⃣ Nombre total de campagnes
        sparql.setQuery(f"""
            {PREFIX}
            SELECT (COUNT(?campagne) AS ?count)
            WHERE {{ ?campagne a ex:campagne_de_sensibilisation . }}
        """)
        total_campagnes = int(sparql.query().convert()["results"]["bindings"][0]["count"]["value"])

        # 🟢 3️⃣ Statistiques par type d’événement
        sparql.setQuery(f"""
            {PREFIX}
            SELECT ?typeEvenement (COUNT(?evenement) AS ?count)
            WHERE {{ ?evenement a ex:evenement ; ex:typeEvenement ?typeEvenement . }}
            GROUP BY ?typeEvenement
        """)
        results = sparql.query().convert()["results"]["bindings"]
        types_evenements = [
            {
                "label": r["typeEvenement"]["value"].split("#")[-1],
                "count": int(r["count"]["value"])
            }
            for r in results
        ]

        # 🟢 4️⃣ Valeurs simulées (à remplacer si tu as des propriétés réelles)
        total_participants = 8547
        satisfaction_rate = 96
        participation_par_mois = [
            {"month": "Janvier", "value": 1200},
            {"month": "Février", "value": 1580},
            {"month": "Mars", "value": 2100},
        ]
        impact_environnemental = {
            "dechets_collectes": "12.5 tonnes",
            "co2_evite": "8.2 tonnes",
            "arbres_sauves": 340
        }

        return jsonify({
            "total_evenements": total_events,
            "total_participants": total_participants,
            "total_campagnes": total_campagnes,
            "satisfaction_rate": satisfaction_rate,
            "participation_par_mois": participation_par_mois,
            "types_evenements": types_evenements,
            "impact_environnemental": impact_environnemental
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500