# wsback/routes/service_transport.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

service_transport_bp = Blueprint('service_transport_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau service de transport
@service_transport_bp.route('/services-transport', methods=['POST'])
def create_service_transport():
    data = request.json
    service_id = f"ST{len(data) + 1}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{service_id} a ex:ServiceTransport ;
            ex:serviceID "{service_id}" ;
            ex:nomService "{data.get('nomService', '')}" ;
            ex:typeService "{data.get('typeService', '')}" ;
            ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
            ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
            ex:estActif "{data.get('estActif', 'true')}"^^xsd:boolean .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Service de transport créé avec succès", "id": service_id}), 201

# Récupérer tous les services de transport
@service_transport_bp.route('/services-transport', methods=['GET'])
def get_services_transport():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?service ?serviceID ?nomService ?typeService ?zoneCouverture ?capaciteMax ?estActif
    WHERE {{
        ?service a ex:ServiceTransport ;
                ex:serviceID ?serviceID ;
                ex:nomService ?nomService ;
                ex:typeService ?typeService ;
                ex:zoneCouverture ?zoneCouverture ;
                ex:capaciteMax ?capaciteMax ;
                ex:estActif ?estActif .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    services = []
    for result in results["results"]["bindings"]:
        services.append({
            "id": result["serviceID"]["value"],
            "nomService": result["nomService"]["value"],
            "typeService": result["typeService"]["value"],
            "zoneCouverture": result["zoneCouverture"]["value"],
            "capaciteMax": result["capaciteMax"]["value"],
            "estActif": result["estActif"]["value"]
        })
    
    return jsonify(services)

# Mettre à jour un service de transport
@service_transport_bp.route('/services-transport/<service_id>', methods=['PUT'])
def update_service_transport(service_id):
    data = request.json
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?service ex:nomService ?oldNom ;
                ex:typeService ?oldType ;
                ex:zoneCouverture ?oldZone ;
                ex:capaciteMax ?oldCapacite ;
                ex:estActif ?oldActif .
    }}
    INSERT {{
        ?service ex:nomService "{data.get('nomService', '')}" ;
                ex:typeService "{data.get('typeService', '')}" ;
                ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
                ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
                ex:estActif "{data.get('estActif', 'true')}"^^xsd:boolean .
    }}
    WHERE {{
        ?service a ex:ServiceTransport ;
                ex:serviceID "{service_id}" ;
                ex:nomService ?oldNom ;
                ex:typeService ?oldType ;
                ex:zoneCouverture ?oldZone ;
                ex:capaciteMax ?oldCapacite ;
                ex:estActif ?oldActif .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Service de transport mis à jour avec succès"})

# Supprimer un service de transport
@service_transport_bp.route('/services-transport/<service_id>', methods=['DELETE'])
def delete_service_transport(service_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?service a ex:ServiceTransport ;
                ex:serviceID "{service_id}" ;
                ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Service de transport supprimé avec succès"})