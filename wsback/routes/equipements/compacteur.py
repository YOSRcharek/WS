# wsback/routes/compacteur.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

compacteur_bp = Blueprint('compacteur_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau compacteur
@compacteur_bp.route('/compacteurs', methods=['POST'])
def create_compacteur():
    data = request.json
    compacteur_id = f"CO{data.get('id', '1')}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{compacteur_id} a ex:compacteur ;
            ex:equipementID "{compacteur_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', 'disponible')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:pressionCompaction "{data.get('pressionCompaction', '')}" .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Compacteur créé avec succès", "id": compacteur_id}), 201

# Récupérer tous les compacteurs
@compacteur_bp.route('/compacteurs', methods=['GET'])
def get_compacteurs():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?compacteur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?pressionCompaction
    WHERE {{
        ?compacteur a ex:compacteur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:pressionCompaction ?pressionCompaction .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    compacteurs = []
    for result in results["results"]["bindings"]:
        compacteurs.append({
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "pressionCompaction": result["pressionCompaction"]["value"]
        })
    
    return jsonify(compacteurs)

# Récupérer un compacteur par ID
@compacteur_bp.route('/compacteurs/<compacteur_id>', methods=['GET'])
def get_compacteur(compacteur_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?compacteur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?pressionCompaction
    WHERE {{
        ?compacteur a ex:compacteur ;
                ex:equipementID "{compacteur_id}" ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:pressionCompaction ?pressionCompaction .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        compacteur = {
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "pressionCompaction": result["pressionCompaction"]["value"]
        }
        return jsonify(compacteur)
    
    return jsonify({"message": "Compacteur non trouvé"}), 404

# Mettre à jour un compacteur
@compacteur_bp.route('/compacteurs/<compacteur_id>', methods=['PUT'])
def update_compacteur(compacteur_id):
    data = request.json
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?compacteur ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:pressionCompaction ?oldPression .
    }}
    INSERT {{
        ?compacteur ex:nomequiement "{data.get('nomEquipement', '')}" ;
                ex:etat "{data.get('etat', '')}" ;
                ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
                ex:localisation "{data.get('localisation', '')}" ;
                ex:pressionCompaction "{data.get('pressionCompaction', '')}" .
    }}
    WHERE {{
        ?compacteur a ex:compacteur ;
                ex:equipementID "{compacteur_id}" ;
                ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:pressionCompaction ?oldPression .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Compacteur mis à jour avec succès"})

# Supprimer un compacteur
@compacteur_bp.route('/compacteurs/<compacteur_id>', methods=['DELETE'])
def delete_compacteur(compacteur_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?compacteur a ex:compacteur ;
                ex:equipementID "{compacteur_id}" ;
                ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Compacteur supprimé avec succès"})