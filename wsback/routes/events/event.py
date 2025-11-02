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

    # Générer un ID unique pour l'événement (ex: "E" + nombre d'événements dans le graph)
    evenement_id = "E" + str(len(g) + 1)
    evt_ref = EX[evenement_id]

    # --- Ajouter dans Fuseki ---
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
            ex:zoneCible "{data.get('zoneCible','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.method = 'POST'
    sparql.query()

    # --- Ajouter dans rdflib local ---
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

    # Sauvegarder RDF local
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Événement '{evenement_id}' ajouté dans Fuseki et Protégé !"})

# --- READ ALL ---
@evenement_bp.route("/evenements", methods=["GET"])
def get_evenements_fuseki():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?evenement ?nomevent ?dateDebut ?dateFin ?lieu ?descriptionevent ?typeEvenement
               ?nombreBenevoles ?quantitecollecte ?nombreParticipants ?publicCible ?zoneCible
        WHERE {
            ?evenement a ex:evenement .
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
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    events = []
    for result in results["results"]["bindings"]:
        event_data = {k: v["value"] for k, v in result.items()}
        events.append(event_data)

    return jsonify(events)

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
        # prendre seulement le fragment après #
        key = r["p"]["value"].split('#')[-1]
        data[key] = r["o"]["value"]

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
