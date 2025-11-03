from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD, RDFS
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
# --- TYPE DE DÉCHET ---
typedechets_bp = Blueprint("typedechets_bp", __name__)

TYPE_DE_DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Type_de_dechet")

# --- CREATE ---
@typedechets_bp.route("/typededechet", methods=["POST"])
def add_type_de_dechet():
    data = request.json
    type_id = "TD" + str(len(g) + 1)
    type_ref = EX[type_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {type_ref.n3()} a <{TYPE_DE_DECHET_CLASS_URI}> ;
            ex:typeID "{type_id}"^^xsd:string ;
            ex:categorie "{data.get('categorie','')}"^^xsd:string ;
            ex:dureeVie "{data.get('dureeVie',0)}"^^xsd:integer ;
            ex:toxic "{str(data.get('toxic', False)).lower()}"^^xsd:boolean .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    g.add((type_ref, RDF.type, TYPE_DE_DECHET_CLASS_URI))
    g.add((type_ref, EX.typeID, Literal(type_id, datatype=XSD.string)))
    g.add((type_ref, EX.categorie, Literal(data.get('categorie',''), datatype=XSD.string)))
    g.add((type_ref, EX.dureeVie, Literal(data.get('dureeVie',0), datatype=XSD.integer)))
    g.add((type_ref, EX.toxic, Literal(data.get('toxic', False), datatype=XSD.boolean)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ TypeDeDechet '{type_id}' ajouté avec succès !"})

# --- READ ALL ---
@typedechets_bp.route("/typededechet", methods=["GET"])
def get_types_de_dechet():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?type ?typeID ?categorie ?dureeVie ?toxic
        WHERE {
            ?type a ex:Type_de_dechet .
            OPTIONAL { ?type ex:typeID ?typeID . }
            OPTIONAL { ?type ex:categorie ?categorie . }
            OPTIONAL { ?type ex:dureeVie ?dureeVie . }
            OPTIONAL { ?type ex:toxic ?toxic . }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    types = []
    for result in results["results"]["bindings"]:
        types.append({k: v["value"] for k, v in result.items()})

    return jsonify(types)

# --- READ ONE ---
@typedechets_bp.route("/typededechet/<type_id>", methods=["GET"])
def get_type_de_dechet(type_id):
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    query = PREFIX + f"""
        SELECT ?type ?categorie ?dureeVie ?toxic
        WHERE {{
            ?type a ex:TypeDeDechet ;
                   ex:typeID "{type_id}"^^xsd:string .
            OPTIONAL {{ ?type ex:categorie ?categorie . }}
            OPTIONAL {{ ?type ex:dureeVie ?dureeVie . }}
            OPTIONAL {{ ?type ex:toxic ?toxic . }}
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return jsonify({"message": f"TypeDeDechet '{type_id}' non trouvé"}), 404

    r = results["results"]["bindings"][0]
    data = {k: v.get("value") for k, v in r.items()}
    return jsonify(data)

# --- UPDATE ---
@typedechets_bp.route("/typededechet/<type_id>", methods=["PUT"])
def update_type_de_dechet(type_id):
    data = request.json
    type_ref = EX[type_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{type_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{type_ref}> a <{TYPE_DE_DECHET_CLASS_URI}> ;
            ex:categorie "{data.get('categorie','')}"^^xsd:string ;
            ex:dureeVie "{data.get('dureeVie',0)}"^^xsd:integer ;
            ex:toxic "{str(data.get('toxic', False)).lower()}"^^xsd:boolean .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"♻️ TypeDeDechet '{type_id}' mis à jour avec succès !"})

# --- DELETE ---
@typedechets_bp.route("/typededechet/<type_id>", methods=["DELETE"])
def delete_type_de_dechet(type_id):
    type_ref = EX[type_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{type_ref}> ?p ?o . }}"

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((type_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ TypeDeDechet '{type_id}' supprimé avec succès."})



METAL_WASTE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/MetalWaste")

# --- CREATE ---
@typedechets_bp.route("/metalwaste", methods=["POST"])
def add_metal_waste():
    data = request.json
    metal_id = "MWT" + str(len(g) + 1)
    metal_ref = EX[metal_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {metal_ref.n3()} a <{METAL_WASTE_CLASS_URI}> ;
            
            ex:typeID "{metal_id}"^^xsd:string ;
            ex:categorie "{data.get('categorie','')}"^^xsd:string ;
            ex:dureeVie "{data.get('dureeVie',0)}"^^xsd:integer ;
            ex:toxic "{str(data.get('toxic', False)).lower()}"^^xsd:boolean;
            ex:typeMetal "{data.get('typeMetal','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    g.add((metal_ref, RDF.type, METAL_WASTE_CLASS_URI))
    g.add((metal_ref, RDFS.subClassOf, TYPE_DE_DECHET_CLASS_URI))
    g.add((metal_ref, EX.typeID, Literal(metal_id, datatype=XSD.string)))
    g.add((metal_ref, EX.typeMetal, Literal(data.get('typeMetal',''), datatype=XSD.string)))
    
    g.add((metal_ref, EX.categorie, Literal(data.get('categorie',''), datatype=XSD.string)))
    g.add((metal_ref, EX.dureeVie, Literal(data.get('dureeVie',0), datatype=XSD.integer)))
    g.add((metal_ref, EX.toxic, Literal(data.get('toxic', False), datatype=XSD.boolean)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ MetalWaste '{metal_id}' ajouté avec succès !"})

# --- READ ALL ---
@typedechets_bp.route("/metalwaste", methods=["GET"])
def get_all_metal_waste():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?metal ?metalWasteID ?typeMetal
        WHERE {
            ?metal a ex:MetalWaste .
            OPTIONAL { ?metal ex:metalWasteID ?metalWasteID . }
            OPTIONAL { ?metal ex:typeMetal ?typeMetal . }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    metals = []
    for result in results["results"]["bindings"]:
        metals.append({k: v["value"] for k, v in result.items()})

    return jsonify(metals)

# --- READ ONE ---
@typedechets_bp.route("/metalwaste/<metal_id>", methods=["GET"])
def get_metal_waste(metal_id):
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    query = PREFIX + f"""
        SELECT ?metal ?typeMetal
        WHERE {{
            ?metal a ex:MetalWaste ;
                   ex:metalWasteID "{metal_id}"^^xsd:string .
            OPTIONAL {{ ?metal ex:typeMetal ?typeMetal . }}
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return jsonify({"message": f"MetalWaste '{metal_id}' non trouvé"}), 404

    r = results["results"]["bindings"][0]
    data = {k: v.get("value") for k, v in r.items()}
    return jsonify(data)

# --- UPDATE ---
@typedechets_bp.route("/metalwaste/<metal_id>", methods=["PUT"])
def update_metal_waste(metal_id):
    data = request.json
    metal_ref = EX[metal_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{metal_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{metal_ref}> a <{METAL_WASTE_CLASS_URI}> ;
            rdfs:subClassOf <{TYPE_DE_DECHET_CLASS_URI}> ;
            ex:metalWasteID "{metal_id}"^^xsd:string ;
            ex:typeMetal "{data.get('typeMetal','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"♻️ MetalWaste '{metal_id}' mis à jour avec succès !"})

# --- DELETE ---
@typedechets_bp.route("/metalwaste/<metal_id>", methods=["DELETE"])
def delete_metal_waste(metal_id):
    metal_ref = EX[metal_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{metal_ref}> ?p ?o . }}"

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((metal_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ MetalWaste '{metal_id}' supprimé avec succès."})