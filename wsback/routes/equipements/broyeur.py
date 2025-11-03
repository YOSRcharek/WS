# wsback/routes/broyeur.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

broyeur_bp = Blueprint('broyeur_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau broyeur
@broyeur_bp.route('/broyeurs', methods=['POST'])
def create_broyeur():
    data = request.json
    broyeur_id = f"BR{data.get('id', '1')}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{broyeur_id} a ex:Broyeur ;
            ex:equipementID "{broyeur_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', 'disponible')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:typeDechetBroyé "{data.get('typeDechetBroye', '')}" .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Broyeur créé avec succès", "id": broyeur_id}), 201

# Récupérer tous les broyeurs
@broyeur_bp.route('/broyeurs', methods=['GET'])
def get_broyeurs():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?broyeur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?typeDechetBroye
    WHERE {{
        ?broyeur a ex:Broyeur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:typeDechetBroyé ?typeDechetBroye .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    broyeurs = []
    for result in results["results"]["bindings"]:
        broyeurs.append({
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "typeDechetBroye": result["typeDechetBroye"]["value"]
        })
    
    return jsonify(broyeurs)

# Récupérer un broyeur par ID
@broyeur_bp.route('/broyeurs/<broyeur_id>', methods=['GET'])
def get_broyeur(broyeur_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?broyeur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?typeDechetBroye
    WHERE {{
        ?broyeur a ex:Broyeur ;
                ex:equipementID "{broyeur_id}" ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:typeDechetBroyé ?typeDechetBroye .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        broyeur = {
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "typeDechetBroye": result["typeDechetBroye"]["value"]
        }
        return jsonify(broyeur)
    
    return jsonify({"message": "Broyeur non trouvé"}), 404

# Mettre à jour un broyeur
@broyeur_bp.route('/broyeurs/<broyeur_id>', methods=['PUT'])
def update_broyeur(broyeur_id):
    data = request.json
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?broyeur ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:typeDechetBroyé ?oldType .
    }}
    INSERT {{
        ?broyeur ex:nomequiement "{data.get('nomEquipement', '')}" ;
                ex:etat "{data.get('etat', '')}" ;
                ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
                ex:localisation "{data.get('localisation', '')}" ;
                ex:typeDechetBroyé "{data.get('typeDechetBroye', '')}" .
    }}
    WHERE {{
        ?broyeur a ex:Broyeur ;
                ex:equipementID "{broyeur_id}" ;
                ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:typeDechetBroyé ?oldType .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Broyeur mis à jour avec succès"})

# Supprimer un broyeur
@broyeur_bp.route('/broyeurs/<broyeur_id>', methods=['DELETE'])
def delete_broyeur(broyeur_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?broyeur a ex:Broyeur ;
                ex:equipementID "{broyeur_id}" ;
                ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Broyeur supprimé avec succès"})