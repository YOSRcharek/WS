from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD, RDFS
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, RDF_FILE, FUSEKI_QUERY_URL

dechets_bp = Blueprint("dechets_bp", __name__)
# URI de la classe Déchet
DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Dechet")

@dechets_bp.route("/dechets/<individu_id>", methods=["POST"])
def add_dechet_with_individu(individu_id):
    try:
        data = request.get_json()
        dechet_id = "D" + str(len(g) + 1)
        dechet_ref = EX[dechet_id]
        individu_ref = EX[individu_id]

        # Vérifier que l'individu est instance d'une sous-classe de Type_de_dechet
        check_query = PREFIX + f"""
        ASK {{
            {individu_ref.n3()} a ?typeClass .
            ?typeClass rdfs:subClassOf ex:Type_de_dechet .
        }}
        """
        sparql_check = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql_check.setMethod("POST")
        sparql_check.setReturnFormat(JSON)
        sparql_check.setQuery(check_query)
        check_result = sparql_check.query().convert()

        if not check_result["boolean"]:
            return jsonify({
                "error": f"L’individu '{individu_id}' n’est pas une instance d’une sous-classe de Type_de_dechet."
            }), 404

        # Préparer les valeurs correctement typées
        poids = float(data.get("poids", 0))
        quantite = float(data.get("quantite", 0))
        isrecyclable = str(data.get("isrecyclable", True)).lower()
        generatedDate = data.get("generatedDate")
        generatedDate_str = f'"{generatedDate}"^^xsd:date' if generatedDate else ''

        # Création du déchet et lien avec l’individu
        insert_query = PREFIX + f"""
        INSERT DATA {{
        {dechet_ref.n3()} a <{DECHET_CLASS_URI}> ;
            ex:dechetID "{dechet_id}"^^xsd:string ;
            ex:nomdechet "{data.get('nomdechet','')}"^^xsd:string ;
            ex:description "{data.get('description','')}"^^xsd:string ;
            ex:couleur "{data.get('couleur','')}"^^xsd:string ;
            ex:poids "{data.get('poids',0)}"^^xsd:float ;
            ex:isrecyclable "{str(data.get('isrecyclable', True)).lower()}"^^xsd:boolean ;
            ex:quantite "{data.get('quantite',0)}"^^xsd:decimal ;
            ex:generatedDate "{data.get('generatedDate','')}"^^xsd:date .
    }}
    """

        # Envoi vers Fuseki
        sparql_insert = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql_insert.setMethod(POST)
        sparql_insert.setQuery(insert_query)
        sparql_insert.query()

        # --- Graphe local ---
        g.add((dechet_ref, RDF.type, DECHET_CLASS_URI))
        g.add((dechet_ref, EX.dechetID, Literal(dechet_id, datatype=XSD.string)))
        g.add((dechet_ref, EX.nomdechet, Literal(data.get('nomdechet',''), datatype=XSD.string)))
        g.add((dechet_ref, EX.description, Literal(data.get('description',''), datatype=XSD.string)))
        g.add((dechet_ref, EX.couleur, Literal(data.get('couleur',''), datatype=XSD.string)))
        g.add((dechet_ref, EX.poids, Literal(poids, datatype=XSD.float)))
        g.add((dechet_ref, EX.isrecyclable, Literal(data.get('isrecyclable', True), datatype=XSD.boolean)))
        g.add((dechet_ref, EX.quantite, Literal(quantite, datatype=XSD.decimal)))
        if generatedDate:
            g.add((dechet_ref, EX.generatedDate, Literal(generatedDate, datatype=XSD.date)))
        g.add((dechet_ref, EX.typeOf, individu_ref))
        g.serialize(destination=RDF_FILE, format="turtle")

        return jsonify({
            "message": f"✅ Déchet '{dechet_id}' ajouté et lié à l’individu '{individu_id}' !",
            "uri": str(dechet_ref)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dechets_bp.route("/alldechets", methods=["GET"])
def get_all_dechets():
    """
    🧩 Récupère tous les déchets avec leur type (individu de sous-classe)
    et la catégorie correspondante (PlasticWaste, MetalWaste, etc.)
    """
    try:
        query = PREFIX + """
        SELECT ?dechet ?dechetID ?nomdechet ?description ?couleur ?poids ?isrecyclable 
               ?quantite ?generatedDate ?typeIndividu ?categorie
        WHERE {
            ?dechet a ex:Dechet .

            OPTIONAL { ?dechet ex:dechetID ?dechetID . }
            OPTIONAL { ?dechet ex:nomdechet ?nomdechet . }
            OPTIONAL { ?dechet ex:description ?description . }
            OPTIONAL { ?dechet ex:couleur ?couleur . }
            OPTIONAL { ?dechet ex:poids ?poids . }
            OPTIONAL { ?dechet ex:isrecyclable ?isrecyclable . }
            OPTIONAL { ?dechet ex:quantite ?quantite . }
            OPTIONAL { ?dechet ex:generatedDate ?generatedDate . }

            # Relation vers un individu de sous-classe de Type_de_dechet
            OPTIONAL { 
                ?dechet ex:typeOf ?typeIndividu .
                ?typeIndividu a ?subClass .
                ?subClass rdfs:subClassOf* ex:Type_de_dechet .
                BIND(STRAFTER(STR(?subClass), "#") AS ?categorie)
            }
        }
        ORDER BY ?categorie ?nomdechet
        """

        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setMethod("POST")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        results = sparql.query().convert()

        dechets = []
        for result in results["results"]["bindings"]:
            dechets.append({
                "uri": result.get("dechet", {}).get("value"),
                "dechetID": result.get("dechetID", {}).get("value"),
                "nomdechet": result.get("nomdechet", {}).get("value"),
                "description": result.get("description", {}).get("value"),
                "couleur": result.get("couleur", {}).get("value"),
                "poids": result.get("poids", {}).get("value"),
                "isrecyclable": result.get("isrecyclable", {}).get("value"),
                "quantite": result.get("quantite", {}).get("value"),
                "generatedDate": result.get("generatedDate", {}).get("value"),
                "typeIndividu": result.get("typeIndividu", {}).get("value"),
                "categorie": result.get("categorie", {}).get("value"),
            })

        return jsonify(dechets), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dechets_bp.route("/dechets/<individu_id>", methods=["GET"])
def get_dechets_by_individu(individu_id):
    """
    🔍 Récupère tous les déchets associés à un individu de sous-classe de Type_de_dechet
    Exemple : /dechets/PlasticBottle renvoie tous les déchets liés à l'individu PlasticBottle
    """
    try:
        individu_ref = EX[individu_id]

        query = PREFIX + f"""
        SELECT ?dechet ?dechetID ?nomdechet ?description ?couleur ?poids ?isrecyclable 
               ?quantite ?generatedDate ?typeIndividu ?categorie
        WHERE {{
            ?dechet a ex:Dechet ;
                     ex:typeOf {individu_id} .

            OPTIONAL {{ ?dechet ex:dechetID ?dechetID . }}
            OPTIONAL {{ ?dechet ex:nomdechet ?nomdechet . }}
            OPTIONAL {{ ?dechet ex:description ?description . }}
            OPTIONAL {{ ?dechet ex:couleur ?couleur . }}
            OPTIONAL {{ ?dechet ex:poids ?poids . }}
            OPTIONAL {{ ?dechet ex:isrecyclable ?isrecyclable . }}
            OPTIONAL {{ ?dechet ex:quantite ?quantite . }}
            OPTIONAL {{ ?dechet ex:generatedDate ?generatedDate . }}

            # Récupération de la catégorie (sous-classe de Type_de_dechet)
            OPTIONAL {{
                {individu_ref.n3()} a ?subClass .
                ?subClass rdfs:subClassOf* ex:Type_de_dechet .
                BIND(STRAFTER(STR(?subClass), "#") AS ?categorie)
            }}

            BIND({individu_ref.n3()} AS ?typeIndividu)
        }}
        ORDER BY ?nomdechet
        """

        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setMethod("POST")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)
        results = sparql.query().convert()

        dechets = []
        for result in results["results"]["bindings"]:
            dechets.append({
                "uri": result.get("dechet", {}).get("value"),
                "dechetID": result.get("dechetID", {}).get("value"),
                "nomdechet": result.get("nomdechet", {}).get("value"),
                "description": result.get("description", {}).get("value"),
                "couleur": result.get("couleur", {}).get("value"),
                "poids": result.get("poids", {}).get("value"),
                "isrecyclable": result.get("isrecyclable", {}).get("value"),
                "quantite": result.get("quantite", {}).get("value"),
                "generatedDate": result.get("generatedDate", {}).get("value"),
                "typeIndividu": result.get("typeIndividu", {}).get("value"),
                "categorie": result.get("categorie", {}).get("value"),
            })

        if not dechets:
            return jsonify({
                "message": f"Aucun déchet trouvé pour l’individu '{individu_id}'."
            }), 404

        return jsonify({
            "individu": individu_id,
            "total": len(dechets),
            "dechets": dechets
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dechets_bp.route("/dechets/<dechet_id>", methods=["GET"])
def get_dechet(dechet_id):
    FUSEKI_QUERY_URL = "http://localhost:3030/wasteDB/query"
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)

    query = PREFIX + f"""
        SELECT ?dechet ?nomdechet ?description ?couleur ?poids ?isRecyclable ?quantite ?generatedDate
        WHERE {{
            ?dechet a ex:Dechet ;
                    ex:dechetID "{dechet_id}"^^xsd:string .
            OPTIONAL {{ ?dechet ex:nomdechet ?nomdechet . }}
            OPTIONAL {{ ?dechet ex:description ?description . }}
            OPTIONAL {{ ?dechet ex:couleur ?couleur . }}
            OPTIONAL {{ ?dechet ex:poids ?poids . }}
            OPTIONAL {{ ?dechet ex:isrecyclable ?isrecyclable . }}
            OPTIONAL {{ ?dechet ex:quantite ?quantite . }}
            OPTIONAL {{ ?dechet ex:generatedDate ?generatedDate . }}
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return jsonify({"message": f"Déchet '{dechet_id}' non trouvé"}), 404

    r = results["results"]["bindings"][0]
    data = {
        "dechet": r["dechet"]["value"],
        "nomdechet": r.get("nomdechet", {}).get("value"),
        "description": r.get("description", {}).get("value"),
        "couleur": r.get("couleur", {}).get("value"),
        "poids": float(r.get("poids", {}).get("value", 0)),
        "isrecyclable": r.get("isrecyclable", {}).get("value") == "true",
        "quantite": float(r.get("quantite", {}).get("value", 0)),
        "generatedDate": r.get("generatedDate", {}).get("value")
    }

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




MEDICAL_WASTE_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/MedicalWaste")

# --- CREATE ---
@dechets_bp.route("/medicalwaste", methods=["POST"])
def add_medical_waste():
    data = request.json
    waste_id = "MW" + str(len(g) + 1)
    waste_ref = EX[waste_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {waste_ref.n3()} a <{MEDICAL_WASTE_CLASS_URI}> ;
            ex:dechetID "{waste_id}"^^xsd:string ;
            ex:nomdechet "{data.get('nomdechet','')}"^^xsd:string ;
            ex:description "{data.get('description','')}"^^xsd:string ;
            ex:couleur "{data.get('couleur','')}"^^xsd:string ;
            ex:poids "{data.get('poids',0)}"^^xsd:float ;
            ex:isrecyclable "{str(data.get('isrecyclable', True)).lower()}"^^xsd:boolean ;
            ex:quantite "{data.get('quantite',0)}"^^xsd:decimal ;
            ex:generatedDate "{data.get('generatedDate','')}"^^xsd:date ;
            ex:stockageSpecial "{data.get('stockageSpecial','')}"^^xsd:string ;
            ex:infectieux "{str(data.get('infectieux', False)).lower()}"^^xsd:boolean .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    g.add((waste_ref, RDF.type, MEDICAL_WASTE_CLASS_URI))
    g.add((waste_ref, EX.dechetID, Literal(waste_id, datatype=XSD.string)))
    g.add((waste_ref, EX.nomdechet, Literal(data.get('nomdechet',''), datatype=XSD.string)))
    g.add((waste_ref, EX.description, Literal(data.get('description',''), datatype=XSD.string)))
    g.add((waste_ref, EX.poids, Literal(data.get('poids',0), datatype=XSD.float)))
    g.add((waste_ref, EX.isrecyclable, Literal(data.get('isrecyclable', True), datatype=XSD.boolean)))
    g.add((waste_ref, EX.quantite, Literal(data.get('quantite',0), datatype=XSD.decimal)))
    g.add((waste_ref, EX.generatedDate, Literal(data.get('generatedDate',''), datatype=XSD.date)))
    g.add((waste_ref, EX.stockageSpecial, Literal(data.get('stockageSpecial',''), datatype=XSD.string)))
    g.add((waste_ref, EX.infectieux, Literal(data.get('infectieux', False), datatype=XSD.boolean)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ MedicalWaste '{waste_id}' ajouté avec succès !"})

# --- READ ALL ---
@dechets_bp.route("/medicalwaste", methods=["GET"])
def get_medical_wastes():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?waste ?dechetID ?nomdechet ?description ?poids ?isrecyclable ?quantite ?generatedDate ?stockageSpecial ?infectieux
        WHERE {
            ?waste a ex:MedicalWaste .
            OPTIONAL { ?waste ex:dechetID ?dechetID . }
            OPTIONAL { ?waste ex:nomdechet ?nomdechet . }
            OPTIONAL { ?waste ex:description ?description . }
            OPTIONAL { ?waste ex:poids ?poids . }
            OPTIONAL { ?waste ex:isrecyclable ?isrecyclable . }
            OPTIONAL { ?waste ex:quantite ?quantite . }
            OPTIONAL { ?waste ex:generatedDate ?generatedDate . }
            OPTIONAL { ?waste ex:stockageSpecial ?stockageSpecial . }
            OPTIONAL { ?waste ex:infectieux ?infectieux . }
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    wastes = []
    for result in results["results"]["bindings"]:
        wastes.append({k: v["value"] for k, v in result.items()})
    return jsonify(wastes)

# --- READ ONE ---
@dechets_bp.route("/medicalwaste/<waste_id>", methods=["GET"])
def get_medical_waste(waste_id):
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    query = PREFIX + f"""
        SELECT ?waste ?nomdechet ?description ?poids ?isrecyclable ?quantite ?generatedDate ?stockageSpecial ?infectieux
        WHERE {{
            ?waste a ex:MedicalWaste ;
                    ex:dechetID "{waste_id}"^^xsd:string .
            OPTIONAL {{ ?waste ex:nomdechet ?nomdechet . }}
            OPTIONAL {{ ?waste ex:description ?description . }}
            OPTIONAL {{ ?waste ex:poids ?poids . }}
            OPTIONAL {{ ?waste ex:isrecyclable ?isrecyclable . }}
            OPTIONAL {{ ?waste ex:quantite ?quantite . }}
            OPTIONAL {{ ?waste ex:generatedDate ?generatedDate . }}
            OPTIONAL {{ ?waste ex:stockageSpecial ?stockageSpecial . }}
            OPTIONAL {{ ?waste ex:infectieux ?infectieux . }}
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if not results["results"]["bindings"]:
        return jsonify({"message": f"MedicalWaste '{waste_id}' non trouvé"}), 404

    r = results["results"]["bindings"][0]
    data = {k: v.get("value") for k, v in r.items()}
    return jsonify(data)

# --- UPDATE ---
@dechets_bp.route("/medicalwaste/<waste_id>", methods=["PUT"])
def update_medical_waste(waste_id):
    data = request.json
    waste_ref = EX[waste_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{waste_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{waste_ref}> a <{MEDICAL_WASTE_CLASS_URI}> ;
            ex:nomdechet "{data.get('nomdechet','')}"^^xsd:string ;
            ex:description "{data.get('description','')}"^^xsd:string ;
            ex:poids "{data.get('poids',0)}"^^xsd:float ;
            ex:isrecyclable "{str(data.get('isrecyclable', True)).lower()}"^^xsd:boolean ;
            ex:quantite "{data.get('quantite',0)}"^^xsd:decimal ;
            ex:generatedDate "{data.get('generatedDate','')}"^^xsd:date ;
            ex:stockageSpecial "{data.get('stockageSpecial','')}"^^xsd:string ;
            ex:infectieux "{str(data.get('infectieux', False)).lower()}"^^xsd:boolean .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"♻️ MedicalWaste '{waste_id}' mis à jour avec succès !"})

# --- DELETE ---
@dechets_bp.route("/medicalwaste/<waste_id>", methods=["DELETE"])
def delete_medical_waste(waste_id):
    waste_ref = EX[waste_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{waste_ref}> ?p ?o . }}"

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((waste_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ MedicalWaste '{waste_id}' supprimé avec succès."})