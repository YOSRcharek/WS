# wsback/routes/broyeur.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, g, EX, RDF_FILE
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD

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
    import time
    broyeur_id = f"BR{int(time.time() * 1000) % 100000}"
    broyeur_uri = broyeur_id
    broyeur_tech_id = broyeur_id
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{broyeur_id} a ex:Broyeur, ex:Equipement ;
            ex:equipementID "{broyeur_id}"^^xsd:string ;
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
    
<<<<<<< HEAD
=======
    # --- Ajout dans le graphe RDF local ---
    broyeur_ref = EX[broyeur_id]
    g.add((broyeur_ref, RDF.type, EX.Broyeur))
    g.add((broyeur_ref, RDF.type, EX.Equipement))
    g.add((broyeur_ref, EX.equipementID, Literal(broyeur_id, datatype=XSD.string)))
    g.add((broyeur_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((broyeur_ref, EX.etat, Literal(data.get('etat', 'disponible'), datatype=XSD.string)))
    g.add((broyeur_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((broyeur_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((broyeur_ref, EX.typeDechetBroyé, Literal(data.get('typeDechetBroye', ''), datatype=XSD.string)))
    
    # Sauvegarder le fichier TTL
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Broyeur créé avec succès", "id": broyeur_id}), 201

# Récupérer tous les broyeurs
@broyeur_bp.route('/broyeurs', methods=['GET'])
def get_broyeurs():
    query = f"""
    {SPARQL_PREFIX}
<<<<<<< HEAD
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
=======
    SELECT DISTINCT ?equipementID ?nomequiement ?etat ?capacite ?localisation ?typeDechetBroyé
    WHERE {{
        ?broyeur a ex:Broyeur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomequiement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:typeDechetBroyé ?typeDechetBroyé .
    }}
    GROUP BY ?equipementID ?nomequiement ?etat ?capacite ?localisation ?typeDechetBroyé
>>>>>>> doua
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    broyeurs = []
<<<<<<< HEAD
    for result in results["results"]["bindings"]:
        broyeurs.append({
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "typeDechetBroye": result["typeDechetBroye"]["value"]
        })
=======
    seen_ids = set()
    for result in results["results"]["bindings"]:
        broyeur_id = result["equipementID"]["value"]
        if broyeur_id not in seen_ids:
            seen_ids.add(broyeur_id)
            broyeurs.append({
                "id": broyeur_id,
                "nomEquipement": result["nomequiement"]["value"],
                "etat": result["etat"]["value"],
                "capacite": result["capacite"]["value"],
                "localisation": result["localisation"]["value"],
                "typeDechetBroye": result["typeDechetBroyé"]["value"]
            })
>>>>>>> doua
    
    return jsonify(broyeurs)

# Récupérer un broyeur par ID
@broyeur_bp.route('/broyeurs/<broyeur_id>', methods=['GET'])
def get_broyeur(broyeur_id):
    query = f"""
    {SPARQL_PREFIX}
<<<<<<< HEAD
    SELECT ?broyeur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?typeDechetBroye
=======
    SELECT ?broyeur ?equipementID ?nomequiement ?etat ?capacite ?localisation ?typeDechetBroyé
>>>>>>> doua
    WHERE {{
        ?broyeur a ex:Broyeur ;
                ex:equipementID "{broyeur_id}" ;
                ex:equipementID ?equipementID ;
<<<<<<< HEAD
                ex:nomequiement ?nomEquipement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:typeDechetBroyé ?typeDechetBroye .
=======
                ex:nomequiement ?nomequiement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:typeDechetBroyé ?typeDechetBroyé .
>>>>>>> doua
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
<<<<<<< HEAD
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "typeDechetBroye": result["typeDechetBroye"]["value"]
=======
            "nomEquipement": result["nomequiement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "typeDechetBroye": result["typeDechetBroyé"]["value"]
>>>>>>> doua
        }
        return jsonify(broyeur)
    
    return jsonify({"message": "Broyeur non trouvé"}), 404

# Mettre à jour un broyeur
@broyeur_bp.route('/broyeurs/<broyeur_id>', methods=['PUT'])
def update_broyeur(broyeur_id):
    data = request.json
    
<<<<<<< HEAD
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
    
=======
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    
    # Supprimer complètement l'entité
    delete_query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{ ex:{broyeur_id} ?p ?o }}
    """
    sparql.setQuery(delete_query)
    sparql.query()
    
    # Recréer l'entité avec les nouvelles données
    insert_query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{broyeur_id} a ex:Broyeur, ex:Equipement ;
            ex:equipementID "{broyeur_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', '')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:typeDechetBroyé "{data.get('typeDechetBroye', '')}" .
    }}
    """
    sparql.setQuery(insert_query)
    sparql.query()
    
    # Mettre à jour localement dans dechet.ttl
    broyeur_ref = EX[broyeur_id]
    for triple in list(g.triples((broyeur_ref, None, None))):
        g.remove(triple)
    g.add((broyeur_ref, RDF.type, EX.Broyeur))
    g.add((broyeur_ref, RDF.type, EX.Equipement))
    g.add((broyeur_ref, EX.equipementID, Literal(broyeur_id, datatype=XSD.string)))
    g.add((broyeur_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((broyeur_ref, EX.etat, Literal(data.get('etat', ''), datatype=XSD.string)))
    g.add((broyeur_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((broyeur_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((broyeur_ref, EX.typeDechetBroyé, Literal(data.get('typeDechetBroye', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Broyeur mis à jour avec succès"})

# Supprimer un broyeur
@broyeur_bp.route('/broyeurs/<broyeur_id>', methods=['DELETE'])
def delete_broyeur(broyeur_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
<<<<<<< HEAD
        ?broyeur a ex:Broyeur ;
                ex:equipementID "{broyeur_id}" ;
                ?p ?o .
=======
        ex:{broyeur_id} ?p ?o .
>>>>>>> doua
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
<<<<<<< HEAD
=======
    # Supprimer localement du fichier dechet.ttl
    broyeur_ref = EX[broyeur_id]
    for triple in list(g.triples((broyeur_ref, None, None))):
        g.remove(triple)
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Broyeur supprimé avec succès"})