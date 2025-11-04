from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

citizen_matching_bp = Blueprint("citizen_matching_bp", __name__)

@citizen_matching_bp.route("/match-citizens", methods=["POST"])
def match_citizens_to_municipalities():
    citizens = get_unmatched_citizens()
    municipalities = get_all_municipalities()
    matches = []
    
    for citizen in citizens:
        citizen_address = citizen.get("adresse", "").lower()
        best_match = None
        
        # Simple address matching logic
        for municipality in municipalities:
            muni_name = municipality.get("nom", "").lower()
            muni_region = municipality.get("region", "").lower()
            
            if (muni_name in citizen_address or 
                muni_region in citizen_address or
                citizen_address in muni_name):
                best_match = municipality
                break
        
        if best_match:
            # Create relationship in RDF
            citizen_uri = get_citizen_uri(citizen["citizenID"])
            muni_uri = get_municipality_uri(best_match["municipaliteID"])
            
            # Add to Fuseki
            insert_query = PREFIX + f"""
            INSERT DATA {{
                <{citizen_uri}> ex:habiteDans <{muni_uri}> .
            }}
            """
            
            sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
            sparql.setMethod(POST)
            sparql.setQuery(insert_query)
            sparql.query()
            
            # Add to local graph
            g.add((URIRef(citizen_uri), EX.habiteDans, URIRef(muni_uri)))
            
            matches.append({
                "citizen": citizen["nom"],
                "municipality": best_match["nom"],
                "reason": "Address match"
            })
    
    # Save to file
    g.serialize(destination=RDF_FILE, format="turtle")
    
    return jsonify({
        "status": "success",
        "matches": matches,
        "total_matched": len(matches)
    })

def get_unmatched_citizens():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?citizenID ?nom ?adresse WHERE {
            ?c a ex:Citoyen .
            ?c ex:citizenID ?citizenID .
            OPTIONAL { ?c ex:neaemcitoyen ?nom . }
            OPTIONAL { ?c ex:addresscit ?adresse . }
            FILTER NOT EXISTS { ?c ex:habiteDans ?m }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return [{"citizenID": r["citizenID"]["value"],
             "nom": r.get("nom", {}).get("value", ""),
             "adresse": r.get("adresse", {}).get("value", "")}
            for r in results["results"]["bindings"]]

def get_all_municipalities():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?municipaliteID ?nom ?region WHERE {
            ?m a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Municipalite> .
            OPTIONAL { ?m ex:municipaliteID ?municipaliteID . }
            OPTIONAL { ?m ex:nom ?nom . }
            OPTIONAL { ?m ex:region ?region . }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return [{"municipaliteID": r.get("municipaliteID", {}).get("value", ""),
             "nom": r.get("nom", {}).get("value", ""),
             "region": r.get("region", {}).get("value", "")}
            for r in results["results"]["bindings"]]

def get_citizen_uri(citizen_id):
    return f"http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#{citizen_id}"

def get_municipality_uri(muni_id):
    return f"http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34#{muni_id}"

@citizen_matching_bp.route("/municipality-citizens/<municipality_id>", methods=["GET"])
def get_municipality_citizens(municipality_id):
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + f"""
        SELECT ?nom ?adresse WHERE {{
            ?c a ex:Citoyen .
            ?c ex:habiteDans ?m .
            ?m ex:municipaliteID "{municipality_id}" .
            OPTIONAL {{ ?c ex:neaemcitoyen ?nom . }}
            OPTIONAL {{ ?c ex:addresscit ?adresse . }}
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    citizens = [{
        "nom": r.get("nom", {}).get("value", "Nom non spécifié"),
        "adresse": r.get("adresse", {}).get("value", "Adresse non spécifiée")
    } for r in results["results"]["bindings"]]
    
    return jsonify(citizens)