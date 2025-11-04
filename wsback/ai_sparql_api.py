#!/usr/bin/env python3
"""API AI pour transformer des demandes en requêtes SPARQL"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, POST, SELECT
import re
import uuid
import requests
from config import FUSEKI_UPDATE_URL, FUSEKI_QUERY_URL, PREFIX

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

class AIQueryProcessor:
    def __init__(self):
        self.patterns = {
            'ajout_camion_benne': {
                'pattern': r'ajout.*camion benne.*nom\s+(\w+).*capacité.*?([\d.]+).*volume.*benne.*?([\d.]+).*état\s+(\w+).*localisation\s+(\w+).*service assigné\s+(\w+)',
                'template': self._create_camion_benne_query
            },
            'ajout_vehicule': {
                'pattern': r'ajout.*véhicule.*nom\s+(\w+).*capacité.*?([\d.]+).*état\s+(\w+).*localisation\s+(\w+)',
                'template': self._create_vehicule_query
            },
            'recherche_vehicule': {
                'pattern': r'recherche.*véhicule.*localisation\s+(\w+)',
                'template': self._search_vehicule_query
            },
            'recherche_camion_service': {
                'pattern': r'donn.*camions?.*benne.*service assigné\s+([\w\s]+)',
                'template': self._search_camion_by_service_query
            }
        }
    
    def _create_camion_benne_query(self, matches):
        nom, capacite, volume_benne, etat, localisation, service = matches
        import time
        camion_tech_id = f"CB{int(time.time() * 1000) % 100000}"
        
        # Trouver le vrai service correspondant
        real_service = find_real_service(service)
        
        query = f"""
        {PREFIX}
        
        INSERT DATA {{
            ex:{camion_tech_id} rdf:type ex:CamionBenne, ex:Equipement ;
                ex:equipementID "{camion_tech_id}" ;
                ex:nomequiement "{nom}" ;
                ex:etat "{etat}" ;
                ex:capacite "{capacite}"^^xsd:decimal ;
                ex:localisation "{localisation}" ;
                ex:volumeBenne "{volume_benne}"^^xsd:decimal ;
                ex:utilisepar ex:{real_service} .
        }}
        """
        return query, f"Camion benne {nom} ajouté avec succès (ID: {camion_tech_id}) - Service: {real_service}"
    
    def _create_vehicule_query(self, matches):
        nom, capacite, etat, localisation = matches
        vehicule_id = f"vehicule_{uuid.uuid4().hex[:8]}"
        
        query = f"""
        {PREFIX}
        
        INSERT DATA {{
            ex:{vehicule_id} rdf:type ex:Vehicule ;
                ex:nom "{nom}" ;
                ex:capacite {capacite} ;
                ex:etat "{etat}" ;
                ex:localisation "{localisation}" .
        }}
        """
        return query, f"Véhicule {nom} ajouté avec succès (ID: {vehicule_id})"
    
    def _search_vehicule_query(self, matches):
        localisation = matches[0]
        
        query = f"""
        {PREFIX}
        
        SELECT ?vehicule ?nom ?capacite ?etat ?type WHERE {{
            ?vehicule rdf:type ?type ;
                ex:nom ?nom ;
                ex:capacite ?capacite ;
                ex:etat ?etat ;
                ex:localisation "{localisation}" .
            FILTER(?type = ex:Vehicule || ?type = ex:CamionBenne)
        }}
        """
        return query, None
    
    def _search_camion_by_service_query(self, matches):
        service = matches[0].strip()
        
        query = f"""
        {PREFIX}
        
        SELECT ?camion ?nom ?capacite ?volumeBenne ?etat ?localisation WHERE {{
            ?camion rdf:type ex:CamionBenne ;
                ex:nomequiement ?nom ;
                ex:capacite ?capacite ;
                ex:volumeBenne ?volumeBenne ;
                ex:etat ?etat ;
                ex:localisation ?localisation ;
                ex:utilisepar ?service .
            FILTER(CONTAINS(LCASE(STR(?service)), LCASE("{service}")))
        }}
        """
        return query, None
    
    def process_request(self, demande):
        """Traite une demande en langage naturel"""
        demande_lower = demande.lower()
        
        for pattern_name, pattern_info in self.patterns.items():
            match = re.search(pattern_info['pattern'], demande_lower)
            if match:
                return pattern_info['template'](match.groups())
        
        return None, "Demande non reconnue. Formats supportés: ajout camion benne, ajout véhicule, recherche véhicule par localisation, recherche camion par service"

def find_real_service(service_id):
    """Trouve la sous-classe qui contient cet ID de service"""
    try:
        # Chercher dans quelle sous-classe se trouve ce serviceID
        query = f"""
        {PREFIX}
        SELECT ?service WHERE {{
            ?service ex:serviceID "{service_id}" ;
                     rdf:type ?type .
            ?type rdfs:subClassOf* ex:ServiceTransport .
        }} LIMIT 1
        """
        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat('json')
        results = sparql.query().convert()
        
        if results["results"]["bindings"]:
            return results["results"]["bindings"][0]["service"]["value"].split('#')[-1]
        
        # Si pas trouvé exactement, chercher par pattern
        query2 = f"""
        {PREFIX}
        SELECT ?service WHERE {{
            ?service rdf:type ?type ;
                     ex:serviceID ?id .
            ?type rdfs:subClassOf* ex:ServiceTransport .
            FILTER(CONTAINS(LCASE(?id), LCASE("{service_id}")))
        }} LIMIT 1
        """
        sparql.setQuery(query2)
        results2 = sparql.query().convert()
        
        if results2["results"]["bindings"]:
            return results2["results"]["bindings"][0]["service"]["value"].split('#')[-1]
        
        return service_id
    except Exception as e:
        print(f"Erreur recherche sous-classe: {e}")
        return service_id

def add_to_flask_api(data, endpoint):
    """Ajoute aussi dans l'API Flask normale"""
    try:
        # Vérifier et corriger le serviceId
        if data.get('serviceId'):
            real_service_id = find_real_service(data['serviceId'])
            data['serviceId'] = real_service_id
            
        response = requests.post(f'http://localhost:5000/api/{endpoint}', json=data)
        return response.status_code == 201
    except:
        return False

def execute_sparql_query(query, is_update=True):
    """Exécute une requête SPARQL"""
    try:
        if is_update:
            sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
            sparql.setQuery(query)
            sparql.setMethod(POST)
            sparql.query()
            return True, "Opération réussie"
        else:
            sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
            sparql.setQuery(query)
            sparql.setReturnFormat('json')
            results = sparql.query().convert()
            return True, results
            
    except Exception as e:
        return False, str(e)

processor = AIQueryProcessor()

@app.route('/api/process', methods=['POST'])
def process_natural_language():
    """Endpoint principal pour traiter les demandes"""
    try:
        data = request.get_json()
        demande = data.get('demande', '')
        
        if not demande:
            return jsonify({'error': 'Demande manquante'}), 400
        
        # Traiter la demande
        query, message = processor.process_request(demande)
        
        if not query:
            return jsonify({'error': message}), 400
        
        # Déterminer si c'est une requête de mise à jour ou de sélection
        is_update = 'INSERT' in query or 'DELETE' in query
        
        # Exécuter la requête SPARQL
        success, result = execute_sparql_query(query, is_update)
        
        # Pas besoin d'ajouter dans l'API Flask car elle lit déjà depuis Fuseki
        
        if success:
            response = {
                'success': True,
                'query_generated': query,
                'message': message if is_update else 'Recherche effectuée',
                'results': result if not is_update else None
            }
        else:
            response = {
                'success': False,
                'error': result,
                'query_generated': query
            }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Retourne des exemples de demandes supportées"""
    examples = [
        {
            'type': 'Ajout camion benne',
            'exemple': 'Ajouter un camion benne avec le nom dd, une capacité de 400.0, un volume de benne de 700.0, un état disponible, une localisation gggg et un service assigné CD17255'
        },
        {
            'type': 'Ajout véhicule',
            'exemple': 'Ajouter un véhicule avec le nom truck01, une capacité de 500.0, un état disponible et une localisation paris'
        },
        {
            'type': 'Recherche véhicule par localisation',
            'exemple': 'Rechercher tous les véhicules dans la localisation paris'
        },
        {
            'type': 'Recherche camion par service',
            'exemple': 'Donner tous les camions benne qui ont leur service assigné Camion Déchets'
        }
    ]
    return jsonify({'examples': examples})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)