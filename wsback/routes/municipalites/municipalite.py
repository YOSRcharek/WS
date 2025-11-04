from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

municipalite_bp = Blueprint("municipalite_bp", __name__)

MUNICIPALITE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Municipalite")

# --- CREATE ---
@municipalite_bp.route("/municipalites", methods=["POST"])
def add_municipalite():
    data = request.json
    municipalite_id = "M" + str(len(g) + 1)
    municipalite_ref = EX[municipalite_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {municipalite_ref.n3()} a <{MUNICIPALITE_CLASS_URI}> ;
            ex:municipaliteID "{municipalite_id}"^^xsd:string ;
            ex:nom "{data.get('nom','')}"^^xsd:string ;
            ex:adresse "{data.get('adresse','')}"^^xsd:string ;
            ex:codePostal "{data.get('codePostal','')}"^^xsd:string ;
            ex:telephone "{data.get('telephone','')}"^^xsd:string ;
            ex:email "{data.get('email','')}"^^xsd:string ;
            ex:region "{data.get('region','')}"^^xsd:string ;
            ex:population "{data.get('population',0)}"^^xsd:integer ;
            ex:surface "{data.get('surface',0.0)}"^^xsd:float .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    g.add((municipalite_ref, RDF.type, MUNICIPALITE_CLASS_URI))
    g.add((municipalite_ref, EX.municipaliteID, Literal(municipalite_id, datatype=XSD.string)))
    g.add((municipalite_ref, EX.nom, Literal(data.get('nom',''), datatype=XSD.string)))
    g.add((municipalite_ref, EX.adresse, Literal(data.get('adresse',''), datatype=XSD.string)))
    g.add((municipalite_ref, EX.codePostal, Literal(data.get('codePostal',''), datatype=XSD.string)))
    g.add((municipalite_ref, EX.telephone, Literal(data.get('telephone',''), datatype=XSD.string)))
    g.add((municipalite_ref, EX.email, Literal(data.get('email',''), datatype=XSD.string)))
    g.add((municipalite_ref, EX.region, Literal(data.get('region',''), datatype=XSD.string)))
    g.add((municipalite_ref, EX.population, Literal(data.get('population',0), datatype=XSD.integer)))
    g.add((municipalite_ref, EX.surface, Literal(data.get('surface',0.0), datatype=XSD.float)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ Municipalité '{municipalite_id}' ajoutée avec succès !"})

# --- READ ALL ---
@municipalite_bp.route("/municipalites", methods=["GET"])
def get_municipalites():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + f"""
        SELECT ?municipalite ?nom ?adresse ?codePostal ?telephone ?email ?region ?population ?surface
        WHERE {{
            ?municipalite a <{MUNICIPALITE_CLASS_URI}> .
            OPTIONAL {{ ?municipalite ex:nom ?nom . }}
            OPTIONAL {{ ?municipalite ex:adresse ?adresse . }}
            OPTIONAL {{ ?municipalite ex:codePostal ?codePostal . }}
            OPTIONAL {{ ?municipalite ex:telephone ?telephone . }}
            OPTIONAL {{ ?municipalite ex:email ?email . }}
            OPTIONAL {{ ?municipalite ex:region ?region . }}
            OPTIONAL {{ ?municipalite ex:population ?population . }}
            OPTIONAL {{ ?municipalite ex:surface ?surface . }}
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    municipalites = []
    for result in results["results"]["bindings"]:
        municipalites.append({k: v["value"] for k, v in result.items()})

    return jsonify(municipalites)

# --- READ ONE ---
@municipalite_bp.route("/municipalites/<municipalite_id>", methods=["GET"])
def get_municipalite(municipalite_id):
    municipalite_ref = EX[municipalite_id]
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + f"""
        SELECT ?p ?o WHERE {{
            <{municipalite_ref}> ?p ?o .
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = {}
    for r in results["results"]["bindings"]:
        key = r["p"]["value"].split('#')[-1]
        data[key] = r["o"]["value"]

    return jsonify(data)

# --- UPDATE ---
@municipalite_bp.route("/municipalites/<municipalite_id>", methods=["PUT"])
def update_municipalite(municipalite_id):
    data = request.json
    municipalite_ref = EX[municipalite_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{municipalite_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{municipalite_ref}> a <{MUNICIPALITE_CLASS_URI}> ;
            ex:nom "{data.get('nom','')}"^^xsd:string ;
            ex:adresse "{data.get('adresse','')}"^^xsd:string ;
            ex:codePostal "{data.get('codePostal','')}"^^xsd:string ;
            ex:telephone "{data.get('telephone','')}"^^xsd:string ;
            ex:email "{data.get('email','')}"^^xsd:string ;
            ex:region "{data.get('region','')}"^^xsd:string ;
            ex:population "{data.get('population',0)}"^^xsd:integer ;
            ex:surface "{data.get('surface',0.0)}"^^xsd:float .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"♻️ Municipalité '{municipalite_id}' mise à jour avec succès !"})

# --- DELETE ---
@municipalite_bp.route("/municipalites/<municipalite_id>", methods=["DELETE"])
def delete_municipalite(municipalite_id):
    municipalite_ref = EX[municipalite_id]

    delete_query = PREFIX + f"""
    DELETE WHERE {{
        <{municipalite_ref}> ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((municipalite_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ Municipalité '{municipalite_id}' supprimée avec succès."})