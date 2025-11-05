// services/pointsCollecteService.js
const API_URL = "http://localhost:5000/points_collecte"; // URL de ton backend Flask

export const getPointsCollecte = async () => {
  const response = await fetch(API_URL);
  const data = await response.json();

  // Ajouter pointID basé sur name pour correspondre à Flask
  data.results = data.results.map(p => ({
    ...p,
    pointID: "PC_" + (p.name || "").replace(/\s+/g, "_")
  }));

  return data;
};

export const getPointCollecte = async (id) => {
  const response = await fetch(`${API_URL}/${id}`);
  return response.json();
};

export const addPointCollecte = async (pointData) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pointData),
  });
  return response.json();
};

export const updatePointCollecte = async (id, pointData) => {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pointData),
  });
  return response.json();
};

export const deletePointCollecte = async (id) => {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });
  return response.json();
};

// Nouvelle fonction pour l'IA NLP
export const addPointCollecteNLP = async (phrase) => {
  const response = await fetch("http://localhost:5000/points_collecte_nlp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phrase }),
  });
  return response.json();
};

// Nouvelle fonction pour filtrer les points de collecte
export const filterPointsCollecte = async () => {
  const response = await fetch("http://localhost:5000/points_collecte_filtre");
  return response.json();
};
