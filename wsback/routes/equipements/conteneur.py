# wsback/routes/conteneur.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
<<<<<<< HEAD
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL
=======
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, g, EX, RDF_FILE
>>>>>>> doua

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
<<<<<<< HEAD
    conteneur_id = f"CN{data.get('id', '1')}"
=======
    import time
    conteneur_id = f"CN{int(time.time() * 1000) % 100000}"
    conteneur_uri = conteneur_id
    conteneur_tech_id = conteneur_id
>>>>>>> doua
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
<<<<<<< HEAD
        ex:{conteneur_id} a ex:Conteneur ;
            ex:equipementID "{conteneur_id}" ;
=======
        ex:{conteneur_id} a ex:Conteneur, ex:Equipement ;
            ex:equipementID "{conteneur_id}"^^xsd:string ;
>>>>>>> doua
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
    
<<<<<<< HEAD
=======
    # Sauvegarder localement dans dechet.ttl
    conteneur_ref = EX[conteneur_id]
    g.add((conteneur_ref, RDF.type, EX.Conteneur))
    g.add((conteneur_ref, RDF.type, EX.Equipement))
    g.add((conteneur_ref, EX.equipementID, Literal(conteneur_id, datatype=XSD.string)))
    g.add((conteneur_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((conteneur_ref, EX.etat, Literal(data.get('etat', 'disponible'), datatype=XSD.string)))
    g.add((conteneur_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((conteneur_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((conteneur_ref, EX.taille, Literal(data.get('taille', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Conteneur créé avec succès", "id": conteneur_id}), 201

# Récupérer tous les conteneurs
@conteneur_bp.route('/conteneurs', methods=['GET'])
def get_conteneurs():
    query = f"""
    {SPARQL_PREFIX}
<<<<<<< HEAD
    SELECT ?conteneur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?taille
    WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomEquipement ;
=======
    SELECT DISTINCT ?equipementID ?nomequiement ?etat ?capacite ?localisation ?taille
    WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomequiement ;
>>>>>>> doua
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:taille ?taille .
    }}
<<<<<<< HEAD
=======
    GROUP BY ?equipementID ?nomequiement ?etat ?capacite ?localisation ?taille
>>>>>>> doua
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    conteneurs = []
<<<<<<< HEAD
    for result in results["results"]["bindings"]:
        conteneurs.append({
            "id": result["equipementID"]["value"],
            "nomEquipement": result["nomEquipement"]["value"],
            "etat": result["etat"]["value"],
            "capacite": result["capacite"]["value"],
            "localisation": result["localisation"]["value"],
            "taille": result["taille"]["value"]
        })
=======
    seen_ids = set()
    for result in results["results"]["bindings"]:
        conteneur_id = result["equipementID"]["value"]
        if conteneur_id not in seen_ids:
            seen_ids.add(conteneur_id)
            conteneurs.append({
                "id": conteneur_id,
                "nomEquipement": result["nomequiement"]["value"],
                "etat": result["etat"]["value"],
                "capacite": result["capacite"]["value"],
                "localisation": result["localisation"]["value"],
                "taille": result["taille"]["value"]
            })
>>>>>>> doua
    
    return jsonify(conteneurs)

# Récupérer un conteneur par ID
@conteneur_bp.route('/conteneurs/<conteneur_id>', methods=['GET'])
def get_conteneur(conteneur_id):
    query = f"""
    {SPARQL_PREFIX}
<<<<<<< HEAD
    SELECT ?conteneur ?equipementID ?nomEquipement ?etat ?capacite ?localisation ?taille
=======
    SELECT ?conteneur ?equipementID ?nomequiement ?etat ?capacite ?localisation ?taille
>>>>>>> doua
    WHERE {{
        ?conteneur a ex:Conteneur ;
                ex:equipementID "{conteneur_id}" ;
                ex:equipementID ?equipementID ;
<<<<<<< HEAD
                ex:nomequiement ?nomEquipement ;
=======
                ex:nomequiement ?nomequiement ;
>>>>>>> doua
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
<<<<<<< HEAD
            "nomEquipement": result["nomEquipement"]["value"],
=======
            "nomEquipement": result["nomequiement"]["value"],
>>>>>>> doua
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
    
<<<<<<< HEAD
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
    
=======
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    
    delete_query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{ ex:{conteneur_id} ?p ?o }}
    """
    sparql.setQuery(delete_query)
    sparql.query()
    
    insert_query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{conteneur_id} a ex:Conteneur, ex:Equipement ;
            ex:equipementID "{conteneur_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', '')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:taille "{data.get('taille', '')}" .
    }}
    """
    sparql.setQuery(insert_query)
    sparql.query()
    
    # Mettre à jour localement dans dechet.ttl
    conteneur_ref = EX[conteneur_id]
    for triple in list(g.triples((conteneur_ref, None, None))):
        g.remove(triple)
    g.add((conteneur_ref, RDF.type, EX.Conteneur))
    g.add((conteneur_ref, RDF.type, EX.Equipement))
    g.add((conteneur_ref, EX.equipementID, Literal(conteneur_id, datatype=XSD.string)))
    g.add((conteneur_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((conteneur_ref, EX.etat, Literal(data.get('etat', ''), datatype=XSD.string)))
    g.add((conteneur_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((conteneur_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((conteneur_ref, EX.taille, Literal(data.get('taille', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
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
    
<<<<<<< HEAD
=======
    # Supprimer localement du fichier dechet.ttl
    conteneur_ref = EX[conteneur_id]
    for triple in list(g.triples((conteneur_ref, None, None))):
        g.remove(triple)
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Conteneur supprimé avec succès"})