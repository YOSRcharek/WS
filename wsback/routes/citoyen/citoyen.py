from flask import Blueprint, jsonify, request
from SPARQLWrapper import SPARQLWrapper, POST, JSON
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE

citoyen_bp = Blueprint("citoyen_bp", __name__)

# URI de la classe Citoyen
CITOYEN_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/citoyen")

# --- CREATE ---
@citoyen_bp.route("/citoyens", methods=["POST"])
def add_citoyen():
    data = request.json
    citizen_id = "C" + str(len(g) + 1)
    citizen_ref = EX[citizen_id]

    insert_query = PREFIX + f"""
    INSERT DATA {{
        {citizen_ref.n3()} a <{CITOYEN_CLASS_URI}> ;
            ex:citizenID "{citizen_id}"^^xsd:string ;
            ex:neaemcitoyen "{data.get('neaemcitoyen','')}"^^xsd:string ;
            ex:addresscit "{data.get('addresscit','')}"^^xsd:string ;
            ex:age "{data.get('age',0)}"^^xsd:integer ;
            ex:email "{data.get('email','')}"^^xsd:string ;
            ex:phoneNumber "{data.get('phoneNumber','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()

    # Mise à jour locale
    g.add((citizen_ref, RDF.type, CITOYEN_CLASS_URI))
    g.add((citizen_ref, EX.citizenID, Literal(citizen_id, datatype=XSD.string)))
    g.add((citizen_ref, EX.neaemcitoyen, Literal(data.get('neaemcitoyen',''), datatype=XSD.string)))
    g.add((citizen_ref, EX.addresscit, Literal(data.get('addresscit',''), datatype=XSD.string)))
    g.add((citizen_ref, EX.age, Literal(data.get('age',0), datatype=XSD.integer)))
    g.add((citizen_ref, EX.email, Literal(data.get('email',''), datatype=XSD.string)))
    g.add((citizen_ref, EX.phoneNumber, Literal(data.get('phoneNumber',''), datatype=XSD.string)))

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"✅ Citoyen '{citizen_id}' ajouté avec succès !"})

# --- READ ALL ---

# --- READ ONE ---
@citoyen_bp.route("/citoyens/<citizen_id>", methods=["GET"])
def get_citoyen(citizen_id):
    # Construire la requête SPARQL
    query = PREFIX + f"""
    SELECT ?citoyen ?citizenID ?namecitoyen ?addresscit ?age ?email ?phoneNumber
    WHERE {{
        ?citoyen ex:citizenID "{citizen_id}"^^xsd:string .  # Assurez-vous que le citizenID correspond exactement
        OPTIONAL {{ ?citoyen ex:namecitoyen ?namecitoyen . }}
        OPTIONAL {{ ?citoyen ex:addresscit ?addresscit . }}
        OPTIONAL {{ ?citoyen ex:age ?age . }}
        OPTIONAL {{ ?citoyen ex:email ?email . }}
        OPTIONAL {{ ?citoyen ex:phoneNumber ?phoneNumber . }}
    }}
    """
    
    # Exécuter la requête SPARQL via le wrapper
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()

        # Vérifier si des résultats ont été trouvés
        if not results["results"]["bindings"]:
            return jsonify({"message": f"Citoyen '{citizen_id}' non trouvé"}), 404

        # Extraire le premier résultat
        r = results["results"]["bindings"][0]
        
        # Construire le dictionnaire de réponse
        citoyen = {
            "citizenID": citizen_id,
            "namecitoyen": r.get("namecitoyen", {}).get("value", "Inconnu"),
            "addresscit": r.get("addresscit", {}).get("value", "Inconnu"),
            "age": r.get("age", {}).get("value", "Inconnu"),
            "email": r.get("email", {}).get("value", "Inconnu"),
            "phoneNumber": r.get("phoneNumber", {}).get("value", "Inconnu")
        }

        return jsonify(citoyen)

    except Exception as e:
        print(f"Erreur lors de la requête SPARQL: {e}")
        return jsonify({"error": "Erreur de serveur."}), 500
# --- UPDATE ---
@citoyen_bp.route("/citoyens/<citizen_id>", methods=["PUT"])
def update_citoyen(citizen_id):
    data = request.json
    citizen_ref = EX[citizen_id]

    delete_query = PREFIX + f"DELETE WHERE {{ <{citizen_ref}> ?p ?o . }}"
    insert_query = PREFIX + f"""
    INSERT DATA {{
        <{citizen_ref}> a ex:Citoyen ;
            ex:citizenID "{citizen_id}"^^xsd:string ;
            ex:neaemcitoyen "{data.get('neaemcitoyen','')}"^^xsd:string ;
            ex:addresscit "{data.get('addresscit','')}"^^xsd:string ;
            ex:age "{data.get('age',0)}"^^xsd:integer ;
            ex:email "{data.get('email','')}"^^xsd:string ;
            ex:phoneNumber "{data.get('phoneNumber','')}"^^xsd:string .
    }}
    """

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()
    sparql.setQuery(insert_query)
    sparql.query()

    return jsonify({"message": f"♻️ Citoyen '{citizen_id}' mis à jour avec succès !"})

# --- DELETE ---
@citoyen_bp.route("/citoyens/<citizen_id>", methods=["DELETE"])
def delete_citoyen(citizen_id):
    citizen_ref = EX[citizen_id]

    delete_query = PREFIX + f"""
    DELETE WHERE {{
        <{citizen_ref}> ?p ?o .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(delete_query)
    sparql.query()

    for triple in list(g.triples((citizen_ref, None, None))):
        g.remove(triple)

    g.serialize(destination=RDF_FILE, format="turtle")
    return jsonify({"message": f"🗑️ Citoyen '{citizen_id}' supprimé avec succès."})