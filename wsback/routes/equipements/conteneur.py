# wsback/routes/conteneur.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL

conteneur_bp = Blueprint('conteneur_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau conteneur
@conteneur_bp.route('/conteneurs', methods=['POST'])
def create_conteneur():
    data = request.json
    conteneur_id = f"CN{data.get('id', '1')}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{conteneur_id} a ex:Conteneur ;
            ex:equipementID "{conteneur_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', 'disponible')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:taille "{data.get('taille', '')}" .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Conteneur créé avec succès", "id": conteneur_id}), 201

# Récupérer tous les conteneurs
@conteneur_bp.route('/conteneurs', methods=['GET'])
def get_conteneurs():
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?conteneur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?taille
    WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:taille ?taille .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    conteneurs = []
    for result in results["results"]["bindings"]:
        conteneurs.append({
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "taille": result["taille"]["value"]
        })
    
    return jsonify(conteneurs)

# Récupérer un conteneur par ID
@conteneur_bp.route('/conteneurs/<conteneur_id>', methods=['GET'])
def get_conteneur(conteneur_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?conteneur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?taille
    WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID "{conteneur_id}" ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:taille ?taille .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        conteneur = {
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "taille": result["taille"]["value"]
        }
        return jsonify(conteneur)
    
    return jsonify({"message": "Conteneur non trouvé"}), 404

# Mettre à jour un conteneur
@conteneur_bp.route('/conteneurs/<conteneur_id>', methods=['PUT'])
def update_conteneur(conteneur_id):
    data = request.json
    
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?conteneur ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:taille ?oldTaille .
    }}
    INSERT {{
        ?conteneur ex:nomequiement "{data.get('nomEquipement', '')}" ;
                ex:etat "{data.get('etat', '')}" ;
                ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
                ex:localisation "{data.get('localisation', '')}" ;
                ex:taille "{data.get('taille', '')}" .
    }}
    WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID "{conteneur_id}" ;
                ex:nomequiement ?oldNom ;
                ex:etat ?oldEtat ;
                ex:capacite ?oldCapacite ;
                ex:localisation ?oldLocalisation ;
                ex:taille ?oldTaille .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Conteneur mis à jour avec succès"})

# Supprimer un conteneur
@conteneur_bp.route('/conteneurs/<conteneur_id>', methods=['DELETE'])
def delete_conteneur(conteneur_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID "{conteneur_id}" ;
                ?p ?o .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
    return jsonify({"message": "Conteneur supprimé avec succès"})