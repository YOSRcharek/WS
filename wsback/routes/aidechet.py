import re
import uuid
from datetime import date
from flask import Blueprint, request, jsonify
from rdflib import Literal, XSD, URIRef
from rdflib.namespace import RDF
from config import g, EX1, RDF_FILE

# --- Blueprint ---
iadechet_bp = Blueprint("iadechet_bp", __name__)

# --- Classe Dechet ---
DECHET_CLASS_URI = URIRef("http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Dechet")
DECHET_FIELDS = ["nomdechet", "description", "poids", "couleur", "isrecyclable", "quantite", "generatedDate"]

# --- Vérification existence ---
def check_existence_local(nomdechet: str):
    for s in g.subjects(predicate=EX1["nomdechet"], object=Literal(nomdechet)):
        return True
    return False

# --- Extraction helper ---
def extract(prompt_text, pattern, default=""):
    m = re.search(pattern, prompt_text, re.IGNORECASE)
    return m.group(1) if m else default

# --- Génération SELECT filtrée à partir du prompt ---
def build_select_from_prompt_local(prompt: str):
    results = []
    for dechet in g.subjects(RDF.type, DECHET_CLASS_URI):
        data = {}
        for f in DECHET_FIELDS:
            val = g.value(dechet, EX1[f])
            if val:
                data[f] = str(val)

        # --- filtres ---
        if re.search(r"recyclables|recyclable|isrecyclable", prompt, re.IGNORECASE):
            if data.get("isrecyclable", "false").lower() != "true":
                continue

        match = re.search(r"poids\s*<\s*([\d\.]+)", prompt, re.IGNORECASE)
        if match and float(data.get("poids", 0)) >= float(match.group(1)):
            continue

        match = re.search(r"poids\s*>\s*([\d\.]+)", prompt, re.IGNORECASE)
        if match and float(data.get("poids", 0)) <= float(match.group(1)):
            continue

        match = re.search(r"avant\s+'([\d]{4}-[\d]{2}-[\d]{2})'", prompt, re.IGNORECASE)
        if match and data.get("generatedDate") and data["generatedDate"] >= match.group(1):
            continue

        match = re.search(r"après\s+'([\d]{4}-[\d]{2}-[\d]{2})'", prompt, re.IGNORECASE)
        if match and data.get("generatedDate") and data["generatedDate"] <= match.group(1):
            continue

        match = re.search(r"couleur\s+'([^']+)'", prompt, re.IGNORECASE)
        if match and data.get("couleur") and data["couleur"].lower() != match.group(1).lower():
            continue

        match = re.search(r"quantit[eé]\s*<\s*([\d\.]+)", prompt, re.IGNORECASE)
        if match and float(data.get("quantite", 0)) >= float(match.group(1)):
            continue

        match = re.search(r"quantit[eé]\s*>\s*([\d\.]+)", prompt, re.IGNORECASE)
        if match and float(data.get("quantite", 0)) <= float(match.group(1)):
            continue

        # --- Citoyen générateur ---
        citoyen_ref = g.value(dechet, EX1.generatedBy)
        if citoyen_ref:
            nom_citoyen = g.value(citoyen_ref, EX1.nom)
            if nom_citoyen:
                data["generatedBy"] = str(nom_citoyen)

        data["Dechet"] = dechet.split("#")[-1] if "#" in dechet else str(dechet)
        results.append(data)

    return results

# --- Route principale ---
@iadechet_bp.route("/sparql-generator", methods=["POST"])
def generate_and_execute_dechet_local():
    data = request.json
    prompt_text = data.get("prompt", "")

    try:
        # --- SELECT / listing ---
        if "liste" in prompt_text.lower() or "tous les déchets" in prompt_text.lower():
            results = build_select_from_prompt_local(prompt_text)
            return jsonify({"status": "success", "results": results})

        # --- INSERT / ajouter nouveau déchet ---
        elif "ajouter" in prompt_text.lower() or "nouveau déchet" in prompt_text.lower():
            new_id = "DCH" + str(uuid.uuid4().int)[:6]
            dechet_ref = EX1[new_id]

            dechet_data = {
                "dechetID": new_id,
                "nomdechet": extract(prompt_text, r"nomm[eé]?\s+'([^']+)'"),
                "description": extract(prompt_text, r"description\s+'([^']+)'"),
                "poids": float(extract(prompt_text, r"poids\s+([\d\.]+)", "0")),
                "couleur": extract(prompt_text, r"couleur\s+'([^']+)'"),
                "isrecyclable": extract(prompt_text, r"recyclable\s+(true|false|oui|non)").lower() in ["true", "oui","false"],
                "quantite": int(extract(prompt_text, r"quantit[eé]\s+([\d]+)", "1")),
                "generatedDate": extract(prompt_text, r"date\s+'([^']+)'", str(date.today())),
                "generatedBy": extract(prompt_text, r"citoyen\s+'([^']+)'"),
                "type": extract(prompt_text, r"type\s+'([^']+)'")
 
            }

            # --- Ajout dans le graphe RDF ---
            g.add((dechet_ref, RDF.type, DECHET_CLASS_URI))
            for field, val in dechet_data.items():
                if field != "generatedBy":
                    if field in ["poids", "quantite"]:
                        g.add((dechet_ref, EX1[field], Literal(val, datatype=XSD.decimal)))
                    elif field == "isrecyclable":
                        g.add((dechet_ref, EX1[field], Literal(val, datatype=XSD.boolean)))
                    elif field == "generatedDate":
                        g.add((dechet_ref, EX1[field], Literal(val, datatype=XSD.date)))
                    else:
                        g.add((dechet_ref, EX1[field], Literal(val)))
            if dechet_data["type"]:
                type_uri = EX1[dechet_data["type"]]
                g.add((dechet_ref, RDF.type, type_uri))
            # --- Gestion du citoyen ---
            if dechet_data["generatedBy"]:
                nom_citoyen = dechet_data["generatedBy"]
                citoyen = None
                for c in g.subjects(RDF.type, EX1.Citoyen):
                    if str(g.value(c, EX1.nom)) == nom_citoyen:
                        citoyen = c
                        break
                if not citoyen:
                    citoyen_id = "CIT" + str(uuid.uuid4().int)[:6]
                    citoyen = EX1[citoyen_id]
                    g.add((citoyen, RDF.type, EX1.Citoyen))
                    g.add((citoyen, EX1.nom, Literal(nom_citoyen)))
                g.add((dechet_ref, EX1.generatedBy, citoyen))

            # --- Sauvegarde ---
            g.serialize(destination=RDF_FILE, format="turtle")
            return jsonify({"status": "success", "results": [dechet_data]})

        # --- DELETE / supprimer ---
        elif "supprimer" in prompt_text.lower() or "effacer" in prompt_text.lower():
            name_match = re.search(r"nomm[eé]?\s+'([^']+)'", prompt_text)
            if not name_match:
                return jsonify({"status": "error", "message": "Nom du déchet introuvable"}), 400
            dechet_name = name_match.group(1)
            if not check_existence_local(dechet_name):
                return jsonify({"status": "error", "message": f"Le déchet '{dechet_name}' n'existe pas"}), 404

            dechet_refs = list(g.subjects(EX1["nomdechet"], Literal(dechet_name)))
            for dechet_ref in dechet_refs:
                g.remove((dechet_ref, None, None))
            g.serialize(destination=RDF_FILE, format="turtle")
            return jsonify({"status": "success", "message": f"Déchet '{dechet_name}' supprimé"})

        # --- UPDATE / mettre à jour ---
        elif "mettre à jour" in prompt_text.lower() or "update" in prompt_text.lower():
            name_match = re.search(r"nomm[eé]?\s+'([^']+)'", prompt_text)
            if not name_match:
                return jsonify({"status": "error", "message": "Nom du déchet introuvable"}), 400
            dechet_name = name_match.group(1)
            dechet_refs = list(g.subjects(EX1["nomdechet"], Literal(dechet_name)))
            if not dechet_refs:
                return jsonify({"status": "error", "message": f"Le déchet '{dechet_name}' n'existe pas"}), 404
            dechet_ref = dechet_refs[0]

            updates = {
                "poids": re.search(r"poids\s+([\d\.]+)", prompt_text),
                "couleur": re.search(r"couleur\s+'([^']+)'", prompt_text),
                "isrecyclable": re.search(r"recyclable\s+(true|false|oui|non)", prompt_text, re.IGNORECASE),
                "description": re.search(r"description\s+'([^']+)'", prompt_text),
                "quantite": re.search(r"quantit[eé]\s+([\d]+)", prompt_text),
                "generatedDate": re.search(r"date\s+'([^']+)'", prompt_text),
            }

            result_item = {"Dechet": dechet_name}
            for field, match in updates.items():
                if match:
                    g.remove((dechet_ref, EX1[field], None))
                    val = match.group(1)
                    if field in ["poids", "quantite"]:
                        g.add((dechet_ref, EX1[field], Literal(float(val), datatype=XSD.decimal)))
                    elif field == "isrecyclable":
                        g.add((dechet_ref, EX1[field], Literal(val.lower() in ["true", "oui"], datatype=XSD.boolean)))
                    elif field == "generatedDate":
                        g.add((dechet_ref, EX1[field], Literal(val, datatype=XSD.date)))
                    else:
                        g.add((dechet_ref, EX1[field], Literal(val)))
                    result_item[field] = val

            g.serialize(destination=RDF_FILE, format="turtle")
            return jsonify({"status": "success", "results": [result_item]})

        # --- Prompt non reconnu ---
        else:
            return jsonify({"status": "error", "message": "Prompt non reconnu"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
