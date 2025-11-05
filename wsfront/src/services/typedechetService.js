// src/services/metalWasteService.js
const API_URL = "http://127.0.0.1:5000/metalwaste"; // endpoint Flask pour MetalWaste

// --- 🧩 GET tous les MetalWaste ---
export const getAllMetalWaste = async () => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error("Erreur lors de la récupération des MetalWaste");
  return res.json();
};

// --- 🔍 GET un MetalWaste par ID ---
export const getMetalWaste = async (id) => {
  const res = await fetch(`${API_URL}/${id}`);
  if (!res.ok) throw new Error("Erreur lors de la récupération du MetalWaste");
  return res.json();
};

// --- ➕ POST : ajouter un nouveau MetalWaste ---
export const addMetalWaste = async (metalData) => {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(metalData),
  });
  if (!res.ok) throw new Error("Erreur lors de l’ajout du MetalWaste");
  return res.json();
};

// --- 🔁 PUT : mettre à jour un MetalWaste existant ---
export const updateMetalWaste = async (id, metalData) => {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(metalData),
  });
  if (!res.ok) throw new Error("Erreur lors de la mise à jour du MetalWaste");
  return res.json();
};

// --- ❌ DELETE : supprimer un MetalWaste ---
export const deleteMetalWaste = async (id) => {
  const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Erreur lors de la suppression du MetalWaste");
  return res.json();
};

// --- 🧹 DELETE TOUS les MetalWaste (optionnel) ---
export const deleteAllMetalWaste = async () => {
  const res = await fetch(`${API_URL}/delete_all`, { method: "DELETE" });
  if (!res.ok) throw new Error("Erreur lors de la suppression de tous les MetalWaste");
  return res.json();
};


// src/services/electronicWasteService.js
const API_URL1 = "http://127.0.0.1:5000/electronicwaste"; // endpoint Flask pour ElectronicWaste

// --- 🧩 GET tous les ElectronicWaste ---
export const getAllElectronicWaste = async () => {
  const res = await fetch(API_URL1);
  if (!res.ok) throw new Error("Erreur lors de la récupération des ElectronicWaste");
  return res.json();
};

// --- 🔍 GET un ElectronicWaste par ID ---
export const getElectronicWaste = async (id) => {
  const res = await fetch(`${API_URL1}/${id}`);
  if (!res.ok) throw new Error("Erreur lors de la récupération de l'ElectronicWaste");
  return res.json();
};

// --- ➕ POST : ajouter un nouveau ElectronicWaste ---
export const addElectronicWaste = async (electronicData) => {
  const res = await fetch(API_URL1, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(electronicData),
  });
  if (!res.ok) throw new Error("Erreur lors de l’ajout de l'ElectronicWaste");
  return res.json();
};

// --- 🔁 PUT : mettre à jour un ElectronicWaste existant ---
export const updateElectronicWaste = async (id, electronicData) => {
  const res = await fetch(`${API_URL1}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(electronicData),
  });
  if (!res.ok) throw new Error("Erreur lors de la mise à jour de l'ElectronicWaste");
  return res.json();
};

// --- ❌ DELETE : supprimer un ElectronicWaste ---
export const deleteElectronicWaste = async (id) => {
  const res = await fetch(`${API_URL1}/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Erreur lors de la suppression de l'ElectronicWaste");
  return res.json();
};

// --- 🧹 DELETE TOUS les ElectronicWaste (optionnel) ---
export const deleteAllElectronicWaste = async () => {
  const res = await fetch(`${API_URL1}/delete_all`, { method: "DELETE" });
  if (!res.ok) throw new Error("Erreur lors de la suppression de tous les ElectronicWaste");
  return res.json();
};
