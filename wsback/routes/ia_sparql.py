import re
import uuid
from flask import Blueprint, request, jsonify
import requests
from dotenv import load_dotenv
import os
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from rdflib import Literal, XSD, URIRef
from rdflib.namespace import RDF
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, RDF_FILE, FUSEKI_QUERY_URL

# --- Blueprint ---
ia_bp = Blueprint("ia_bp", __name__)

# --- Classe Evenement ---
EVENEMENT_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/evenement")

# --- Charger variables d'environnement ---
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# --- Champs reconnus ---
EVENT_FIELDS = [
    "evenement", "nomevent", "dateDebut", "dateFin", "lieu", "descriptionevent",
    "typeEvenement", "nombreBenevoles", "quantitecollecte", "nombreParticipants",
    "publicCible", "zoneCible", "campaign"
]
def check_existence(event_name: str):
    """
    Vérifie si un événement avec un nom donné existe dans Fuseki.
    """
    sparql_check = f"""
    {PREFIX}
    ASK WHERE {{
        ?e a <{EVENEMENT_CLASS_URI}> ;
           ex:nomevent "{event_name}" .
    }}
    """
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(sparql_check)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result.get("boolean", False)


# --- Détection du type de requête ---
def detect_sparql_type(query: str):
    """
    Détecte correctement le type de requête SPARQL, 
    en distinguant DELETE/INSERT/WHERE (UPDATE) d’un vrai DELETE.
    """
    query_no_prefix = re.sub(r'PREFIX\s+\w+:\s*<[^>]+>', '', query, flags=re.IGNORECASE).strip()

    # Si on détecte DELETE + INSERT + WHERE → c’est une mise à jour (UPDATE)
    if re.search(r'delete\s*{.*}\s*insert\s*{.*}\s*where', query_no_prefix, re.IGNORECASE | re.DOTALL):
        return "update"

    # Sinon on garde la détection standard
    match = re.search(r'^(select|ask|insert|delete|update|modify|with)\b', query_no_prefix, re.IGNORECASE)
    return match.group(1).lower() if match else None

def normalize_predicates(sparql_query: str) -> str:
    """
    Corrige les noms des propriétés générées par l'IA pour correspondre à l'ontologie réelle.
    """
    replacements = {
        "ex:name": "ex:nomevent",
        "ex:description": "ex:descriptionevent",
        "ex:type": "ex:typeEvenement",
        "ex:location": "ex:lieu",
        "ex:startDate": "ex:dateDebut",
        "ex:endDate": "ex:dateFin",
        "ex:volunteers": "ex:nombreBenevoles",
        "ex:quantity": "ex:quantitecollecte",
        "ex:participants": "ex:nombreParticipants",
        "ex:targetAudience": "ex:publicCible",
        "ex:targetZone": "ex:zoneCible",
    }

    for wrong, correct in replacements.items():
        sparql_query = re.sub(rf"\b{wrong}\b", correct, sparql_query)
    return sparql_query

# --- Route principale ---
@ia_bp.route("/sparql-generator", methods=["POST"])
def generate_and_execute_sparql():
    data = request.json
    prompt_text = data.get("prompt", "")

    # --- Génération SPARQL via IA ---
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
                    "Tu dois utiliser les classes et propriétés de l'ontologie Campagne et Evenement. "
                    "Si la consigne demande une MISE À JOUR, tu dois toujours produire une requête SPARQL de type "
                    "DELETE/INSERT/WHERE complète, qui supprime l’ancienne valeur et insère la nouvelle. "
                    "Ne génère jamais une simple requête DELETE pour une mise à jour."
                )
            },
           {"role": "user", "content": (
                f"Génère une requête SPARQL complète pour : {prompt_text}. "
                "Si la requête demande une mise à jour ou une modification, utilise la forme DELETE/INSERT/WHERE complète "
                "pour remplacer la valeur existante par la nouvelle. "
                f"Utilise le préfixe suivant : {PREFIX} "
                "Ne mets aucune explication ni texte, uniquement la requête SPARQL correcte et complète sur une seule ligne."
            )}

        ]
    }


    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # --- Extraction de la requête SPARQL ---
        match = re.search(r"```sparql\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
        sparql_query = match.group(1).strip() if match else content.strip()
        sparql_query_clean = " ".join(sparql_query.split())
        sparql_query_clean = normalize_predicates(sparql_query_clean)

        if not sparql_query_clean.lower().startswith("prefix ex:"):
            sparql_query_clean = PREFIX + "\n" + sparql_query_clean

        query_type = detect_sparql_type(sparql_query_clean)
        print("=== SPARQL générée ===\n", sparql_query_clean)

        if not query_type:
            return jsonify({"status": "error", "message": "Type de requête SPARQL non supporté"}), 400

        # === SELECT / ASK ===
        if query_type in ["select", "ask"]:
            sparql_wrapper = SPARQLWrapper(FUSEKI_QUERY_URL)

            # 🔹 Extraire un nom éventuel depuis le prompt
            name_match = re.search(r"nomm[eé]\s+'([^']+)'", prompt_text)
            event_name = name_match.group(1) if name_match else None

            # 🔹 Construire la requête avec ou sans filtre
            filter_clause = f'FILTER(?nomevent = "{event_name}")' if event_name else ""

            sparql_query_clean = f"""
            {PREFIX}
            SELECT ?evenement ?nomevent ?dateDebut ?dateFin ?lieu ?descriptionevent ?typeEvenement
                ?nombreBenevoles ?quantitecollecte ?nombreParticipants ?publicCible ?zoneCible ?campaign
            WHERE {{
                ?evenement a <{EVENEMENT_CLASS_URI}> .
                OPTIONAL {{ ?evenement ex:nomevent ?nomevent . }}
                OPTIONAL {{ ?evenement ex:dateDebut ?dateDebut . }}
                OPTIONAL {{ ?evenement ex:dateFin ?dateFin . }}
                OPTIONAL {{ ?evenement ex:lieu ?lieu . }}
                OPTIONAL {{ ?evenement ex:descriptionevent ?descriptionevent . }}
                OPTIONAL {{ ?evenement ex:typeEvenement ?typeEvenement . }}
                OPTIONAL {{ ?evenement ex:nombreBenevoles ?nombreBenevoles . }}
                OPTIONAL {{ ?evenement ex:quantitecollecte ?quantitecollecte . }}
                OPTIONAL {{ ?evenement ex:nombreParticipants ?nombreParticipants . }}
                OPTIONAL {{ ?evenement ex:publicCible ?publicCible . }}
                OPTIONAL {{ ?evenement ex:zoneCible ?zoneCible . }}
                OPTIONAL {{ ?evenement ex:partOf ?campaign . }}
                {filter_clause}
            }}
            ORDER BY ?evenement
            """

            sparql_wrapper.setQuery(sparql_query_clean)
            sparql_wrapper.setReturnFormat(JSON)
            results = sparql_wrapper.query().convert()

            simplified = []
            for row in results.get("results", {}).get("bindings", []):
                item = {}
                for field in EVENT_FIELDS:
                    if field in row:
                        value = row[field]["value"]
                        if field == "campaign":
                            value = value.split("#")[-1]
                        item[field] = value
                simplified.append(item)
            return jsonify({"status": "success", "results": simplified})

        # === INSERT ===
        elif query_type == "insert":
            new_event_id = "EVT" + str(uuid.uuid4().int)[:6]
            evt_ref = EX[new_event_id]

            event_data = {
                "nomevent": re.search(r"nommé\s+'([^']+)'", prompt_text),
                "dateDebut": re.search(r"début le\s+([\d\-]+)", prompt_text),
                "dateFin": re.search(r"fin le\s+([\d\-]+)", prompt_text),
                "lieu": re.search(r"lieu\s+'([^']+)'", prompt_text),
                "descriptionevent": re.search(r"description\s+'([^']+)'", prompt_text),
                "typeEvenement": re.search(r"type\s+'([^']+)'", prompt_text),
                "nombreBenevoles": re.search(r"(\d+)\s+bénévoles", prompt_text),
                "quantitecollecte": re.search(r"(\d+)\s+kg", prompt_text),
                "nombreParticipants": re.search(r"(\d+)\s+participants", prompt_text),
                "publicCible": re.search(r"public cible\s+'([^']+)'", prompt_text),
                "zoneCible": re.search(r"zone cible\s+'([^']+)'", prompt_text)
            }

            triples = [f"{evt_ref.n3()} a <{EVENEMENT_CLASS_URI}> ."]
            for field, match in event_data.items():
                if match:
                    value = match.group(1)
                    if field in ["nombreBenevoles", "quantitecollecte", "nombreParticipants"]:
                        triples.append(f'{evt_ref.n3()} ex:{field} "{value}"^^xsd:integer .')
                    else:
                        triples.append(f'{evt_ref.n3()} ex:{field} "{value}" .')

            sparql_insert = PREFIX + "\nINSERT DATA {\n" + "\n".join(triples) + "\n}"
            sparql_wrapper = SPARQLWrapper(FUSEKI_UPDATE_URL)
            sparql_wrapper.setMethod(POST)
            sparql_wrapper.setQuery(sparql_insert)
            sparql_wrapper.query()

            # Sauvegarde RDF locale
            g.add((evt_ref, RDF.type, EVENEMENT_CLASS_URI))
            for field, match in event_data.items():
                if match:
                    value = match.group(1)
                    if field in ["nombreBenevoles", "quantitecollecte", "nombreParticipants"]:
                        g.add((evt_ref, EX[field], Literal(int(value), datatype=XSD.integer)))
                    else:
                        g.add((evt_ref, EX[field], Literal(value)))
            g.serialize(destination=RDF_FILE, format="turtle")

            result_item = {f: m.group(1) for f, m in event_data.items() if m}
            result_item["evenement"] = new_event_id
            return jsonify({"status": "success", "results": [result_item]}), 200

       # === DELETE ===
        elif query_type == "delete":
            # 🔍 Extraire le nom de l'événement depuis le prompt
            name_match = re.search(r"nomm[eé]\s+'([^']+)'", prompt_text)
            event_name = name_match.group(1) if name_match else None

            if not event_name:
                return jsonify({
                    "status": "error",
                    "message": "Impossible de détecter le nom de l'événement dans le prompt."
                }), 400

            # Vérification existence
            exists = check_existence(event_name)
            if not exists:
                return jsonify({
                    "status": "error",
                    "message": f"L'événement '{event_name}' n'existe pas dans Fuseki."
                }), 404

            # 🔧 Requête DELETE complète pour supprimer tous les triples liés à cet événement
            sparql_delete = f"""
            {PREFIX}
            DELETE WHERE {{
                ?event ex:nomevent "{event_name}" ;
                    ?p ?o .
            }}
            """

            sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
            sparql.setMethod(POST)
            sparql.setQuery(sparql_delete)
            sparql.query()

            # 🔥 Supprimer aussi localement dans le graphe RDF
            for s, p, o in list(g.triples((None, EX["nomevent"], Literal(event_name)))):
                g.remove((s, None, None))
            g.serialize(destination=RDF_FILE, format="turtle")

            return jsonify({
                "status": "success",
                "message": f"L'événement '{event_name}' a été supprimé avec succès.",
                "sparql": sparql_delete
            }), 200

        # === UPDATE / MODIFY / WITH regroupés ===
        elif query_type in ["update", "modify", "with"]:
            # 🧠 Extraire le nom de l'événement depuis le prompt
            name_match = re.search(r"nomm[eé]\s+'([^']+)'", prompt_text)
            event_name = name_match.group(1) if name_match else None

            # 🧩 Vérification existence avant update
            if event_name:
                exists = check_existence(event_name)
                if not exists:
                    return jsonify({
                        "status": "error",
                        "message": f"L'événement '{event_name}' n'existe pas dans Fuseki. Impossible de le mettre à jour."
                    }), 404

            # 🧩 Correction automatique du mauvais prédicat 'ex:named' → 'ex:nomevent'
            sparql_query_clean = sparql_query_clean.replace("ex:named", "ex:nomevent")

            # ⚙️ Exécution UPDATE / MODIFY / WITH sur Fuseki
            response = requests.post(
                FUSEKI_UPDATE_URL,
                data={"update": sparql_query_clean},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            # ✅ Si l’exécution Fuseki réussit
            if response.status_code == 200:
                if event_name:
                    # 🔎 Vérifier la nouvelle description après la mise à jour
                    verify_query = f"""
                    {PREFIX}
                    SELECT ?desc WHERE {{
                        ?e ex:nomevent "{event_name}" ;
                        ex:descriptionevent ?desc .
                    }}
                    """
                    verify = SPARQLWrapper(FUSEKI_QUERY_URL)
                    verify.setQuery(verify_query)
                    verify.setReturnFormat(JSON)
                    res = verify.query().convert()
                    descriptions = [b["desc"]["value"] for b in res["results"]["bindings"]]
                    new_value = descriptions[-1] if descriptions else None

                    # 🧠 Mettre à jour le graphe local RDF
                    for s, p, o in list(g.triples((None, EX["nomevent"], Literal(event_name)))):
                        g.remove((s, EX["descriptionevent"], None))
                        if new_value:
                            g.add((s, EX["descriptionevent"], Literal(new_value, datatype=XSD.string)))

                    # 💾 Sauvegarde locale pour Protégé
                    g.serialize(destination=RDF_FILE, format="turtle")

                return jsonify({
                    "status": "success",
                    "message": f"Requête SPARQL {query_type.upper()} exécutée avec succès.",
                    "sparql": sparql_query_clean
                }), 200

    # ❌ Erreur Fuseki
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Erreur Fuseki: {response.text}",
                    "sparql": sparql_query_clean
                }), response.status_code
        # === Cas non prévu ===
        else:
            return jsonify({"status": "error", "message": "Type de requête SPARQL non pris en charge."}), 400

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Erreur Fuseki : {str(e)}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

