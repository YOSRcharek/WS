const express = require('express');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(bodyParser.json());
app.use(cors());

// URL du endpoint SPARQL de Fuseki
const FUSEKI_URL = 'http://localhost:3030/gestionDechets/sparql';

// Lire le fichier SPARQL et séparer les requêtes par '# ---'
const sparqlFile = path.join(__dirname, 'sparql', 'requetes.sparql');
const sparqlQueries = fs.readFileSync(sparqlFile, 'utf8').split('# ---');

// Fonction pour exécuter une requête SPARQL
async function executeSparql(query) {
  try {
    const response = await axios.get(FUSEKI_URL, {
      params: {
        query: query,
        format: 'json'
      }
    });
    return response.data.results.bindings;
  } catch (err) {
    console.error('Erreur Fuseki :', err.message);
    return [];
  }
}

// ======================
// Endpoints REST
// ======================

// 1️⃣ Points de collecte
app.get('/api/points', async (req, res) => {
  const query = sparqlQueries[0];
  const data = await executeSparql(query);
  res.json(data);
});

// 2️⃣ Centres de recyclage
app.get('/api/centres', async (req, res) => {
  const query = sparqlQueries[1];
  const data = await executeSparql(query);
  res.json(data);
});

// 3️⃣ Déchets
app.get('/api/dechets', async (req, res) => {
  const query = sparqlQueries[2];
  const data = await executeSparql(query);
  res.json(data);
});

// 4️⃣ Événements
app.get('/api/evenements', async (req, res) => {
  const query = sparqlQueries[3];
  const data = await executeSparql(query);
  res.json(data);
});

// 5️⃣ Équipements
app.get('/api/equipements', async (req, res) => {
  const query = sparqlQueries[4];
  const data = await executeSparql(query);
  res.json(data);
});

// 6️⃣ Municipalités
app.get('/api/municipalites', async (req, res) => {
  const query = sparqlQueries[5];
  const data = await executeSparql(query);
  res.json(data);
});

// 7️⃣ Services de transport
app.get('/api/services', async (req, res) => {
  const query = sparqlQueries[6];
  const data = await executeSparql(query);
  res.json(data);
});

// 8️⃣ Types de déchets
app.get('/api/types-dechets', async (req, res) => {
  const query = sparqlQueries[7];
  const data = await executeSparql(query);
  res.json(data);
});

// 9️⃣ Points de collecte pleins par municipalité (statistique)
app.get('/api/points-pleins', async (req, res) => {
  const query = sparqlQueries[8];
  const data = await executeSparql(query);
  res.json(data);
});

// 🔟 Volume total de déchets recyclables et non recyclables par type
app.get('/api/stats-dechets', async (req, res) => {
  const query = sparqlQueries[9];
  const data = await executeSparql(query);
  res.json(data);
});

// 1️⃣1️⃣ Parcours d’un déchet : point → centre
app.get('/api/parcours-dechet', async (req, res) => {
  const query = sparqlQueries[10];
  const data = await executeSparql(query);
  res.json(data);
});

// 1️⃣2️⃣ Déchets générés aujourd'hui
app.get('/api/dechets-aujourdhui', async (req, res) => {
  const query = sparqlQueries[11];
  const data = await executeSparql(query);
  res.json(data);
});

// ======================
// Démarrage du serveur
// ======================
app.listen(PORT, () => {
  console.log(`Backend Express prêt sur http://localhost:${PORT}`);
});
