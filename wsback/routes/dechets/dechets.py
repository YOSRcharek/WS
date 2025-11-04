from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD, RDFS
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

dechets_bp = Blueprint("dechets_bp", __name__)

# URI de la classe Déchet
DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Dechet")

# --- CREATE ---
@dechets_bp.route("/dechets", methods=["POST"])
def add_dechet():
    data = request.json
    dechet_id = "D" + str(len(g) + 1)
    dechet_ref = EX[dechet_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {dechet_ref.n3()} a <{DECHET_CLASS_URI}> ;
            ex:dechetID "{dechet_id}"^^xsd:string ;
            ex:nomdechet "{data.get('nomdechet','')}"^^xsd:string ;
            ex:description "{data.get('description','')}"^^xsd:string ;
            ex:couleur "{data.get('couleur','')}"^^xsd:string ;
            ex:poids "{data.get('poids',0)}"^^xsd:float ;
            ex:isRecyclable "{str(data.get('isRecyclable', True)).lower()}"^^xsd:boolean ;
            ex:quantite "{data.get('quantite',0)}"^^xsd:decimal ;
            ex:generatedDate "{data.get('generatedDate','')}"^^xsd:date .
    }}
    """

    # --- Insert dans Fuseki ---
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # --- Insert local RDF ---
    g.add((dechet_ref, RDF.type, DECHET_CLASS_URI))
    g.add((dechet_ref, EX.dechetID, Literal(dechet_id, datatype=XSD.string)))
    g.add((dechet_ref, EX.nomdechet, Literal(data.get('nomdechet',''), datatype=XSD.string)))
    g.add((dechet_ref, EX.description, Literal(data.get('description',''), datatype=XSD.string)))
    g.add((dechet_ref, EX.couleur, Literal(data.get('couleur',''), datatype=XSD.string)))
    g.add((dechet_ref, EX.poids, Literal(data.get('poids',0), datatype=XSD.float)))
    g.add((dechet_ref, EX.isRecyclable, Literal(data.get('isRecyclable', True), datatype=XSD.boolean)))
    g.add((dechet_ref, EX.quantite, Literal(data.get('quantite',0), datatype=XSD.decimal)))
    g.add((dechet_ref, EX.generatedDate, Literal(data.get('generatedDate',''), datatype=XSD.date)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ Déchet '{dechet_id}' ajouté avec succès !"})

# --- READ ALL ---
@dechets_bp.route("/dechets", methods=["GET"])
def get_dechets():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?dechet ?nomdechet ?description ?couleur ?poids ?isRecyclable ?quantite ?generatedDate
        WHERE {
            ?dechet a ex:Dechet .
            OPTIONAL { ?dechet ex:nomdechet ?nomdechet . }
            OPTIONAL { ?dechet ex:description ?description . }
            OPTIONAL { ?dechet ex:couleur ?couleur . }
            OPTIONAL { ?dechet ex:poids ?poids . }
            OPTIONAL { ?dechet ex:isRecyclable ?isRecyclable . }
            OPTIONAL { ?dechet ex:quantite ?quantite . }
            OPTIONAL { ?dechet ex:generatedDate ?generatedDate . }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dechets = []
    for result in results["results"]["bindings"]:
        dechets.append({k: v["value"] for k, v in result.items()})

    return jsonify(dechets)

# --- READ ONE ---
@dechets_bp.route("/dechets/<dechet_id>", methods=["GET"])
def get_dechet(dechet_id):
    dechet_ref = EX[dechet_id]
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + f"""
        SELECT ?p ?o WHERE {{
            <{dechet_ref}> ?p ?o .
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
@dechets_bp.route("/dechets/<dechet_id>", methods=["PUT"])
def update_dechet(dechet_id):
    data = request.json
    dechet_ref = EX[dechet_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{dechet_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{dechet_ref}> a <{DECHET_CLASS_URI}> ;
            ex:nomdechet "{data.get('nomdechet','')}"^^xsd:string ;
            ex:description "{data.get('description','')}"^^xsd:string ;
            ex:couleur "{data.get('couleur','')}"^^xsd:string ;
            ex:poids "{data.get('poids',0)}"^^xsd:float ;
            ex:isRecyclable "{str(data.get('isRecyclable', True)).lower()}"^^xsd:boolean ;
            ex:quantite "{data.get('quantite',0)}"^^xsd:decimal ;
            ex:generatedDate "{data.get('generatedDate','')}"^^xsd:date .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"♻️ Déchet '{dechet_id}' mis à jour avec succès !"})

# --- DELETE ---
@dechets_bp.route("/dechets/<dechet_id>", methods=["DELETE"])
def delete_dechet(dechet_id):
    dechet_ref = EX[dechet_id]

    delete_query = PREFIX + f"""
    DELETE WHERE {{
        <{dechet_ref}> ?p ?o .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((dechet_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ Déchet '{dechet_id}' supprimé avec succès."})
