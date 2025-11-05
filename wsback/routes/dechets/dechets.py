from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD, RDFS
from config import g, EX1,FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
import requests

dechets_bp = Blueprint("dechets_bp", __name__)
# URI de la classe Déchet
DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Dechet")
PREFIX = """PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

"""
PREFIX1 = """PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

"""
FUSEKI_QUERY_URL1 = "http://127.0.0.1:3030/wasteDB/sparql"

@dechets_bp.route("/citoyens", methods=["GET"])
def get_all_citoyens():
    """
    🧑‍🤝‍🧑 Récupère tous les citoyens (instances de ex1:citoyen)
    depuis le fichier dechet.ttl avec leurs propriétés.
    """
    try:
        citoyens = []

        # Parcours des individus de type ex1:citoyen
        for citoyen in g.subjects(RDF.type, EX1.citoyen):
            citoyen_data = {"uri": str(citoyen)}

            # Récupérer les propriétés connues
            for prop, name in [
                (EX1.addresscit, "addresscit"),
                (EX1.age, "age"),
                (EX1.citizenID, "citizenID"),
                (EX1.email, "email"),
                (EX1.neaemcitoyen, "neaemcitoyen"),
                (EX1.phoneNumber, "phoneNumber"),
            ]:
                value = g.value(citoyen, prop)
                # Si valeur manquante, on peut mettre un ID par défaut basé sur l’URI
                if value:
                    citoyen_data[name] = str(value)
                elif name == "citizenID":
                    # extraire le dernier segment de l'URI si citizenID absent
                    citoyen_data[name] = str(citoyen).split("/")[-1]

            citoyens.append(citoyen_data)

        # Trier les citoyens par nom si possible
        citoyens.sort(key=lambda c: c.get("neaemcitoyen", "").lower())

        return jsonify(citoyens), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dechets_bp.route("/dechets/<individu_id>", methods=["POST"])
def add_dechet_with_individu(individu_id):
    """
    ➕ Ajoute un déchet lié à un individu existant
    dans Fuseki ET localement dans dechet.ttl (Protégé).
    """
    try:
        data = request.get_json()
        dechet_id = "D" + str(len(g) + 1)
        dechet_ref = EX1[dechet_id]
        individu_ref = EX1[individu_id]

        # --- Vérifier que l’individu appartient à une sous-classe de Type_de_dechet ---
        check_query = PREFIX + f"""
        ASK {{
            {individu_ref.n3()} a ?typeClass .
            ?typeClass rdfs:subClassOf ex:Type_de_dechet .
        }}
        """
        sparql_check = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql_check.setReturnFormat(JSON)
        sparql_check.setQuery(check_query)
        result_check = sparql_check.query().convert()

        if not result_check["boolean"]:
            return jsonify({
                "error": f"L’individu '{individu_id}' n’est pas une instance d’une sous-classe de Type_de_dechet."
            }), 400

        # --- Préparer les valeurs correctement typées ---
        poids = float(data.get("poids", 0))
        quantite = float(data.get("quantite", 0))
        isrecyclable = str(data.get("isrecyclable", True)).lower()
        generatedDate = data.get("generatedDate")
        generatedDate_triple = f'ex:generatedDate "{generatedDate}"^^xsd:date ;' if generatedDate else ''

        # --- SPARQL INSERT (FUSEKI) ---
        insert_query = PREFIX + f"""
        INSERT DATA {{
            {dechet_ref.n3()} a ex:Dechet ;
                ex:dechetID "{dechet_id}"^^xsd:string ;
                ex:nomdechet "{data.get('nomdechet','')}"^^xsd:string ;
                ex:categorie "{data.get('categorie','')}"^^xsd:string ;
                ex:description "{data.get('description','')}"^^xsd:string ;
                ex:couleur "{data.get('couleur','')}"^^xsd:string ;
                ex:poids "{poids}"^^xsd:float ;
                ex:quantite "{quantite}"^^xsd:decimal ;
                ex:isrecyclable "{isrecyclable}"^^xsd:boolean ;
                ex:type_of {individu_ref.n3()} ;
                {generatedDate_triple}
                rdfs:subClassOf ex:Type_de_dechet .
        }}

        """
        
        sparql_insert = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql_insert.setMethod(POST)
        sparql_insert.setQuery(insert_query)
        sparql_insert.query()

        # --- Ajout local dans dechet.ttl ---
        g.add((dechet_ref, RDF.type, EX1.Dechet))
        g.add((dechet_ref, EX1.dechetID, Literal(dechet_id, datatype=XSD.string)))
        g.add((dechet_ref, EX1.nomdechet, Literal(data.get("nomdechet", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.categorie, Literal(data.get("categorie", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.description, Literal(data.get("description", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.couleur, Literal(data.get("couleur", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.poids, Literal(poids, datatype=XSD.float)))
        g.add((dechet_ref, EX1.quantite, Literal(quantite, datatype=XSD.decimal)))
        g.add((dechet_ref, EX1.isrecyclable, Literal(data.get("isrecyclable", True), datatype=XSD.boolean)))
        if generatedDate:
            g.add((dechet_ref, EX1.generatedDate, Literal(generatedDate, datatype=XSD.date)))
        g.add((dechet_ref, EX1.type_of, individu_ref))

        g.serialize(destination=RDF_FILE, format="turtle")

        return jsonify({
            "message": f"✅ Déchet '{dechet_id}' ajouté et lié à l’individu '{individu_id}' !",
            "uri": str(dechet_ref)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dechets_bp.route("/citoyens/<citoyen_id>/dechets", methods=["GET"])
def get_dechets_by_citoyen_local(citoyen_id):
    """
    ♻️ Retourne tous les déchets générés par un citoyen spécifique
    via la propriété ex:generatedBy depuis le fichier local dechet.ttl
    """
    try:
        dechets = []

        citoyen_ref = EX1[citoyen_id]

        # Parcourir tous les déchets liés à ce citoyen
        for dechet in g.subjects(EX1.generatedBy, citoyen_ref):
            dechet_data = {"dechetID": str(dechet).split("#")[-1]}

            # Lire toutes les propriétés connues du déchet
            for prop, name, cast in [
                (EX1.nomdechet, "nomdechet", str),
                (EX1.description, "description", str),
                (EX1.couleur, "couleur", str),
                (EX1.categorie, "categorie", str),
                (EX1.poids, "poids", float),
                (EX1.quantite, "quantite", float),
                (EX1.isrecyclable, "isrecyclable", lambda v: str(v).lower() == "true"),
                (EX1.generatedDate, "generatedDate", str),
            ]:
                value = g.value(dechet, prop)
                if value is not None:
                    dechet_data[name] = cast(value)

            dechets.append(dechet_data)

        return jsonify(dechets), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dechets_bp.route("/dechets/<dechet_id>/assign-citoyen/<citoyen_id>", methods=["POST"])
def assign_citoyen_to_dechet(dechet_id, citoyen_id):
    try:
        # Récupérer l'URI du déchet
        dechet_ref = EX1[dechet_id]
        citoyen_ref = EX1[citoyen_id]

        # Vérifier si le déchet existe
        if (dechet_ref, None, None) not in g:
            return jsonify({"error": f"Déchet {dechet_id} introuvable"}), 404

        # Ajouter la relation generatedBy
        g.set((dechet_ref, EX1.generatedBy, citoyen_ref))  # set remplace si existe

        # Sauvegarder le TTL
        g.serialize(destination=RDF_FILE, format="turtle")

        return jsonify({"status": "success", "message": f"Déchet {dechet_id} assigné à {citoyen_id}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@dechets_bp.route("/dechets", methods=["GET"])
def get_all_dechets():
    """
    🧩 Récupère tous les déchets depuis le fichier dechet.ttl
    et inclut le nom du citoyen qui les a générés
    """
    try:
        dechets = []

        for dechet in g.subjects(RDF.type, EX1.Dechet):
            dechet_data = {"uri": str(dechet)}

            # Récupération des propriétés du déchet
            for prop, name in [
                (EX1.dechetID, "dechetID"),
                (EX1.nomdechet, "nomdechet"),
                (EX1.description, "description"),
                (EX1.couleur, "couleur"),
                (EX1.poids, "poids"),
                (EX1.isrecyclable, "isrecyclable"),
                (EX1.quantite, "quantite"),
                (EX1.generatedDate, "generatedDate"),
                (EX1.categorie, "categorie"),
            ]:
                value = g.value(dechet, prop)
                if value:
                    dechet_data[name] = str(value)

            # Récupération du type spécifique (PlasticWaste, MetalWaste, etc.)
            for t in g.objects(dechet, RDF.type):
                if t != EX1.Dechet:  # ignorer la classe générique
                    t_str = str(t)
                    if "#" in t_str:
                        dechet_data["typeIndividu"] = t_str.split("#")[-1]
                    elif "/" in t_str:
                        dechet_data["typeIndividu"] = t_str.split("/")[-1]

            # 🔹 Récupération du citoyen qui a généré le déchet
            citoyen = g.value(dechet, EX1.generatedBy)
            if citoyen:
                # Extraire le citizenID depuis l'URI
                citizenID = str(citoyen).split("/")[-1]
                dechet_data["citizenID"] = citizenID

                # Chercher le nom du citoyen dans le graphe RDF
                nom_citoyen = None
                for c in g.subjects(RDF.type, EX1.citoyen):
                    c_id = g.value(c, EX1.citizenID)
                    if c_id and str(c_id) == citizenID:
                        nom_citoyen = g.value(c, EX1.neaemcitoyen)
                        break
                if nom_citoyen:
                    dechet_data["citoyenNom"] = str(nom_citoyen)

                dechet_data["citoyenURI"] = str(citoyen)

            dechets.append(dechet_data)

        return jsonify(dechets), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@dechets_bp.route("/dechets/<dechet_id>", methods=["GET"])
def get_dechet_local(dechet_id):
    """
    🔍 Retourne un déchet spécifique depuis le fichier local (dechet.ttl)
    en fonction de son dechetID.
    """
    try:
        # Construire la référence RDF du déchet
        dechet_ref = EX1[dechet_id]

        # Vérifier si ce déchet existe dans le graphe
        if (dechet_ref, RDF.type, EX1.Dechet) not in g:
            return jsonify({"message": f"Déchet '{dechet_id}' non trouvé dans le fichier local"}), 404

        # Créer un dictionnaire pour stocker les informations
        data = {
            "dechetID": dechet_id,
        }

        # Récupérer les propriétés RDF associées à ce déchet
        for prop, name, dtype in [
            (EX1.nomdechet, "nomdechet", str),
            (EX1.description, "description", str),
            (EX1.couleur, "couleur", str),
            (EX1.poids, "poids", float),
            (EX1.isrecyclable, "isrecyclable", lambda v: str(v).lower() == "true"),
            (EX1.quantite, "quantite", float),
            (EX1.generatedDate, "generatedDate", str),
            (EX1.categorie, "categorie", str),
        ]:
            value = g.value(dechet_ref, prop)
            if value is not None:
                try:
                    data[name] = dtype(value)
                except Exception:
                    data[name] = str(value)

        # Retourner le résultat
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dechets_bp.route("/dechets/<dechet_id>", methods=["PUT"])
def update_dechet(dechet_id):
    """
    ♻️ Met à jour un déchet existant dans Fuseki ET dans Protégé (fichier .ttl)
    sans créer un nouveau, tout en préservant les relations (type_of, generatedBy...).
    """
    try:
        data = request.get_json()
        dechet_ref = EX1[dechet_id]

        # --- 🔍 Vérifier existence dans Fuseki ---
        sparql_check = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql_check.setReturnFormat(JSON)
        sparql_check.setQuery(PREFIX + f"""
        SELECT ?type ?dechetID ?typeOf ?generatedBy
        WHERE {{
            <{dechet_ref}> a ?type .
            OPTIONAL {{ <{dechet_ref}> ex:dechetID ?dechetID . }}
            OPTIONAL {{ <{dechet_ref}> ex:type_of ?typeOf . }}
            OPTIONAL {{ <{dechet_ref}> ex:generatedBy ?generatedBy . }}
        }}
        """)
        results = sparql_check.query().convert()

        if not results["results"]["bindings"]:
            return jsonify({"error": f"Déchet '{dechet_id}' introuvable."}), 404

        binding = results["results"]["bindings"][0]
        type_uri = binding.get("type", {}).get("value", str(DECHET_CLASS_URI))
        old_typeOf = binding.get("typeOf", {}).get("value", None)
        old_generatedBy = binding.get("generatedBy", {}).get("value", None)
        old_dechetID = binding.get("dechetID", {}).get("value", dechet_id)

        # --- 🧹 DELETE ciblé ---
        delete_query = PREFIX + f"""
        DELETE {{
            <{dechet_ref}> ex:nomdechet ?nomdechet ;
                           ex:description ?description ;
                           ex:couleur ?couleur ;
                           ex:poids ?poids ;
                           ex:isrecyclable ?isrecyclable ;
                           ex:quantite ?quantite ;
                           ex:generatedDate ?generatedDate ;
                           ex:categorie ?categorie .
        }}
        WHERE {{
            OPTIONAL {{ <{dechet_ref}> ex:nomdechet ?nomdechet . }}
            OPTIONAL {{ <{dechet_ref}> ex:description ?description . }}
            OPTIONAL {{ <{dechet_ref}> ex:couleur ?couleur . }}
            OPTIONAL {{ <{dechet_ref}> ex:poids ?poids . }}
            OPTIONAL {{ <{dechet_ref}> ex:isrecyclable ?isrecyclable . }}
            OPTIONAL {{ <{dechet_ref}> ex:quantite ?quantite . }}
            OPTIONAL {{ <{dechet_ref}> ex:generatedDate ?generatedDate . }}
            OPTIONAL {{ <{dechet_ref}> ex:categorie ?categorie . }}
        }}
        """

        # --- 🧩 INSERT avec préservation des relations ---
        relation_triples = ""
        if old_typeOf:
            relation_triples += f"ex:type_of <{old_typeOf}> ;\n"
        if old_generatedBy:
            relation_triples += f"ex:generatedBy <{old_generatedBy}> ;\n"

        insert_query = PREFIX + f"""
        INSERT DATA {{
            <{dechet_ref}> a <{DECHET_CLASS_URI}> ;
                ex:dechetID "{old_dechetID}"^^xsd:string ;
                {relation_triples}
                ex:nomdechet "{data.get('nomdechet', '')}"^^xsd:string ;
                ex:description "{data.get('description', '')}"^^xsd:string ;
                ex:couleur "{data.get('couleur', '')}"^^xsd:string ;
                ex:poids "{float(data.get('poids', 0))}"^^xsd:float ;
                ex:isrecyclable "{str(data.get('isrecyclable', True)).lower()}"^^xsd:boolean ;
                ex:quantite "{float(data.get('quantite', 0))}"^^xsd:decimal ;
                ex:generatedDate "{data.get('generatedDate', '')}"^^xsd:date ;
                ex:categorie "{data.get('categorie', '')}"^^xsd:string .
        }}
        """

        # --- 💾 Envoyer DELETE + INSERT vers Fuseki ---
        sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql.setMethod(POST)
        sparql.setQuery(delete_query)
        sparql.query()
        sparql.setQuery(insert_query)
        sparql.query()

        # --- 🧹 Mise à jour du graphe local ---
        g.remove((dechet_ref, EX1.nomdechet, None))
        g.remove((dechet_ref, EX1.description, None))
        g.remove((dechet_ref, EX1.couleur, None))
        g.remove((dechet_ref, EX1.poids, None))
        g.remove((dechet_ref, EX1.isrecyclable, None))
        g.remove((dechet_ref, EX1.quantite, None))
        g.remove((dechet_ref, EX1.generatedDate, None))
        g.remove((dechet_ref, EX1.categorie, None))

        g.add((dechet_ref, RDF.type, URIRef(type_uri)))
        g.add((dechet_ref, EX1.dechetID, Literal(old_dechetID, datatype=XSD.string)))
        g.add((dechet_ref, EX1.nomdechet, Literal(data.get("nomdechet", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.description, Literal(data.get("description", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.couleur, Literal(data.get("couleur", ""), datatype=XSD.string)))
        g.add((dechet_ref, EX1.poids, Literal(float(data.get("poids", 0)), datatype=XSD.float)))
        g.add((dechet_ref, EX1.isrecyclable, Literal(bool(data.get("isrecyclable", True)), datatype=XSD.boolean)))
        g.add((dechet_ref, EX1.quantite, Literal(float(data.get("quantite", 0)), datatype=XSD.decimal)))
        g.add((dechet_ref, EX1.generatedDate, Literal(data.get("generatedDate", ""), datatype=XSD.date)))
        g.add((dechet_ref, EX1.categorie, Literal(data.get("categorie", ""), datatype=XSD.string)))

        if old_typeOf:
            g.add((dechet_ref, EX1.type_of, URIRef(old_typeOf)))
        if old_generatedBy:
            g.add((dechet_ref, EX1.generatedBy, URIRef(old_generatedBy)))

        g.serialize(destination=RDF_FILE, format="turtle")

        return jsonify({
            "message": f"✅ Déchet '{dechet_id}' mis à jour proprement (relations préservées).",
            "relations": {
                "type_of": old_typeOf,
                "generatedBy": old_generatedBy
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dechets_bp.route("/dechets/citoyen/<citizen_id>", methods=["GET"])
def get_types_dechets_par_citoyen_id(citizen_id):
    """
    Retourne la liste des types de déchets générés par un citoyen donné (avec son ID)
    """
    types_generes = set()

    # Parcourir tous les déchets
    for dechet in g.subjects(RDF.type, DECHET_CLASS_URI):
        citoyen_ref = g.value(dechet, EX1.generatedBy)
        if not citoyen_ref:
            continue

        c_id = g.value(citoyen_ref, EX1.citizenID)
        if not c_id or str(c_id) != citizen_id:
            continue

        # Récupérer les types spécifiques du déchet
        for t in g.objects(dechet, RDF.type):
            if t != DECHET_CLASS_URI:  # ignorer la classe générique
                type_str = str(t).split("#")[-1] if "#" in str(t) else str(t).split("/")[-1]
                types_generes.add(type_str)

    return list(types_generes)

@dechets_bp.route("/dechets/type/<type_id>", methods=["GET"])
def get_dechets_by_type(type_id):
    """
    Récupère tous les déchets qui ont une object property
    pointant vers un individu de TypeDeDechet donné par son typeID.
    """
    try:
        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setReturnFormat(JSON)

        # 🔹 SPARQL : récupérer tous les déchets qui ont ex:type_of -> individu avec ce typeID
        sparql.setQuery(PREFIX + f"""
        SELECT ?dechet ?dechetID ?nomdechet ?description ?couleur ?poids ?isrecyclable ?quantite ?generatedDate
        WHERE {{
            ?dechet a ex:Dechet ;
                    ex:type_of ?typeIndividu .

            ?typeIndividu ex:typeID "{type_id}"^^xsd:string .

            OPTIONAL {{ ?dechet ex:dechetID ?dechetID . }}
            OPTIONAL {{ ?dechet ex:nomdechet ?nomdechet . }}
            OPTIONAL {{ ?dechet ex:description ?description . }}
            OPTIONAL {{ ?dechet ex:couleur ?couleur . }}
            OPTIONAL {{ ?dechet ex:poids ?poids . }}
            OPTIONAL {{ ?dechet ex:isrecyclable ?isrecyclable . }}
            OPTIONAL {{ ?dechet ex:quantite ?quantite . }}
            OPTIONAL {{ ?dechet ex:generatedDate ?generatedDate . }}
        }}
        """)

        results = sparql.query().convert()

        dechets = []
        for r in results["results"]["bindings"]:
            dechets.append({k: v.get("value") for k, v in r.items()})

        return jsonify(dechets), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DELETE ---
@dechets_bp.route("/dechets/<dechet_id>", methods=["DELETE"])
def delete_dechet(dechet_id):
    dechet_ref = EX1[dechet_id]

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
    waste_ref = EX1[waste_id]

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
    g.add((waste_ref, EX1.dechetID, Literal(waste_id, datatype=XSD.string)))
    g.add((waste_ref, EX1.nomdechet, Literal(data.get('nomdechet',''), datatype=XSD.string)))
    g.add((waste_ref, EX1.description, Literal(data.get('description',''), datatype=XSD.string)))
    g.add((waste_ref, EX1.poids, Literal(data.get('poids',0), datatype=XSD.float)))
    g.add((waste_ref, EX1.isrecyclable, Literal(data.get('isrecyclable', True), datatype=XSD.boolean)))
    g.add((waste_ref, EX1.quantite, Literal(data.get('quantite',0), datatype=XSD.decimal)))
    g.add((waste_ref, EX1.generatedDate, Literal(data.get('generatedDate',''), datatype=XSD.date)))
    g.add((waste_ref, EX1.stockageSpecial, Literal(data.get('stockageSpecial',''), datatype=XSD.string)))
    g.add((waste_ref, EX1.infectieux, Literal(data.get('infectieux', False), datatype=XSD.boolean)))

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
    waste_ref = EX1[waste_id]

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

CITOYEN_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/citoyen")

@dechets_bp.route("/citoyens", methods=["POST"])
def create_citoyen():
    data = request.json
    nom = data.get("neaemcitoyen")
    adresse = data.get("addresscit")
    email = data.get("email")
    telephone = data.get("phoneNumber")

    if not nom:
        return jsonify({"status": "error", "message": "Le nom du citoyen est obligatoire"}), 400

    citoyen_id = "CIT"  + str(len(g) + 1)
    citoyen_ref = EX1[citoyen_id]

    g.add((citoyen_ref, RDF.type, CITOYEN_CLASS_URI))
    g.add((citoyen_ref, EX1["neaemcitoyen"], Literal(nom)))
    if adresse:
        g.add((citoyen_ref, EX1["addresscit"], Literal(adresse)))
    if email:
        g.add((citoyen_ref, EX1["email"], Literal(email)))

    if telephone:
        g.add((citoyen_ref, EX1["phoneNumber"], Literal(str(telephone))))

    g.serialize(destination=RDF_FILE, format="turtle")

    result_item = {
        "id": citoyen_id,
        "neaemcitoyen": nom,
        "addresscit": adresse,
        "email": email,
        "phoneNumber": telephone
    }

    return jsonify({"status": "success", "results": result_item})


@dechets_bp.route("/medicalwaste/<waste_id>", methods=["DELETE"])
def delete_medical_waste(waste_id):
    waste_ref = EX1[waste_id]
    delete_query = PREFIX + f"DELETE WHERE {{ <{waste_ref}> ?p ?o . }}"

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((waste_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ MedicalWaste '{waste_id}' supprimé avec succès."})