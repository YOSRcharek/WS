# 🌍 Projet WasteWise : Gestion des Déchets

## Description

WasteWise est une application web dédiée à la gestion des déchets. Ce projet permet de visualiser, interroger et manipuler des données RDF relatives à la gestion des déchets, stockées dans un triple store Apache Jena Fuseki.

## 🚀 Technologies Utilisées

- **Python** 🌐 : Serveur backend pour gérer les requêtes et l'API.
- **React** ⚛️ : Framework frontend pour construire l'interface utilisateur.
- **SPARQL** 🔍 : Langage de requête pour interroger les données RDF.
- **Apache Jena Fuseki** 🗄️ : Triple store pour stocker et gérer les données RDF.
- **RDFLib (Python)** 🐍 : Bibliothèque Python pour manipuler les données RDF.
- **Apache Jena** 📚 : Framework Java pour travailler avec des données RDF.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Python] et la bibliothèque RDFLib

## 🛠️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/YOSRcharek/WS.git
cd WS
```
 ### 2. Installer les dépendances
Pour le backend (Node.js) :

```bash

cd wsback
pip install requirements.txt
```
Pour le frontend (React) :

```bash
cd frontend
npm install
```

### 3. Démarrer Apache Jena Fuseki

```bash
java -jar fuseki-server.jar
```
Accédez à l'interface web de Fuseki à l'adresse [http://localhost:3030]. 

### 4. Démarrer le serveur Python
```bash

cd backend
py app.py

```
### 5. Démarrer l'application React

```bash

cd frontend
npm start
```
## 🖥️ Utilisation

Accédez à l'interface utilisateur via [http://localhost:3000].
Utilisez l'interface pour interroger et manipuler les données RDF relatives à la gestion des déchets.
Testez vos requêtes SPARQL via l'interface Fuseki à [http://localhost:3030].

## 🙌 Acknowledgements
[Apache Jena]
[RDFLib]
[React]
