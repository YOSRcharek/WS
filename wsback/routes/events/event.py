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
            {"; ex:partOf " + camp_ref.n3() if camp_ref else ""} .
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
        g.add((evt_ref, EX.partOf, camp_ref))
        # Optionnel : lier la campagne à cet événement
        g.add((camp_ref, EX.hasEvent, evt_ref))

    # Sauvegarder RDF local
    g.serialize(destination=RDF_FILE, format="turtle")

    msg = f"✅ Événement '{evenement_id}' ajouté avec succès."
    if campaign_id:
        msg += f" Lié à la campagne '{campaign_id}'."

    return jsonify({"message": msg})

# --- READ ALL ---
@evenement_bp.route("/evenements", methods=["GET"])
def get_evenements_fuseki():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)

    sparql.setQuery("""
        PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#>
        SELECT ?evenement ?nomevent ?dateDebut ?dateFin ?lieu ?descriptionevent ?typeEvenement
               ?nombreBenevoles ?quantitecollecte ?nombreParticipants ?publicCible ?zoneCible ?campaign
        WHERE {
            ?evenement a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement> .
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
            OPTIONAL { ?evenement ex:partOf ?campaign }
        }
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    events = []
    for result in results["results"]["bindings"]:
        event_data = {}
        for k, v in result.items():
            if k == "evenement":
                event_data["evenementID"] = v["value"].split('#')[-1]  # ✅ Ajouté ici
            if k == "campaign":
                event_data["campaignID"] = v["value"].split('#')[-1]
            else:
                event_data[k] = v["value"]
        events.append(event_data)

    return jsonify({
        "status": "success",
        "count": len(events),
        "results": events
    })

# --- READ ONE ---
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
        if key == "partOf":  # ✅ campagne
            data["campaignID"] = value.split('#')[-1]
        else:
            data[key] = value

    return jsonify(data)


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