#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000/api"

def test_add_camion_benne():
    """Test d'ajout d'un camion benne"""
    camion_data = {
        "nomEquipement": "Camion Test",
        "etat": "disponible",
        "capacite": 500,
        "localisation": "Tunis Centre",
        "volumeBenne": 15.5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/camions-benne", json=camion_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Erreur lors de l'ajout du camion: {e}")
        return False

def test_add_broyeur():
    """Test d'ajout d'un broyeur"""
    broyeur_data = {
        "nomEquipement": "Broyeur Test",
        "etat": "disponible", 
        "capacite": 200,
        "localisation": "Sfax",
        "typeDechetBroye": "plastique"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/broyeurs", json=broyeur_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Erreur lors de l'ajout du broyeur: {e}")
        return False

def check_ttl_file():
    """Vérifier si le fichier TTL contient les nouveaux équipements"""
    try:
        with open("../../dechet.ttl", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Chercher les derniers équipements ajoutés
        if "CamionBenne" in content and "Broyeur" in content:
            print("✅ Les équipements sont présents dans le fichier TTL")
            return True
        else:
            print("❌ Les équipements ne sont pas dans le fichier TTL")
            return False
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier TTL: {e}")
        return False

if __name__ == "__main__":
    print("=== Test d'ajout d'un camion benne ===")
    success_camion = test_add_camion_benne()
    
    print("\n=== Test d'ajout d'un broyeur ===")
    success_broyeur = test_add_broyeur()
    
    print("\n=== Vérification du fichier TTL ===")
    ttl_ok = check_ttl_file()
    
    if success_camion and success_broyeur and ttl_ok:
        print("\n✅ Tous les tests sont passés!")
    else:
        print("\n❌ Certains tests ont échoué.")