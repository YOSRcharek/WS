# wsback/routes/camion_benne.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

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
    camion_id = f"CB{data.get('id', '1')}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} a ex:CamionBenne ;
            ex:equipementID "{camion_id}" ;
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
    
    return jsonify({"message": "Camion benne créé avec succès", "id": camion_id}), 201

# Récupérer tous les camions benne
@camion_benne_bp.route('/camions-benne', methods=['GET'])
def get_camions_benne():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?camion ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?volumeBenne
    WHERE {{
        ?camion a ex:CamionBenne ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
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
    
    camions = []
    for result in results["results"]["bindings"]:
        camions.append({
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "volumeBenne": result["volumeBenne"]["value"]
        })
    
    return jsonify(camions)

# Récupérer un camion benne par ID
@camion_benne_bp.route('/camions-benne/<camion_id>', methods=['GET'])
def get_camion_benne(camion_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?camion ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?volumeBenne
    WHERE {{
        ?camion a ex:CamionBenne ;
                ex:equipementID "{camion_id}" ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
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
            "nomEquipement": result["nomEquipement"]["value"],
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
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?camion ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:volumeBenne ?oldVolume .
    }}
    INSERT {{
        ?camion ex:nomequiement "{data.get('nomEquipement', '')}" ;
                ex:etat "{data.get('etat', '')}" ;
                ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
                ex:localisation "{data.get('localisation', '')}" ;
                ex:volumeBenne "{data.get('volumeBenne', 0)}"^^xsd:decimal .
    }}
    WHERE {{
        ?camion a ex:CamionBenne ;
                ex:equipementID "{camion_id}" ;
                ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:volumeBenne ?oldVolume .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
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
    
    return jsonify({"message": "Camion benne supprimé avec succès"})