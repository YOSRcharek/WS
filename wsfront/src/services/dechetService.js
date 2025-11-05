// src/services/dechetService.js
const API_URL = "http://127.0.0.1:5000/dechets"; // ton endpoint Flask pour les déchets

// --- 🧩 GET tous les déchets ---
export const getDechets = async () => {
  const res = await fetch(API_URL);
  if (!res.ok) throw new Error("Erreur lors de la récupération des déchets");
  return res.json();
};

// --- 🔍 GET un déchet par ID ---
export const getDechet = async (id) => {
  const res = await fetch(`${API_URL}/${id}`);
  if (!res.ok) throw new Error("Erreur lors de la récupération du déchet");
  return res.json();
};

// --- ➕ POST : ajouter un nouveau déchet ---
export const addDechet = async (typeId, dechetData) => {
  const res = await fetch(`${API_URL}/${typeId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dechetData),
  });
  if (!res.ok) throw new Error("Erreur lors de l’ajout du déchet");
  return res.json();
};

// --- 🔁 PUT : mettre à jour un déchet existant ---
export const updateDechet = async (id, dechetData) => {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dechetData),
  });
  if (!res.ok) throw new Error("Erreur lors de la mise à jour du déchet");
  return res.json();
};

// --- ❌ DELETE : supprimer un déchet ---
export const deleteDechet = async (id) => {
  const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Erreur lors de la suppression du déchet");
  return res.json();
};

// --- 🧹 DELETE TOUS LES DÉCHETS ---
export const deleteAllDechets = async () => {
  const res = await fetch(`${API_URL}/delete_all`, { method: "DELETE" });
  if (!res.ok) throw new Error("Erreur lors de la suppression de tous les déchets");
  return res.json();
};

// --- 📊 GET statistiques (si tu veux les afficher dans un dashboard) ---
export const getDechetStats = async () => {
  const res = await fetch("http://127.0.0.1:5000/dechets/stats");
  if (!res.ok) throw new Error("Erreur lors de la récupération des statistiques");
  return res.json();
};

// --- 🔹 POST : assigner un déchet à un citoyen ---
export const assignDechetToCitoyen = async (dechetID, citoyenID) => {
  const res = await fetch(`${API_URL}/${dechetID}/assign-citoyen/${citoyenID}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Erreur lors de l'affectation du citoyen au déchet");
  return res.json();
};
const CITOYENS_API_URL = "http://127.0.0.1:5000/citoyens";
// --- 🧑‍🤝‍🧑 GET tous les citoyens ---
export const get_all_citoyens = async () => {
  const res = await fetch(CITOYENS_API_URL);
  if (!res.ok) throw new Error("Erreur lors de la récupération des citoyens");
  return res.json(); // doit retourner [{id, nom}, ...]
};

export const getDechetsByCitoyen = async (citoyenId) => {
  const res = await fetch(`${CITOYENS_API_URL}/${citoyenId}/dechets`);
  if (!res.ok) throw new Error("Erreur lors de la récupération des déchets du citoyen");
  return res.json();
};