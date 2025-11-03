import re
import uuid
from flask import Blueprint, request, jsonify
import requests
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from rdflib import Literal, XSD, URIRef
from rdflib.namespace import RDF
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, RDF_FILE, FUSEKI_QUERY_URL

# --- Blueprint ---
iadechet_bp = Blueprint("iadechet_bp", __name__)

# --- Classe Dechet ---
DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Dechet")

# --- Charger variables d'environnement ---
load_dotenv()
openrouter_api_key ="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"

# --- Champs reconnus ---
DECHET_FIELDS = [
    "nomdechet", "description", "poids", "couleur",
    "isrecyclable", "quantite", "generatedDate"
]

# --- Vérification existence ---
def check_existence(nomdechet: str):
    sparql_check = f"""
    {PREFIX}
    ASK WHERE {{
        ?d a <{DECHET_CLASS_URI}> ;
           ex:nomdechet "{nomdechet}" .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(sparql_check)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result.get("boolean", False)

# --- Détection du type de requête ---
def detect_sparql_type(query: str):
    query_no_prefix = re.sub(r'PREFIX\s+\w+:\s*<[^>]+>', '', query, flags=re.IGNORECASE).strip()
    if re.search(r'delete\s*{.*}\s*insert\s*{.*}\s*where', query_no_prefix, re.IGNORECASE | re.DOTALL):
        return "update"
    match = re.search(r'^(select|ask|insert|delete|update|modify|with)\b', query_no_prefix, re.IGNORECASE)
    return match.group(1).lower() if match else None

# --- Normalisation des prédicats ---
def normalize_predicates(sparql_query: str) -> str:
    replacements = {
        "ex:nom_dechet": "ex:nomdechet",
        "ex:nomDechet": "ex:nomdechet",
        "ex:weight": "ex:poids",
        "ex:color": "ex:couleur",
        "ex:quantity": "ex:quantite",
        "ex:dateCreated": "ex:generatedDate",
        "ex:isrecyclable": "ex:isrecyclable",
        "ex:description": "ex:description",
    }
    for wrong, correct in replacements.items():
        sparql_query = re.sub(rf"\b{wrong}\b", correct, sparql_query)
    sparql_query = re.sub(r"ex:[A-Z]\w+", lambda m: m.group(0).lower(), sparql_query)
    return sparql_query

# --- Route principale ---
@iadechet_bp.route("/sparql-generator", methods=["POST"])
def generate_and_execute_sparql_dechet():
    data = request.json
    prompt_text = data.get("prompt", "")

    # === Étape 1 : Génération SPARQL via IA ===
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es un expert en génération de requêtes SPARQL conformes au standard W3C. "
                    "Tu dois utiliser les classes et propriétés de l'ontologie des Déchets. "
                    "Si la consigne demande une MISE À JOUR, produis toujours une requête DELETE/INSERT/WHERE complète."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Génère une requête SPARQL pour : {prompt_text}. "
                    "Si c’est une modification, utilise DELETE/INSERT/WHERE. "
                    f"Utilise ce préfixe : {PREFIX} "
                    "Aucune explication, seulement la requête SPARQL complète."
                )
            }
        ]
    }

    try:
        # Appel API OpenRouter
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        match = re.search(r"```sparql\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
        sparql_query = match.group(1).strip() if match else content.strip()
        sparql_query_clean = " ".join(sparql_query.split())
        sparql_query_clean = normalize_predicates(sparql_query_clean)
        if not sparql_query_clean.lower().startswith("prefix ex:"):
            sparql_query_clean = PREFIX + "\n" + sparql_query_clean

        query_type = detect_sparql_type(sparql_query_clean)
        if not query_type:
            return jsonify({"status": "error", "message": "Type de requête SPARQL non supporté"}), 400

        # ==================== SELECT / ASK ====================
        if query_type in ["select", "ask"]:
            sparql_wrapper = SPARQLWrapper(FUSEKI_QUERY_URL)

            filters = []
            for field in DECHET_FIELDS:
                # Comparateurs numériques pour poids et quantite
                pattern_num = rf"{field}\s*(<=|>=|<|>|=)\s*([\d\.]+)"
                match_num = re.search(pattern_num, prompt_text, re.IGNORECASE)
                if match_num:
                    op, val = match_num.group(1), match_num.group(2)
                    filters.append(f"?{field} {op} {val}")
                    continue
                # Egalité pour les autres champs
                pattern_eq = rf"{field}\s+'([^']+)'"
                match_eq = re.search(pattern_eq, prompt_text, re.IGNORECASE)
                if match_eq:
                    val = match_eq.group(1)
                    if field == "isrecyclable":
                        val_bool = val.lower() in ["true", "oui"]
                        filters.append(f"?{field} = {str(val_bool).lower()}")
                    else:
                        filters.append(f'?{field} = "{val}"')

            filter_clause = f"FILTER({' && '.join(filters)})" if filters else ""
            optional_lines = "".join([f"OPTIONAL {{ ?Dechet ex:{f} ?{f} . }}\n" for f in DECHET_FIELDS])

            sparql_query_clean = f"""{PREFIX}
SELECT ?Dechet {" ".join("?" + f for f in DECHET_FIELDS)}
WHERE {{
    ?Dechet a <{DECHET_CLASS_URI}> .
    {optional_lines}
    {filter_clause}
}}
ORDER BY ?Dechet
"""
            sparql_wrapper.setQuery(sparql_query_clean)
            sparql_wrapper.setReturnFormat(JSON)
            results = sparql_wrapper.query().convert()

            simplified = []
            for row in results.get("results", {}).get("bindings", []):
                item = {}
                for field in DECHET_FIELDS:
                    if field in row:
                        item[field] = row[field]["value"]
                simplified.append(item)
            return jsonify({"status": "success", "results": simplified})

        # ==================== INSERT ====================
        elif query_type in [ "insert" , "inserer" , "ajouter" ] :
            new_id = "DCH" + str(uuid.uuid4().int)[:6]
            dechet_ref = EX[new_id]
            dechet_data = {
                "nomdechet": re.search(r"nomm[eé]?\s+'([^']+)'", prompt_text),
                "description": re.search(r"description\s+'([^']+)'", prompt_text),
                "poids": re.search(r"poids\s+([\d\.]+)", prompt_text),
                "couleur": re.search(r"couleur\s+'([^']+)'", prompt_text),
                "isrecyclable": re.search(r"recyclable\s+(true|false|oui|non)", prompt_text, re.IGNORECASE),
                "quantite": re.search(r"quantit[eé]\s+([\d]+)", prompt_text),
                "generatedDate": re.search(r"date\s+'([^']+)'", prompt_text),
            }

            triples = [f"{dechet_ref.n3()} a <{DECHET_CLASS_URI}> ."]
            for field, match in dechet_data.items():
                if match:
                    value = match.group(1)
                    if field in ["poids", "quantite"]:
                        triples.append(f'{dechet_ref.n3()} ex:{field} "{value}"^^xsd:decimal .')
                    elif field == "isrecyclable":
                        val = "true" if value.lower() in ["true", "oui"] else "false"
                        triples.append(f'{dechet_ref.n3()} ex:{field} "{val}"^^xsd:boolean .')
                    else:
                        triples.append(f'{dechet_ref.n3()} ex:{field} "{value}" .')

            sparql_insert = PREFIX + "\nINSERT DATA {\n" + "\n".join(triples) + "\n}"
            sparql_wrapper = SPARQLWrapper(FUSEKI_UPDATE_URL)
            sparql_wrapper.setMethod(POST)
            sparql_wrapper.setQuery(sparql_insert)
            sparql_wrapper.query()

            # Local RDF update
            g.add((dechet_ref, RDF.type, DECHET_CLASS_URI))
            for field, match in dechet_data.items():
                if match:
                    val = match.group(1)
                    if field in ["poids", "quantite"]:
                        g.add((dechet_ref, EX[field], Literal(float(val), datatype=XSD.decimal)))
                    elif field == "isrecyclable":
                        g.add((dechet_ref, EX[field], Literal(val.lower() in ["true", "oui"], datatype=XSD.boolean)))
                    else:
                        g.add((dechet_ref, EX[field], Literal(val)))
            g.serialize(destination=RDF_FILE, format="turtle")

            result_item = {f: m.group(1) for f, m in dechet_data.items() if m}

            result_item["Dechet"] = new_id
            if "nomdechet" not in result_item and dechet_data.get("nomdechet"):
                result_item["nomdechet"] = dechet_data["nomdechet"].group(1).strip()
            return jsonify({"status": "success", "results": [result_item]}), 200

        # ==================== DELETE ====================
        elif query_type == "delete":
            name_match = re.search(r"nomm[eé]?\s+'([^']+)'", prompt_text)
            dechet_name = name_match.group(1) if name_match else None
            if not dechet_name:
                return jsonify({"status": "error", "message": "Nom du déchet introuvable."}), 400

            if not check_existence(dechet_name):
                return jsonify({"status": "error", "message": f"Le déchet '{dechet_name}' n'existe pas."}), 404

            sparql_delete = f"""
            {PREFIX}
            DELETE WHERE {{
                ?d ex:nomdechet "{dechet_name}" ;
                   ?p ?o .
            }}
            """
            sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
            sparql.setMethod(POST)
            sparql.setQuery(sparql_delete)
            sparql.query()

            for s, p, o in list(g.triples((None, EX["nomdechet"], Literal(dechet_name)))):
                g.remove((s, None, None))
            g.serialize(destination=RDF_FILE, format="turtle")

            return jsonify({
                "status": "success",
                "message": f"Le déchet '{dechet_name}' a été supprimé.",
                "sparql": sparql_delete
            }), 200

        # ==================== UPDATE ====================
        elif query_type in ["update", "modify", "with"]:
            response = requests.post(
                FUSEKI_UPDATE_URL,
                data={"update": sparql_query_clean},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if response.status_code == 200:
                return jsonify({
                    "status": "success",
                    "message": f"Requête SPARQL {query_type.upper()} exécutée avec succès.",
                    "sparql": sparql_query_clean
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Erreur Fuseki : {response.text}",
                    "sparql": sparql_query_clean
                }), response.status_code

        return jsonify({"status": "error", "message": "Type non pris en charge"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
