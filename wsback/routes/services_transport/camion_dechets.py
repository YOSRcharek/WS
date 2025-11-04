# wsback/routes/camion_dechets.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, g, EX, RDF_FILE

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
    import time
    camion_id = f"CD{int(time.time() * 1000) % 100000}"
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} a ex:camion_de_déchets ;
            ex:servicetransportID "{camion_id}"^^xsd:string ;
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
    
    # Sauvegarder localement dans dechet.ttl
    camion_ref = EX[camion_id]
    g.add((camion_ref, RDF.type, EX.camion_de_déchets))
    g.add((camion_ref, EX.servicetransportID, Literal(camion_id, datatype=XSD.string)))
    g.add((camion_ref, EX.zoneCouverture, Literal(data.get('zoneCouverture', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.capaciteMax, Literal(data.get('capaciteMax', 0), datatype=XSD.decimal)))
    g.add((camion_ref, EX.etattransport, Literal(data.get('etat', 'actif'), datatype=XSD.string)))
    g.add((camion_ref, EX.typeDechetTransporte, Literal(data.get('typeDechetTransporte', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Camion de déchets créé avec succès", "id": camion_id}), 201

# Récupérer tous les camions de déchets
@camion_dechets_bp.route('/camions-dechets', methods=['GET'])
def get_camions_dechets():
    query = f"""
    {SPARQL_PREFIX}
    SELECT DISTINCT ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetTransporte
    WHERE {{
        ?camion a ex:camion_de_déchets ;
                ex:servicetransportID ?serviceID ;
                ex:zoneCouverture ?zoneCouverture ;
                ex:capaciteMax ?capaciteMax ;
                ex:etattransport ?etat ;
                ex:typeDechetTransporte ?typeDechetTransporte .
    }}
    GROUP BY ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetTransporte
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    camions = []
    seen_ids = set()
    for result in results["results"]["bindings"]:
        camion_id = result["serviceID"]["value"]
        if camion_id not in seen_ids:
            seen_ids.add(camion_id)
            camions.append({
                "id": camion_id,
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
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    
    delete_query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{ ex:{camion_id} ?p ?o }}
    """
    sparql.setQuery(delete_query)
    sparql.query()
    
    insert_query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{camion_id} a ex:camion_de_déchets ;
            ex:servicetransportID "{camion_id}"^^xsd:string ;
            ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
            ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
            ex:etattransport "{data.get('etat', '')}" ;
            ex:typeDechetTransporte "{data.get('typeDechetTransporte', '')}" .
    }}
    """
    sparql.setQuery(insert_query)
    sparql.query()
    
    # Mettre à jour localement dans dechet.ttl
    camion_ref = EX[camion_id]
    for triple in list(g.triples((camion_ref, None, None))):
        g.remove(triple)
    g.add((camion_ref, RDF.type, EX.camion_de_déchets))
    g.add((camion_ref, EX.servicetransportID, Literal(camion_id, datatype=XSD.string)))
    g.add((camion_ref, EX.zoneCouverture, Literal(data.get('zoneCouverture', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.capaciteMax, Literal(data.get('capaciteMax', 0), datatype=XSD.decimal)))
    g.add((camion_ref, EX.etattransport, Literal(data.get('etat', ''), datatype=XSD.string)))
    g.add((camion_ref, EX.typeDechetTransporte, Literal(data.get('typeDechetTransporte', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
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
    
    # Supprimer localement du fichier dechet.ttl
    camion_ref = EX[camion_id]
    for triple in list(g.triples((camion_ref, None, None))):
        g.remove(triple)
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({"message": "Camion de déchets supprimé avec succès"})