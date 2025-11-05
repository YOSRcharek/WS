# wsback/routes/camion_benne.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, g, EX, RDF_FILE
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD

def get_service_type_and_id(service_id):
    """Détermine le type de service basé sur l'ID"""
    try:
        # Vérifier si le service existe comme entité directe
        query = f"""
        {PREFIX}
        SELECT ?type WHERE {{
            ex:{service_id} rdf:type ?type .
        }}
        """
        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        if results["results"]["bindings"]:
            for result in results["results"]["bindings"]:
                service_type = result["type"]["value"].split('#')[-1]
                if service_type == 'CamionDechets':
                    return f"Camion Déchets - {service_id}"
                elif service_type == 'TransportDechetsDangereux':
                    return f"Transport Dangereux - {service_id}"
        
        # Logique basée sur le préfixe de l'ID
        if service_id.upper().startswith('CD'):
            return f"Camion Déchets - {service_id}"
        elif service_id.upper().startswith('TDD'):
            return f"Transport Dangereux - {service_id}"
        
        return f"Service - {service_id}"
    except Exception as e:
        print(f"Erreur recherche service: {e}")
        return f"Service - {service_id}"

camion_benne_bp = Blueprint('camion_benne_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau camion benne
@camion_benne_bp.route('/camions-benne', methods=['POST'])
def create_camion_benne():
    data = request.json
    import time
    camion_id = f"CB{int(time.time() * 1000) % 100000}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} a ex:CamionBenne, ex:Equipement ;
            ex:equipementID "{camion_id}"^^xsd:string ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', 'disponible')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:volumeBenne "{data.get('volumeBenne', 0)}"^^xsd:decimal .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    # --- Ajout dans le graphe RDF local ---
    camion_ref = EX[camion_id]
    g.add((camion_ref, RDF.type, EX.CamionBenne))
    g.add((camion_ref, RDF.type, EX.Equipement))
    g.add((camion_ref, EX.equipementID, Literal(camion_id, datatype=XSD.string)))
    g.add((camion_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.etat, Literal(data.get('etat', 'disponible'), datatype=XSD.string)))
    g.add((camion_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((camion_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.volumeBenne, Literal(data.get('volumeBenne', 0), datatype=XSD.decimal)))
    
    # Assigner le service si fourni
    service_id = data.get('serviceId')
    if service_id:
        assign_query = f"""
        {SPARQL_PREFIX}
        INSERT DATA {{
            ex:{camion_id} ex:utilisepar ex:{service_id} .
        }}
        """
        sparql.setQuery(assign_query)
        sparql.query()
        
        # Ajout de la relation dans le graphe local
        g.add((camion_ref, EX.utilisepar, EX[service_id]))
    
    # Sauvegarder le fichier TTL
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Camion benne créé avec succès", "id": camion_id}), 201

# Récupérer tous les camions benne
@camion_benne_bp.route('/camions-benne', methods=['GET'])
def get_camions_benne():
    query = f"""
    {SPARQL_PREFIX}
    SELECT DISTINCT ?equipementID ?nomequiement ?etat ?capacite ?localisation ?volumeBenne ?service
    WHERE {{
        ?camion a ex:CamionBenne ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomequiement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:volumeBenne ?volumeBenne .
        OPTIONAL {{
            ?camion ex:utilisepar ?service .
        }}
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    camions = []
    seen_ids = set()
    for result in results["results"]["bindings"]:
        camion_id = result["equipementID"]["value"]
        if camion_id not in seen_ids:
            seen_ids.add(camion_id)
            camions.append({
                "id": camion_id,
                "nomEquipement": result["nomequiement"]["value"],
                "etat": result["etat"]["value"],
                "capacite": result["capacite"]["value"],
                "localisation": result["localisation"]["value"],
                "volumeBenne": result["volumeBenne"]["value"],
                "serviceAssigne": (
                    get_service_type_and_id(result['service']['value'].split('#')[-1]) 
                    if "service" in result and result["service"] 
                    else "Aucun"
                )
            })
    
    return jsonify(camions)

# Récupérer un camion benne par ID
@camion_benne_bp.route('/camions-benne/<camion_id>', methods=['GET'])
def get_camion_benne(camion_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?camion ?equipementID ?nomequiement ?etat ?capacite ?localisation ?volumeBenne
    WHERE {{
        ?camion a ex:CamionBenne ;
                ex:equipementID "{camion_id}" ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomequiement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:volumeBenne ?volumeBenne .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        camion = {
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomequiement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "volumeBenne": result["volumeBenne"]["value"]
        }
        return jsonify(camion)
    
    return jsonify({"message": "Camion benne non trouvé"}), 404

# Mettre à jour un camion benne
@camion_benne_bp.route('/camions-benne/<camion_id>', methods=['PUT'])
def update_camion_benne(camion_id):
    data = request.json
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    
    # Supprimer l'entité
    delete_query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{ ex:{camion_id} ?p ?o }}
    """
    sparql.setQuery(delete_query)
    sparql.query()
    
    # Recréer l'entité
    insert_query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} a ex:CamionBenne, ex:Equipement ;
            ex:equipementID "{camion_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', '')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:volumeBenne "{data.get('volumeBenne', 0)}"^^xsd:decimal .
    }}
    """
    sparql.setQuery(insert_query)
    sparql.query()
    
    # --- Mise à jour dans le graphe RDF local ---
    camion_ref = EX[camion_id]
    # Supprimer les anciens triplets
    for triple in list(g.triples((camion_ref, None, None))):
        g.remove(triple)
    
    # Ajouter les nouveaux triplets
    g.add((camion_ref, RDF.type, EX.CamionBenne))
    g.add((camion_ref, RDF.type, EX.Equipement))
    g.add((camion_ref, EX.equipementID, Literal(camion_id, datatype=XSD.string)))
    g.add((camion_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.etat, Literal(data.get('etat', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((camion_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.volumeBenne, Literal(data.get('volumeBenne', 0), datatype=XSD.decimal)))
    
    # Sauvegarder le fichier TTL
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Camion benne mis à jour avec succès"})

# Supprimer un camion benne
@camion_benne_bp.route('/camions-benne/<camion_id>', methods=['DELETE'])
def delete_camion_benne(camion_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?camion a ex:CamionBenne ;
                ex:equipementID "{camion_id}" ;
                ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    # --- Suppression dans le graphe RDF local ---
    camion_ref = EX[camion_id]
    for triple in list(g.triples((camion_ref, None, None))):
        g.remove(triple)
    
    # Sauvegarder le fichier TTL
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Camion benne supprimé avec succès"})

# Assigner un camion à un service
@camion_benne_bp.route('/camions-benne/<camion_id>/assigner-service', methods=['POST'])
def assigner_service_camion(camion_id):
    data = request.json
    service_id = data.get('serviceId')
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} ex:utilisepar ex:{service_id} .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    # --- Ajout de la relation dans le graphe RDF local ---
    camion_ref = EX[camion_id]
    service_ref = EX[service_id]
    g.add((camion_ref, EX.utilisepar, service_ref))
    
    # Sauvegarder le fichier TTL
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Service assigné avec succès"})
