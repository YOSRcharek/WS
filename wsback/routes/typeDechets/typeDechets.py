from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD, RDFS
from config import g, EX1, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
# --- TYPE DE DÉCHET ---
typedechets_bp = Blueprint("typedechets_bp", __name__)

TYPE_DE_DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Type_de_dechet")
PREFIX = """PREFIX ex: <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

"""

# --- CREATE ---
@typedechets_bp.route("/typededechet", methods=["POST"])
def add_type_de_dechet():
    data = request.json
    type_id = "TD" + str(len(g) + 1)
    type_ref = EX1[type_id]

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
    g.add((type_ref, EX1.typeID, Literal(type_id, datatype=XSD.string)))
    g.add((type_ref, EX1.categorie, Literal(data.get('categorie',''), datatype=XSD.string)))
    g.add((type_ref, EX1.dureeVie, Literal(data.get('dureeVie',0), datatype=XSD.integer)))
    g.add((type_ref, EX1.toxic, Literal(data.get('toxic', False), datatype=XSD.boolean)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ TypeDeDechet '{type_id}' ajouté avec succès !"})
@typedechets_bp.route("/dechets/sousclasses/individus", methods=["GET"])
def get_individus_sousclasses():
    """
    📜 Afficher tous les individus appartenant à chaque sous-classe de Type_de_dechet,
    avec leurs attributs (categorie, dureeVie, toxic, typeID)
    """
    try:
        data = []

        # --- 1️⃣ Récupérer toutes les sous-classes de Type_de_dechet ---
        sous_classes = list(g.subjects(RDFS.subClassOf, EX1.Type_de_dechet))

        # --- 2️⃣ Pour chaque sous-classe, récupérer ses individus ---
        for sous_classe in sous_classes:
            sous_classe_name = str(sous_classe).split("#")[-1] if "#" in str(sous_classe) else str(sous_classe).split("/")[-1]

            for individu in g.subjects(RDF.type, sous_classe):
                individu_data = {
                    "individu": str(individu),
                    "sousClasse": sous_classe_name
                }

                # --- 3️⃣ Récupérer les attributs optionnels ---
                for prop, name in [
                    (EX1.categorie, "categorie"),
                    (EX1.dureeVie, "dureeVie"),
                    (EX1.toxic, "toxic"),
                    (EX1.typeID, "typeID")
                ]:
                    value = g.value(individu, prop)
                    if value:
                        individu_data[name] = str(value)

                data.append(individu_data)

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
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
    type_ref = EX1[type_id]

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
    type_ref = EX1[type_id]
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
    metal_ref = EX1[metal_id]

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
    g.add((metal_ref, EX1.typeID, Literal(metal_id, datatype=XSD.string)))
    g.add((metal_ref, EX1.typeMetal, Literal(data.get('typeMetal',''), datatype=XSD.string)))
    
    g.add((metal_ref, EX1.categorie, Literal(data.get('categorie',''), datatype=XSD.string)))
    g.add((metal_ref, EX1.dureeVie, Literal(data.get('dureeVie',0), datatype=XSD.integer)))
    g.add((metal_ref, EX1.toxic, Literal(data.get('toxic', False), datatype=XSD.boolean)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ MetalWaste '{metal_id}' ajouté avec succès !"})
# --- READ ALL ---
@typedechets_bp.route("/metalwaste", methods=["GET"])
def get_all_metal_waste():
    """
    ⚙️ Récupère tous les déchets métalliques (MetalWaste)
    depuis le fichier dechet.ttl
    """
    try:
        metals = []

        # Parcours des individus de type ex:MetalWaste
        for metal in g.subjects(RDF.type, EX1.MetalWaste):
            metal_data = {"uri": str(metal)}

            # Récupérer les propriétés disponibles
            for prop, name in [
                
                (EX1.typeMetal, "typeMetal"),
                (EX1.categorie, "categorie"),
                (EX1.dureeVie, "dureeVie"),
                (EX1.toxic, "toxic"),
                (EX1.typeID, "typeID"),
            ]:
                value = g.value(metal, prop)
                if value:
                    metal_data[name] = str(value)

            metals.append(metal_data)

        return jsonify(metals), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- READ ONE ---
@typedechets_bp.route("/metalwaste/<metal_id>", methods=["GET"])
def get_metal_waste(metal_id):
    """
    🔎 Récupère un seul déchet métallique (MetalWaste) par son metalWasteID depuis le fichier local
    """
    try:
        found = False
        data = {}

        # Parcours des individus de type MetalWaste
        for metal in g.subjects(RDF.type, EX1.MetalWaste):
            # Vérifier si le metalWasteID correspond à celui recherché
            id_value = g.value(metal, EX1.typeID)
            if id_value and str(id_value) == metal_id:
                found = True
                data["uri"] = str(metal)

                # Récupérer les propriétés facultatives
                for prop, name in [
                    (EX1.typeID, "typeID"),
                    (EX1.typeMetal, "typeMetal"),
                    (EX1.categorie, "categorie"),
                    (EX1.dureeVie, "dureeVie"),
                    (EX1.toxic, "toxic"),
                    
                ]:
                    value = g.value(metal, prop)
                    if value:
                        data[name] = str(value)
                break

        if not found:
            return jsonify({"message": f"MetalWaste '{metal_id}' non trouvé"}), 404

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# --- UPDATE ---
@typedechets_bp.route("/metalwaste/<metal_id>", methods=["PUT"])
def update_metal_waste(metal_id):
    data = request.get_json()
    metal_ref = EX1[metal_id]

    # 🧠 Récupérer l'ancien typeID dans le graphe local s'il existe
    old_type_id = g.value(metal_ref, EX1.typeID)
    new_type_id = data.get("typeID")

    # Si pas fourni, on garde l'ancien
    if not new_type_id and old_type_id:
        new_type_id = str(old_type_id)

    # --- DELETE ciblé ---
    delete_query = PREFIX + f"""
    DELETE {{
        <{metal_ref}> ex:typeMetal ?typeMetal ;
                      ex:categorie ?categorie ;
                      ex:dureeVie ?dureeVie ;
                      ex:toxic ?toxic ;
                      ex:typeID ?typeID .
    }}
    WHERE {{
        OPTIONAL {{ <{metal_ref}> ex:typeMetal ?typeMetal . }}
        OPTIONAL {{ <{metal_ref}> ex:categorie ?categorie . }}
        OPTIONAL {{ <{metal_ref}> ex:dureeVie ?dureeVie . }}
        OPTIONAL {{ <{metal_ref}> ex:toxic ?toxic . }}
        OPTIONAL {{ <{metal_ref}> ex:typeID ?typeID . }}
    }}
    """

    # --- INSERT avec le typeID préservé ---
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{metal_ref}> a ex:MetalWaste ;
            rdfs:subClassOf ex:Type_de_dechet ;
            ex:typeMetal "{data.get('typeMetal', '')}"^^xsd:string ;
            ex:categorie "{data.get('categorie', '')}"^^xsd:string ;
            ex:dureeVie "{data.get('dureeVie', '')}"^^xsd:string ;
            ex:toxic "{data.get('toxic', '')}"^^xsd:string ;
            ex:typeID "{new_type_id}"^^xsd:string .
    }}
    """

    # --- Mise à jour Fuseki ---
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    # --- Mise à jour locale ---
    g.remove((metal_ref, EX1.typeMetal, None))
    g.remove((metal_ref, EX1.categorie, None))
    g.remove((metal_ref, EX1.dureeVie, None))
    g.remove((metal_ref, EX1.toxic, None))
    g.remove((metal_ref, EX1.typeID, None))

    g.add((metal_ref, RDF.type, EX1.MetalWaste))
    g.add((metal_ref, RDFS.subClassOf, EX1.Type_de_dechet))
    g.add((metal_ref, EX1.typeMetal, Literal(data.get("typeMetal", ""), datatype=XSD.string)))
    g.add((metal_ref, EX1.categorie, Literal(data.get("categorie", ""), datatype=XSD.string)))
    g.add((metal_ref, EX1.dureeVie, Literal(data.get("dureeVie", ""), datatype=XSD.string)))
    g.add((metal_ref, EX1.toxic, Literal(data.get("toxic", ""), datatype=XSD.string)))
    g.add((metal_ref, EX1.typeID, Literal(new_type_id, datatype=XSD.string)))

    g.serialize(destination=RDF_FILE, format="turtle")

    return jsonify({"message": f"♻️ MetalWaste '{metal_id}' mis à jour sans perte de typeID."})



@typedechets_bp.route("/metalwaste/<metal_id>", methods=["DELETE"])
def delete_metal_waste(metal_id):
    """
    🗑️ Supprime un individu MetalWaste dans Fuseki et localement dans dechet.ttl
    """
    metal_ref = EX1[metal_id]

    # --- 1️⃣ Suppression dans Fuseki ---
    delete_query = PREFIX + f"""
    DELETE WHERE {{ <{metal_ref}> ?p ?o . }}
    """

    try:
        sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql.setMethod(POST)
        sparql.setQuery(delete_query)
        sparql.query()
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression dans Fuseki : {str(e)}"}), 500

    # --- 2️⃣ Suppression dans le graphe local ---
    try:
        # Supprime tous les triples liés à ce MetalWaste
        for triple in list(g.triples((metal_ref, None, None))):
            g.remove(triple)

        # Sauvegarde du fichier RDF mis à jour
        g.serialize(destination=RDF_FILE, format="turtle")

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la suppression locale : {str(e)}"}), 500

    # --- ✅ Succès ---
    return jsonify({"message": f"🗑️ MetalWaste '{metal_id}' supprimé avec succès (Fuseki + dechet.ttl)."})


ELECTRONIC_WASTE_CLASS_URI = URIRef(
    "http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/ElectronicWaste"
)

# --- CREATE ---
@typedechets_bp.route("/electronicwaste", methods=["POST"])
def add_electronic_waste():
    data = request.json
    electronic_id = "EWT" + str(len(g) + 1)
    electronic_ref = EX1[electronic_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {electronic_ref.n3()} a <{ELECTRONIC_WASTE_CLASS_URI}> ;
            ex:typeID "{electronic_id}"^^xsd:string ;
            ex:categorie "{data.get('categorie','')}"^^xsd:string ;
            ex:dureeVie "{data.get('dureeVie',0)}"^^xsd:integer ;
            ex:toxic "{str(data.get('toxic', False)).lower()}"^^xsd:boolean;
            ex:typeAppareil "{data.get('typeAppareil','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # Graphe local
    g.add((electronic_ref, RDF.type, ELECTRONIC_WASTE_CLASS_URI))
    g.add((electronic_ref, RDFS.subClassOf, TYPE_DE_DECHET_CLASS_URI))
    g.add((electronic_ref, EX1.typeID, Literal(electronic_id, datatype=XSD.string)))
    g.add((electronic_ref, EX1.typeAppareil, Literal(data.get('typeAppareil',''), datatype=XSD.string)))
    g.add((electronic_ref, EX1.categorie, Literal(data.get('categorie',''), datatype=XSD.string)))
    g.add((electronic_ref, EX1.dureeVie, Literal(data.get('dureeVie',0), datatype=XSD.integer)))
    g.add((electronic_ref, EX1.toxic, Literal(data.get('toxic', False), datatype=XSD.boolean)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ ElectronicWaste '{electronic_id}' ajouté avec succès !"})

@typedechets_bp.route("/electronicwaste", methods=["GET"])
def get_all_electronic_waste():
    """
    🔌 Récupère tous les déchets électroniques (ElectronicWaste)
    directement depuis le fichier dechet.ttl
    """
    try:
        electronic_wastes = []

        # Parcours des individus de type ex:ElectronicWaste
        for elec in g.subjects(RDF.type, EX1.ElectronicWaste):
            elec_data = {"uri": str(elec)}

            # Propriétés à récupérer
            for prop, name in [
                
                (EX1.typeAppareil, "typeAppareil"),
                (EX1.categorie, "categorie"),
                (EX1.dureeVie, "dureeVie"),
                (EX1.toxic, "toxic"),
              
                (EX1.typeID, "typeID"),
            ]:
                value = g.value(elec, prop)
                if value:
                    elec_data[name] = str(value)

            electronic_wastes.append(elec_data)

        return jsonify(electronic_wastes), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# --- READ ONE ---
@typedechets_bp.route("/electronicwaste/<electronic_id>", methods=["GET"])
def get_electronic_waste(electronic_id):
    """
    🔎 Récupère un seul déchet électronique (ElectronicWaste)
    par son electronic_id depuis le fichier local (dechet.ttl)
    """
    try:
        found = False
        data = {}

        # Parcours des individus de type ElectronicWaste
        for ew in g.subjects(RDF.type, EX1.ElectronicWaste):
            # Vérifier si le typeID correspond à celui recherché
            id_value = g.value(ew, EX1.typeID)
            if id_value and str(id_value) == electronic_id:
                found = True
                data["uri"] = str(ew)

                # Récupérer les propriétés facultatives
                for prop, name in [
                    (EX1.typeID, "typeID"),
                    (EX1.typeAppareil, "typeAppareil"),
                    (EX1.categorie, "categorie"),
                    (EX1.dureeVie, "dureeVie"),
                    (EX1.toxic, "toxic"),
                  
                ]:
                    value = g.value(ew, prop)
                    if value:
                        data[name] = str(value)
                break

        if not found:
            return jsonify({"message": f"ElectronicWaste '{electronic_id}' non trouvé"}), 404

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- UPDATE ---
# --- UPDATE ElectronicWaste ---
@typedechets_bp.route("/electronicwaste/<electronic_id>", methods=["PUT"])
def update_electronic_waste(electronic_id):
    """
    ♻️ Met à jour un ElectronicWaste existant dans Fuseki ET localement (Protégé)
    sans créer un nouveau, tout en conservant le typeID.
    """
    try:
        data = request.get_json()
        electronic_ref = EX1[electronic_id]

        # 🧠 Récupérer l'ancien typeID depuis le graphe local
        old_type_id = g.value(electronic_ref, EX1.typeID)
        new_type_id = data.get("typeID")

        # Si non fourni, on garde l'ancien typeID
        if not new_type_id and old_type_id:
            new_type_id = str(old_type_id)

        # --- DELETE ciblé dans Fuseki ---
        delete_query = PREFIX + f"""
        DELETE {{
            <{electronic_ref}> ex:typeAppareil ?typeAppareil ;
                              ex:categorie ?categorie ;
                              ex:dureeVie ?dureeVie ;
                              ex:toxic ?toxic ;
                              ex:recyclable ?recyclable ;
                              ex:typeID ?typeID .
        }}
        WHERE {{
            OPTIONAL {{ <{electronic_ref}> ex:typeAppareil ?typeAppareil . }}
            OPTIONAL {{ <{electronic_ref}> ex:categorie ?categorie . }}
            OPTIONAL {{ <{electronic_ref}> ex:dureeVie ?dureeVie . }}
            OPTIONAL {{ <{electronic_ref}> ex:toxic ?toxic . }}
            OPTIONAL {{ <{electronic_ref}> ex:recyclable ?recyclable . }}
            OPTIONAL {{ <{electronic_ref}> ex:typeID ?typeID . }}
        }}
        """

        # --- INSERT avec les nouvelles valeurs ---
        insert_query = PREFIX + f"""
        INSERT DATA {{
            <{electronic_ref}> a ex:ElectronicWaste ;
                rdfs:subClassOf ex:Type_de_dechet ;
                ex:typeAppareil "{data.get('typeAppareil', '')}"^^xsd:string ;
                ex:categorie "{data.get('categorie', '')}"^^xsd:string ;
                ex:dureeVie "{data.get('dureeVie', '')}"^^xsd:string ;
                ex:toxic "{data.get('toxic', '')}"^^xsd:string ;
           
                ex:typeID "{new_type_id}"^^xsd:string .
        }}
        """

        # --- ⚙️ Envoi vers Fuseki ---
        sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql.setMethod(POST)
        sparql.setQuery(delete_query)
        sparql.query()
        sparql.setQuery(insert_query)
        sparql.query()

        # --- 🧹 Mise à jour locale ---
        g.remove((electronic_ref, EX1.typeAppareil, None))
        g.remove((electronic_ref, EX1.categorie, None))
        g.remove((electronic_ref, EX1.dureeVie, None))
        g.remove((electronic_ref, EX1.toxic, None))
      
        g.remove((electronic_ref, EX1.typeID, None))

        g.add((electronic_ref, RDF.type, EX1.ElectronicWaste))
        g.add((electronic_ref, RDFS.subClassOf, EX1.Type_de_dechet))
        g.add((electronic_ref, EX1.typeAppareil, Literal(data.get("typeAppareil", ""), datatype=XSD.string)))
        g.add((electronic_ref, EX1.categorie, Literal(data.get("categorie", ""), datatype=XSD.string)))
        g.add((electronic_ref, EX1.dureeVie, Literal(data.get("dureeVie", ""), datatype=XSD.string)))
        g.add((electronic_ref, EX1.toxic, Literal(data.get("toxic", ""), datatype=XSD.string)))
       
        g.add((electronic_ref, EX1.typeID, Literal(new_type_id, datatype=XSD.string)))

        # Sauvegarde dans le fichier TTL
        g.serialize(destination=RDF_FILE, format="turtle")

        return jsonify({
            "message": f"♻️ ElectronicWaste '{electronic_id}' mis à jour avec succès (typeID conservé)."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# --- DELETE ElectronicWaste ---
@typedechets_bp.route("/electronicwaste/<electronic_id>", methods=["DELETE"])
def delete_electronic_waste(electronic_id):
    """
    🗑️ Supprime un ElectronicWaste à la fois de Fuseki et du fichier local (dechet.ttl)
    """
    try:
        electronic_ref = EX1[electronic_id]

        # --- 🧹 Suppression dans Fuseki ---
        delete_query = PREFIX + f"""
        DELETE WHERE {{
            <{electronic_ref}> ?p ?o .
        }};
        DELETE WHERE {{
            ?s ?p <{electronic_ref}> .
        }}
        """
        sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
        sparql.setMethod(POST)
        sparql.setQuery(delete_query)
        sparql.query()

        # --- 🧹 Suppression locale dans le graphe ---
        triples_to_remove = list(g.triples((electronic_ref, None, None)))
        for t in triples_to_remove:
            g.remove(t)

        # Supprimer aussi les triples où l’individu est objet (si référencé ailleurs)
        triples_as_object = list(g.triples((None, None, electronic_ref)))
        for t in triples_as_object:
            g.remove(t)

        # Sauvegarde dans le fichier TTL
        g.serialize(destination=RDF_FILE, format="turtle")

        return jsonify({
            "message": f"🗑️ ElectronicWaste '{electronic_id}' supprimé avec succès (Fuseki + dechet.ttl)."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
