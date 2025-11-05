from flask import Blueprint, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON, POST
from rdflib import Literal, URIRef
from rdflib.namespace import RDF, XSD
from config import g, EX, PREFIX, FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, RDF_FILE
import uuid
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

citizen_requests_bp = Blueprint("citizen_requests_bp", __name__)

@citizen_requests_bp.route("/citizen-requests", methods=["POST"])
def create_citizen_request():
    data = request.json
    request_id = "REQ" + str(uuid.uuid4().int)[:6]
    request_ref = EX[request_id]
    
    # Insert into Fuseki
    insert_query = PREFIX + f"""
    INSERT DATA {{
        {request_ref.n3()} a ex:CitizenRequest ;
            ex:requestID "{request_id}"^^xsd:string ;
            ex:citizenName "{data.get('citizenName', '')}"^^xsd:string ;
            ex:municipalityName "{data.get('municipalityName', '')}"^^xsd:string ;
            ex:requestType "{data.get('requestType', '')}"^^xsd:string ;
            ex:description "{data.get('description', '')}"^^xsd:string ;
            ex:priority "{data.get('priority', 'Normal')}"^^xsd:string ;
            ex:status "En attente"^^xsd:string ;
            ex:dateCreated "{datetime.now().isoformat()}"^^xsd:dateTime .
    }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(insert_query)
    sparql.query()
    
    # Add to local graph
    g.add((request_ref, RDF.type, EX.CitizenRequest))
    g.add((request_ref, EX.requestID, Literal(request_id, datatype=XSD.string)))
    g.add((request_ref, EX.citizenName, Literal(data.get('citizenName', ''), datatype=XSD.string)))
    g.add((request_ref, EX.municipalityName, Literal(data.get('municipalityName', ''), datatype=XSD.string)))
    g.add((request_ref, EX.requestType, Literal(data.get('requestType', ''), datatype=XSD.string)))
    g.add((request_ref, EX.description, Literal(data.get('description', ''), datatype=XSD.string)))
    g.add((request_ref, EX.priority, Literal(data.get('priority', 'Normal'), datatype=XSD.string)))
    g.add((request_ref, EX.status, Literal("En attente", datatype=XSD.string)))
    g.add((request_ref, EX.dateCreated, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    
    g.serialize(destination=RDF_FILE, format="turtle")
    
    # Send email to municipality
    municipality_email = get_municipality_email(data.get('municipalityName', ''))
    if municipality_email:
        send_email_to_municipality(municipality_email, data, request_id)
    
    return jsonify({"message": "Demande créée avec succès", "requestID": request_id})

@citizen_requests_bp.route("/citizen-requests", methods=["GET"])
def get_all_requests():
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + """
        SELECT ?requestID ?citizenName ?municipalityName ?requestType ?description ?priority ?status ?dateCreated WHERE {
            ?r a ex:CitizenRequest .
            OPTIONAL { ?r ex:requestID ?requestID . }
            OPTIONAL { ?r ex:citizenName ?citizenName . }
            OPTIONAL { ?r ex:municipalityName ?municipalityName . }
            OPTIONAL { ?r ex:requestType ?requestType . }
            OPTIONAL { ?r ex:description ?description . }
            OPTIONAL { ?r ex:priority ?priority . }
            OPTIONAL { ?r ex:status ?status . }
            OPTIONAL { ?r ex:dateCreated ?dateCreated . }
        }
        ORDER BY DESC(?dateCreated)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    requests_list = []
    for r in results["results"]["bindings"]:
        requests_list.append({
            "requestID": r.get("requestID", {}).get("value", ""),
            "citizenName": r.get("citizenName", {}).get("value", ""),
            "municipalityName": r.get("municipalityName", {}).get("value", ""),
            "requestType": r.get("requestType", {}).get("value", ""),
            "description": r.get("description", {}).get("value", ""),
            "priority": r.get("priority", {}).get("value", ""),
            "status": r.get("status", {}).get("value", ""),
            "dateCreated": r.get("dateCreated", {}).get("value", "")
        })
    
    return jsonify(requests_list)

@citizen_requests_bp.route("/citizen-requests/<request_id>/status", methods=["PUT"])
def update_request_status(request_id):
    data = request.json
    new_status = data.get("status", "")
    
    # Update in Fuseki
    update_query = PREFIX + f"""
    DELETE {{ ?r ex:status ?oldStatus }}
    INSERT {{ ?r ex:status "{new_status}"^^xsd:string }}
    WHERE {{ ?r ex:requestID "{request_id}" ; ex:status ?oldStatus }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(update_query)
    sparql.query()
    
    return jsonify({"message": "Statut mis à jour avec succès"})

@citizen_requests_bp.route("/update-status/<request_id>/<new_status>", methods=["GET"])
def update_status_via_email(request_id, new_status):
    # Update in Fuseki
    update_query = PREFIX + f"""
    DELETE {{ ?r ex:status ?oldStatus }}
    INSERT {{ ?r ex:status "{new_status}"^^xsd:string }}
    WHERE {{ ?r ex:requestID "{request_id}" ; ex:status ?oldStatus }}
    """
    
    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setMethod(POST)
    sparql.setQuery(update_query)
    sparql.query()
    
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
    <h2 style="color: #10b981;">Statut mis à jour avec succès!</h2>
    <p>La demande {request_id} a été marquée comme: <strong>{new_status}</strong></p>
    <p>Merci d'avoir traité cette demande citoyenne.</p>
    </body>
    </html>
    """

def get_municipality_email(municipality_name):
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(PREFIX + f"""
        SELECT ?email WHERE {{
            ?m a <http://www.semanticweb.org/msi/ontologies/2025/9/untitled-ontology-34/Municipalite> .
            ?m ex:nom "{municipality_name}" .
            ?m ex:email ?email .
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["email"]["value"]
    return None

def send_email_to_municipality(municipality_email, request_data, request_id):
    try:
        # Email configuration (use Gmail SMTP)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "chamekheya1@gmail.com"
        sender_password = "zwzi htyh segm lffy"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = municipality_email
        msg['Subject'] = f"Nouvelle demande citoyenne - {request_id}"
        
        # Email body with HTML for buttons
        body = f"""
        <html>
        <body>
        <h2>Nouvelle demande citoyenne reçue</h2>
        
        <p><strong>ID de la demande:</strong> {request_id}</p>
        <p><strong>Citoyen:</strong> {request_data.get('citizenName', '')}</p>
        <p><strong>Type de demande:</strong> {request_data.get('requestType', '')}</p>
        <p><strong>Priorité:</strong> {request_data.get('priority', '')}</p>
        
        <p><strong>Description:</strong></p>
        <p>{request_data.get('description', '')}</p>
        
        <div style="margin: 20px 0;">
        <a href="http://127.0.0.1:5000/update-status/{request_id}/En cours" 
           style="background-color: #f59e0b; color: white; padding: 10px 20px; text-decoration: none; margin-right: 10px; border-radius: 5px;">
           Marquer En Cours
        </a>
        <a href="http://127.0.0.1:5000/update-status/{request_id}/Résolu" 
           style="background-color: #10b981; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
           Marquer Résolu
        </a>
        </div>
        
        <p>Cordialement,<br>Système WasteWise</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, municipality_email, text)
        server.quit()
        
        print(f"Email envoyé à {municipality_email}")
        
    except Exception as e:
        print(f"Erreur envoi email: {str(e)}")