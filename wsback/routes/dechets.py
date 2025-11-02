from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper
from rdflib import Literal
from rdflib.namespace import RDF, RDFS, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, RDF_FILE
from SPARQLWrapper import JSON

dechets_bp = Blueprint("dechets_bp", __name__)

@dechets_bp.route("/dechets", methods=["POST"])
def add_dechet():
    data = request.json
    name = data["name"]
    dechet_uri = f"ex:{name}"

    # --- 1️⃣ Ajout dans Fuseki ---
    insert_query = PREFIX + f"""
        INSERT DATA {{
            {dechet_uri} a ex:Dechet ;
                rdfs:label "{data.get('label', name)}" ;
                ex:nomdechet "{data.get('nomdechet', name)}"^^xsd:string ;
                ex:description "{data.get('description', '')}"^^xsd:string ;
                ex:couleur "{data.get('couleur', '')}"^^xsd:string ;
                ex:poids "{data.get('poids', 0)}"^^xsd:float ;
                ex:isrecyclable "{str(data.get('isrecyclable', True)).lower()}"^^xsd:boolean ;
                ex:quantite "{data.get('quantite', 0)}"^^xsd:decimal ;
                ex:generatedDate "{data.get('generatedDate', '')}"^^xsd:date .
        }}
    """
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(insert_query)
    sparql.method = "POST"
    sparql.query()

    # --- 2️⃣ Ajout dans RDF local ---
    dechet_ref = EX[name]
    g.add((dechet_ref, RDF.type, EX.Dechet))
    g.add((dechet_ref, RDFS.label, Literal(data.get('label', name))))
    g.add((dechet_ref, EX.nomdechet, Literal(data.get('nomdechet', name), datatype=XSD.string)))
    g.add((dechet_ref, EX.description, Literal(data.get('description', ''), datatype=XSD.string)))
    g.add((dechet_ref, EX.couleur, Literal(data.get('couleur', ''), datatype=XSD.string)))
    g.add((dechet_ref, EX.poids, Literal(data.get('poids', 0), datatype=XSD.float)))
    g.add((dechet_ref, EX.isrecyclable, Literal(data.get('isrecyclable', True), datatype=XSD.boolean)))
    g.add((dechet_ref, EX.quantite, Literal(data.get('quantite', 0), datatype=XSD.decimal)))
    g.add((dechet_ref, EX.generatedDate, Literal(data.get('generatedDate', ''), datatype=XSD.date)))

    # Sauvegarde locale
    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"✅ Déchet '{name}' ajouté avec succès !"})

@dechets_bp.route("/dechets", methods=["GET"])
def get_dechets_fuseki():
    FUSEKI_QUERY_URL = "http://localhost:3030/wasteDB/query"
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?dechet ?label ?nomdechet ?description ?typeDechet ?couleur ?poids ?isRecyclable ?quantite ?generatedDate
        WHERE {
            ?dechet a ex:Dechet .
            OPTIONAL { ?dechet rdfs:label ?label . }
            OPTIONAL { ?dechet ex:nomdechet ?nomdechet . }
            OPTIONAL { ?dechet ex:description ?description . }
            OPTIONAL { ?dechet ex:typeDechet ?typeDechet . }
            OPTIONAL { ?dechet ex:couleur ?couleur . }
            OPTIONAL { ?dechet ex:poids ?poids . }
            OPTIONAL { ?dechet ex:isRecyclable ?isRecyclable . }
            OPTIONAL { ?dechet ex:quantite ?quantite . }
            OPTIONAL { ?dechet ex:generatedDate ?generatedDate . }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = []
    for r in results["results"]["bindings"]:
        data.append({
            "dechet": r["dechet"]["value"],
            "label": r.get("label", {}).get("value"),
            "nomdechet": r.get("nomdechet", {}).get("value"),
            "description": r.get("description", {}).get("value"),
            "couleur": r.get("couleur", {}).get("value"),
            "poids": float(r.get("poids", {}).get("value", 0)),
            "isrecyclable": r.get("isrecyclable", {}).get("value") == "true",
            "quantite": float(r.get("quantite", {}).get("value", 0)),
            "generatedDate": r.get("generatedDate", {}).get("value")
        })

    return jsonify(data)