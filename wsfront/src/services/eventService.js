// src/services/eventService.js
const API_URL = "http://127.0.0.1:5000/evenements"; // ton endpoint Flask

// --- GET tous les événements ---
export const getEvenements = async () => {
  const res = await fetch(API_URL);
  return res.json();
};

// --- GET un événement par ID ---
export const getEvenement = async (id) => {
  const res = await fetch(`${API_URL}/${id}`);
  return res.json();
};

// --- POST nouvel événement ---
export const addEvenement = async (eventData) => {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(eventData),
  });
  return res.json();
};

// --- PUT / UPDATE événement ---
export const updateEvenement = async (id, eventData) => {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(eventData),
  });
  return res.json();
};

// --- DELETE événement ---
export const deleteEvenement = async (id) => {
  const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  return res.json();
};

export const getStats = async () => {
  const res = await fetch(`http://127.0.0.1:5000/stats`);
  if (!res.ok) throw new Error("Erreur lors de la récupération des statistiques");
  return res.json();
};
<<<<<<< HEAD

export const generateAndExecuteSPARQL = async (prompt) => {
  const res = await fetch("http://localhost:5000/sparql-generator", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }), 
  });
  if (!res.ok) {
    throw new Error(`Erreur : ${res.statusText}`);
  }
  return res.json(); 
};
// --- GET campagne par événement ID ---
export const getCampagneByEvenement = async (evenementId) => {
  const res = await fetch(`http://127.0.0.1:5000/evenements/${evenementId}/campagne`);
  if (!res.ok) {
    throw new Error(`Erreur lors de la récupération de la campagne pour l'événement ${evenementId}`);
  }
  return res.json();
};

export const getParticipantsByEvenement = async (evenementId) => {
  const res = await fetch(`http://127.0.0.1:5000/evenements/${evenementId}/participants`);
  if (!res.ok) {
    throw new Error(`Erreur lors de la récupération des participants pour l'événement ${evenementId}`);
  }
  return res.json();
};

export const associerCitoyenAEvenement = async (evenementId, citoyenId) => {
  const res = await fetch(`http://127.0.0.1:5000/evenements/${evenementId}/associer-citoyen/${citoyenId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Erreur lors de l'association du citoyen '${citoyenId}' à l'événement '${evenementId}'`);
  }

  return res.json();
};

// --- GET tous les citoyens ---
export const getAllCitoyens = async () => {
  const res = await fetch("http://127.0.0.1:5000/citoyens");
  
  if (!res.ok) {
    throw new Error(`Erreur lors de la récupération des citoyens: ${res.statusText}`);
  }

  return res.json();
};
=======
>>>>>>> doua
