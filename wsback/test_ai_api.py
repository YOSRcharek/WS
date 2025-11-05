#!/usr/bin/env python3
"""Test de l'API AI SPARQL"""

import requests
import json

def test_ai_api():
    """Test l'API avec différentes demandes"""
    
    base_url = "http://localhost:5001"
    
    # Test 1: Ajout camion benne
    print("🧪 Test 1: Ajout camion benne")
    demande1 = "faire l'ajout d'un camion benne avec ces informations nom dd, capacité 400.0, volume benne 700.0, état disponible, localisation gggg, service assigné CD17255"
    
    response1 = requests.post(f"{base_url}/api/process", 
                             json={"demande": demande1})
    
    print(f"Status: {response1.status_code}")
    print(f"Response: {json.dumps(response1.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    # Test 2: Ajout véhicule simple
    print("🧪 Test 2: Ajout véhicule")
    demande2 = "ajouter un véhicule nom truck01, capacité 500.0, état disponible, localisation paris"
    
    response2 = requests.post(f"{base_url}/api/process", 
                             json={"demande": demande2})
    
    print(f"Status: {response2.status_code}")
    print(f"Response: {json.dumps(response2.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    # Test 3: Recherche véhicule
    print("🧪 Test 3: Recherche véhicule")
    demande3 = "recherche véhicule localisation paris"
    
    response3 = requests.post(f"{base_url}/api/process", 
                             json={"demande": demande3})
    
    print(f"Status: {response3.status_code}")
    print(f"Response: {json.dumps(response3.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    # Test 4: Demande non reconnue
    print("🧪 Test 4: Demande non reconnue")
    demande4 = "supprimer tous les véhicules"
    
    response4 = requests.post(f"{base_url}/api/process", 
                             json={"demande": demande4})
    
    print(f"Status: {response4.status_code}")
    print(f"Response: {json.dumps(response4.json(), indent=2, ensure_ascii=False)}")
    print("-" * 50)
    
    # Test 5: Exemples disponibles
    print("🧪 Test 5: Exemples disponibles")
    response5 = requests.get(f"{base_url}/api/examples")
    
    print(f"Status: {response5.status_code}")
    print(f"Response: {json.dumps(response5.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    try:
        test_ai_api()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: L'API n'est pas accessible. Assurez-vous qu'elle est démarrée sur le port 5001")
    except Exception as e:
        print(f"❌ Erreur: {e}")