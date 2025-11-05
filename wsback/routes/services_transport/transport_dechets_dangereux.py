# wsback/routes/transport_dechets_dangereux.py
from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, POST, JSON
<<<<<<< HEAD
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL
=======
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, g, EX, RDF_FILE
>>>>>>> doua

transport_dechets_dangereux_bp = Blueprint('transport_dechets_dangereux_bp', __name__)

# Préfixes SPARQL
SPARQL_PREFIX = f"""
{PREFIX}
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# Créer un nouveau transport de déchets dangereux
@transport_dechets_dangereux_bp.route('/transports-dechets-dangereux', methods=['POST'])
def create_transport_dechets_dangereux():
    data = request.json
<<<<<<< HEAD
    transport_id = f"TDD{data.get('id', '1')}"
=======
    import time
    transport_id = f"TDD{int(time.time() * 1000) % 100000}"
>>>>>>> doua
    
    query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{transport_id} a ex:TransportDechetsDangereux ;
<<<<<<< HEAD
            ex:servicetransportID "{transport_id}" ;
=======
            ex:servicetransportID "{transport_id}"^^xsd:string ;
>>>>>>> doua
            ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
            ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
            ex:etattransport "{data.get('etat', 'actif')}" ;
            ex:typeDechetDangereux "{data.get('typeDechetDangereux', '')}" ;
            ex:normesSecurite "{data.get('normesSecurite', '')}" .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(query)
    sparql.query()
    
<<<<<<< HEAD
=======
    # Sauvegarder localement dans dechet.ttl
    transport_ref = EX[transport_id]
    g.add((transport_ref, RDF.type, EX.TransportDechetsDangereux))
    g.add((transport_ref, EX.servicetransportID, Literal(transport_id, datatype=XSD.string)))
    g.add((transport_ref, EX.zoneCouverture, Literal(data.get('zoneCouverture', ''), datatype=XSD.string)))
    g.add((transport_ref, EX.capaciteMax, Literal(data.get('capaciteMax', 0), datatype=XSD.decimal)))
    g.add((transport_ref, EX.etattransport, Literal(data.get('etat', 'actif'), datatype=XSD.string)))
    g.add((transport_ref, EX.typeDechetDangereux, Literal(data.get('typeDechetDangereux', ''), datatype=XSD.string)))
    g.add((transport_ref, EX.normesSecurite, Literal(data.get('normesSecurite', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Transport de déchets dangereux créé avec succès", "id": transport_id}), 201

# Récupérer tous les transports de déchets dangereux
@transport_dechets_dangereux_bp.route('/transports-dechets-dangereux', methods=['GET'])
def get_transports_dechets_dangereux():
    query = f"""
    {SPARQL_PREFIX}
<<<<<<< HEAD
    SELECT ?transport ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetDangereux ?normesSecurite
=======
    SELECT DISTINCT ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetDangereux ?normesSecurite
>>>>>>> doua
    WHERE {{
        ?transport a ex:TransportDechetsDangereux ;
                ex:servicetransportID ?serviceID ;
                ex:zoneCouverture ?zoneCouverture ;
                ex:capaciteMax ?capaciteMax ;
                ex:etattransport ?etat ;
                ex:typeDechetDangereux ?typeDechetDangereux ;
                ex:normesSecurite ?normesSecurite .
    }}
<<<<<<< HEAD
=======
    GROUP BY ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetDangereux ?normesSecurite
>>>>>>> doua
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    transports = []
<<<<<<< HEAD
    for result in results["results"]["bindings"]:
        transports.append({
            "id": result["serviceID"]["value"],
            "zoneCouverture": result["zoneCouverture"]["value"],
            "capaciteMax": result["capaciteMax"]["value"],
            "etat": result["etat"]["value"],
            "typeDechetDangereux": result["typeDechetDangereux"]["value"],
            "normesSecurite": result["normesSecurite"]["value"]
        })
=======
    seen_ids = set()
    for result in results["results"]["bindings"]:
        transport_id = result["serviceID"]["value"]
        if transport_id not in seen_ids:
            seen_ids.add(transport_id)
            transports.append({
                "id": transport_id,
                "zoneCouverture": result["zoneCouverture"]["value"],
                "capaciteMax": result["capaciteMax"]["value"],
                "etat": result["etat"]["value"],
                "typeDechetDangereux": result["typeDechetDangereux"]["value"],
                "normesSecurite": result["normesSecurite"]["value"]
            })
>>>>>>> doua
    
    return jsonify(transports)

# Récupérer un transport de déchets dangereux par ID
@transport_dechets_dangereux_bp.route('/transports-dechets-dangereux/<transport_id>', methods=['GET'])
def get_transport_dechets_dangereux(transport_id):
    query = f"""
    {SPARQL_PREFIX}
    SELECT ?transport ?serviceID ?zoneCouverture ?capaciteMax ?etat ?typeDechetDangereux ?normesSecurite
    WHERE {{
        ?transport a ex:TransportDechetsDangereux ;
                ex:servicetransportID "{transport_id}" ;
                ex:servicetransportID ?serviceID ;
                ex:zoneCouverture ?zoneCouverture ;
                ex:capaciteMax ?capaciteMax ;
                ex:etattransport ?etat ;
                ex:typeDechetDangereux ?typeDechetDangereux ;
                ex:normesSecurite ?normesSecurite .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        transport = {
            "id": result["serviceID"]["value"],
            "zoneCouverture": result["zoneCouverture"]["value"],
            "capaciteMax": result["capaciteMax"]["value"],
            "etat": result["etat"]["value"],
            "typeDechetDangereux": result["typeDechetDangereux"]["value"],
            "normesSecurite": result["normesSecurite"]["value"]
        }
        return jsonify(transport)
    
    return jsonify({"message": "Transport de déchets dangereux non trouvé"}), 404

# Mettre à jour un transport de déchets dangereux
@transport_dechets_dangereux_bp.route('/transports-dechets-dangereux/<transport_id>', methods=['PUT'])
def update_transport_dechets_dangereux(transport_id):
    data = request.json
    
<<<<<<< HEAD
    query = f"""
    {SPARQL_PREFIX}
    DELETE {{
        ?transport ex:zoneCouverture ?oldZone ;
                ex:capaciteMax ?oldCapacite ;
                ex:etattransport ?oldEtat ;
                ex:typeDechetDangereux ?oldType ;
                ex:normesSecurite ?oldNormes .
    }}
    INSERT {{
        ?transport ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
                ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
                ex:etattransport "{data.get('etat', '')}" ;
                ex:typeDechetDangereux "{data.get('typeDechetDangereux', '')}" ;
                ex:normesSecurite "{data.get('normesSecurite', '')}" .
    }}
    WHERE {{
        ?transport a ex:TransportDechetsDangereux ;
                ex:servicetransportID "{transport_id}" ;
                ex:zoneCouverture ?oldZone ;
                ex:capaciteMax ?oldCapacite ;
                ex:etattransport ?oldEtat ;
                ex:typeDechetDangereux ?oldType ;
                ex:normesSecurite ?oldNormes .
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
    DELETE WHERE {{ ex:{transport_id} ?p ?o }}
    """
    sparql.setQuery(delete_query)
    sparql.query()
    
    insert_query = f"""
    {SPARQL_PREFIX}
    INSERT DATA {{
        ex:{transport_id} a ex:TransportDechetsDangereux ;
            ex:servicetransportID "{transport_id}"^^xsd:string ;
            ex:zoneCouverture "{data.get('zoneCouverture', '')}" ;
            ex:capaciteMax "{data.get('capaciteMax', 0)}"^^xsd:decimal ;
            ex:etattransport "{data.get('etat', '')}" ;
            ex:typeDechetDangereux "{data.get('typeDechetDangereux', '')}" ;
            ex:normesSecurite "{data.get('normesSecurite', '')}" .
    }}
    """
    sparql.setQuery(insert_query)
    sparql.query()
    
    # Mettre à jour localement dans dechet.ttl
    transport_ref = EX[transport_id]
    for triple in list(g.triples((transport_ref, None, None))):
        g.remove(triple)
    g.add((transport_ref, RDF.type, EX.TransportDechetsDangereux))
    g.add((transport_ref, EX.servicetransportID, Literal(transport_id, datatype=XSD.string)))
    g.add((transport_ref, EX.zoneCouverture, Literal(data.get('zoneCouverture', ''), datatype=XSD.string)))
    g.add((transport_ref, EX.capaciteMax, Literal(data.get('capaciteMax', 0), datatype=XSD.decimal)))
    g.add((transport_ref, EX.etattransport, Literal(data.get('etat', ''), datatype=XSD.string)))
    g.add((transport_ref, EX.typeDechetDangereux, Literal(data.get('typeDechetDangereux', ''), datatype=XSD.string)))
    g.add((transport_ref, EX.normesSecurite, Literal(data.get('normesSecurite', ''), datatype=XSD.string)))
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Transport de déchets dangereux mis à jour avec succès"})

# Supprimer un transport de déchets dangereux
@transport_dechets_dangereux_bp.route('/transports-dechets-dangereux/<transport_id>', methods=['DELETE'])
def delete_transport_dechets_dangereux(transport_id):
    query = f"""
    {SPARQL_PREFIX}
    DELETE WHERE {{
        ?transport a ex:TransportDechetsDangereux ;
                ex:servicetransportID "{transport_id}" ;
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
    transport_ref = EX[transport_id]
    for triple in list(g.triples((transport_ref, None, None))):
        g.remove(triple)
    g.serialize(destination=RDF_FILE, format="turtle")
    
>>>>>>> doua
    return jsonify({"message": "Transport de déchets dangereux supprimé avec succès"})