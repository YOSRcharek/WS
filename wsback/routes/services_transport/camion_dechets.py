# wsback/routes/camion_dechets.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

camion_dechets_bp = Blueprint('camion_dechets_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau camion de déchets
@camion_dechets_bp.route('/camions-dechets', methods=['POST'])
def create_camion_dechets():
    data = request.json
    camion_id = f"CD{data.get('id', '1')}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} a ex:camion_de_déchets ;
            ex:servicetransportID "{camion_id}" ;
            ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
            ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
            ex:etattransport "{data.get('etat', 'actif')}" ;
            ex:typeDechetTransporte "{data.get('typeDechetTransporte', '')}" .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Camion de déchets créé avec succès", "id": camion_id}), 201

# Récupérer tous les camions de déchets
@camion_dechets_bp.route('/camions-dechets', methods=['GET'])
def get_camions_dechets():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?camion ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetTransporte
    WHERE {{
        ?camion a ex:camion_de_déchets ;
                ex:servicetransportID ?serviceID ;
                ex:zoneCouverture ?zoneCouverture ;
                ex:capaciteMax ?capaciteMax ;
                ex:etattransport ?etat ;
                ex:typeDechetTransporte ?typeDechetTransporte .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    camions = []
    for result in results["results"]["bindings"]:
        camions.append({
            "id": result["serviceID"]["value"],
            "zoneCouverture": result["zoneCouverture"]["value"],
            "capaciteMax": result["capaciteMax"]["value"],
            "etat": result["etat"]["value"],
            "typeDechetTransporte": result["typeDechetTransporte"]["value"]
        })
    
    return jsonify(camions)

# Récupérer un camion de déchets par ID
@camion_dechets_bp.route('/camions-dechets/<camion_id>', methods=['GET'])
def get_camion_dechets(camion_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?camion ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetTransporte
    WHERE {{
        ?camion a ex:camion_de_déchets ;
                ex:servicetransportID "{camion_id}" ;
                ex:servicetransportID ?serviceID ;
                ex:zoneCouverture ?zoneCouverture ;
                ex:capaciteMax ?capaciteMax ;
                ex:etattransport ?etat ;
                ex:typeDechetTransporte ?typeDechetTransporte .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        camion = {
            "id": result["serviceID"]["value"],
            "zoneCouverture": result["zoneCouverture"]["value"],
            "capaciteMax": result["capaciteMax"]["value"],
            "etat": result["etat"]["value"],
            "typeDechetTransporte": result["typeDechetTransporte"]["value"]
        }
        return jsonify(camion)
    
    return jsonify({"message": "Camion de déchets non trouvé"}), 404

# Mettre à jour un camion de déchets
@camion_dechets_bp.route('/camions-dechets/<camion_id>', methods=['PUT'])
def update_camion_dechets(camion_id):
    data = request.json
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?camion ex:zoneCouverture ?oldZone ;
                ex:capaciteMax ?oldCapacite ;
                ex:etattransport ?oldEtat ;
                ex:typeDechetTransporte ?oldType .
    }}
    INSERT {{
        ?camion ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
                ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
                ex:etattransport "{data.get('etat', '')}" ;
                ex:typeDechetTransporte "{data.get('typeDechetTransporte', '')}" .
    }}
    WHERE {{
        ?camion a ex:camion_de_déchets ;
                ex:servicetransportID "{camion_id}" ;
                ex:zoneCouverture ?oldZone ;
                ex:capaciteMax ?oldCapacite ;
                ex:etattransport ?oldEtat ;
                ex:typeDechetTransporte ?oldType .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Camion de déchets mis à jour avec succès"})

# Supprimer un camion de déchets
@camion_dechets_bp.route('/camions-dechets/<camion_id>', methods=['DELETE'])
def delete_camion_dechets(camion_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?camion a ex:camion_de_déchets ;
                ex:servicetransportID "{camion_id}" ;
                ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Camion de déchets supprimé avec succès"})