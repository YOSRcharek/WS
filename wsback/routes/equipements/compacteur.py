# wsback/routes/compacteur.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, g, EX, RDF_FILE

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
    import time
    compacteur_id = f"CO{int(time.time() * 1000) % 100000}"
    compacteur_uri = compacteur_id
    compacteur_tech_id = compacteur_id
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{compacteur_id} a ex:compacteur, ex:Equipement ;
            ex:equipementID "{compacteur_id}"^^xsd:string ;
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
    
    # Sauvegarder localement dans dechet.ttl
    compacteur_ref = EX[compacteur_id]
    g.add((compacteur_ref, RDF.type, EX.compacteur))
    g.add((compacteur_ref, RDF.type, EX.Equipement))
    g.add((compacteur_ref, EX.equipementID, Literal(compacteur_id, datatype=XSD.string)))
    g.add((compacteur_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((compacteur_ref, EX.etat, Literal(data.get('etat', 'disponible'), datatype=XSD.string)))
    g.add((compacteur_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((compacteur_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((compacteur_ref, EX.pressionCompaction, Literal(data.get('pressionCompaction', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Compacteur créé avec succès", "id": compacteur_id}), 201

# Récupérer tous les compacteurs
@compacteur_bp.route('/compacteurs', methods=['GET'])
def get_compacteurs():
    query = f"""
    {SPARQL_PREFIX}
    SELECT DISTINCT ?equipementID ?nomequiement ?etat ?capacite ?localisation ?pressionCompaction
    WHERE {{
        ?compacteur a ex:compacteur ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomequiement ;
                ex:etat ?etat ;
                ex:capacite ?capacite ;
                ex:localisation ?localisation ;
                ex:pressionCompaction ?pressionCompaction .
    }}
    GROUP BY ?equipementID ?nomequiement ?etat ?capacite ?localisation ?pressionCompaction
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    compacteurs = []
    seen_ids = set()
    for result in results["results"]["bindings"]:
        compacteur_id = result["equipementID"]["value"]
        if compacteur_id not in seen_ids:
            seen_ids.add(compacteur_id)
            compacteurs.append({
                "id": compacteur_id,
                "nomEquipement": result["nomequiement"]["value"],
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
    SELECT ?compacteur ?equipementID ?nomequiement ?etat ?capacite ?localisation ?pressionCompaction
    WHERE {{
        ?compacteur a ex:compacteur ;
                ex:equipementID "{compacteur_id}" ;
                ex:equipementID ?equipementID ;
                ex:nomequiement ?nomequiement ;
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
            "nomEquipement": result["nomequiement"]["value"],
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
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    
    delete_query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{ ex:{compacteur_id} ?p ?o }}
    """
    sparql.setQuery(delete_query)
    sparql.query()
    
    insert_query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{compacteur_id} a ex:compacteur, ex:Equipement ;
            ex:equipementID "{compacteur_id}" ;
            ex:nomequiement "{data.get('nomEquipement', '')}" ;
            ex:etat "{data.get('etat', '')}" ;
            ex:capacite "{data.get('capacite', 0)}"^^xsd:decimal ;
            ex:localisation "{data.get('localisation', '')}" ;
            ex:pressionCompaction "{data.get('pressionCompaction', '')}" .
    }}
    """
    sparql.setQuery(insert_query)
    sparql.query()
    
    # Mettre à jour localement dans dechet.ttl
    compacteur_ref = EX[compacteur_id]
    for triple in list(g.triples((compacteur_ref, None, None))):
        g.remove(triple)
    g.add((compacteur_ref, RDF.type, EX.compacteur))
    g.add((compacteur_ref, RDF.type, EX.Equipement))
    g.add((compacteur_ref, EX.equipementID, Literal(compacteur_id, datatype=XSD.string)))
    g.add((compacteur_ref, EX.nomequiement, Literal(data.get('nomEquipement', ''), datatype=XSD.string)))
    g.add((compacteur_ref, EX.etat, Literal(data.get('etat', ''), datatype=XSD.string)))
    g.add((compacteur_ref, EX.capacite, Literal(data.get('capacite', 0), datatype=XSD.decimal)))
    g.add((compacteur_ref, EX.localisation, Literal(data.get('localisation', ''), datatype=XSD.string)))
    g.add((compacteur_ref, EX.pressionCompaction, Literal(data.get('pressionCompaction', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
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
    
    # Supprimer localement du fichier dechet.ttl
    compacteur_ref = EX[compacteur_id]
    for triple in list(g.triples((compacteur_ref, None, None))):
        g.remove(triple)
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Compacteur supprimé avec succès"})