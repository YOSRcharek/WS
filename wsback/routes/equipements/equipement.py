# wsback/routes/equipement.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

equipement_bp = Blueprint('equipement_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouvel équipement
@equipement_bp.route('/equipements', methods=['POST'])
def create_equipement():
    data = request.json
    equipement_id = f"E{len(data) + 1}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{equipement_id} a ex:Equipement ;
            ex:equipementID "{equipement_id}" ;
            ex:nomEquipement "{data.get('nomEquipement', '')}" ;
            ex:typeEquipement "{data.get('typeEquipement', '')}" ;
            ex:etat "{data.get('etat', 'disponible')}" ;
            ex:dateMaintenance "{data.get('dateMaintenance', '')}"^^xsd:date ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Équipement créé avec succès", "id": equipement_id}), 201

# Récupérer tous les équipements
@equipement_bp.route('/equipements', methods=['GET'])
def get_equipements():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?equipement ?equipementID ?nomEquipement ?typeEquipement ?etat ?dateMaintenance ?capacite
    WHERE {{
        ?equipement a ex:Equipement ;
                   ex:equipementID ?equipementID ;
                   ex:nomEquipement ?nomEquipement ;
                   ex:typeEquipement ?typeEquipement ;
                   ex:etat ?etat ;
                   ex:dateMaintenance ?dateMaintenance ;
                   ex:capacite ?capacite .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    equipements = []
    for result in results["results"]["bindings"]:
        equipements.append({
            "id": result["equipementID"]["value"],
            "nom": result["nomEquipement"]["value"],
            "type": result["typeEquipement"]["value"],
            "etat": result["etat"]["value"],
            "dateMaintenance": result["dateMaintenance"]["value"],
            "capacite": result["capacite"]["value"]
        })
    
    return jsonify(equipements)

# Mettre à jour un équipement
@equipement_bp.route('/equipements/<equipement_id>', methods=['PUT'])
def update_equipement(equipement_id):
    data = request.json
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?equipement ex:nomEquipement ?oldNom ;
                   ex:typeEquipement ?oldType ;
                   ex:etat ?oldEtat ;
                   ex:dateMaintenance ?oldDate ;
                   ex:capacite ?oldCapacite .
    }}
    INSERT {{
        ?equipement ex:nomEquipement "{data.get('nomEquipement', '')}" ;
                   ex:typeEquipement "{data.get('typeEquipement', '')}" ;
                   ex:etat "{data.get('etat', '')}" ;
                   ex:dateMaintenance "{data.get('dateMaintenance', '')}"^^xsd:date ;
                   ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal .
    }}
    WHERE {{
        ?equipement a ex:Equipement ;
                   ex:equipementID "{equipement_id}" ;
                   ex:nomEquipement ?oldNom ;
                   ex:typeEquipement ?oldType ;
                   ex:etat ?oldEtat ;
                   ex:dateMaintenance ?oldDate ;
                   ex:capacite ?oldCapacite .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Équipement mis à jour avec succès"})

# Supprimer un équipement
@equipement_bp.route('/equipements/<equipement_id>', methods=['DELETE'])
def delete_equipement(equipement_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?equipement a ex:Equipement ;
                   ex:equipementID "{equipement_id}" ;
                   ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Équipement supprimé avec succès"})