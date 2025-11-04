// src/services/campagneService.js
const API_BASE_URL = "http://127.0.0.1:5000";

// ============================
// 🔹 GET toutes les campagnes
// ============================
export const getAllCampagnes = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes`);
    const data = await res.json();
    return data; // renvoie un tableau de campagnes
  } catch (error) {
    console.error("Erreur getAllCampagnes:", error);
    return [];
  }
};

// ============================
// 🔹 GET une campagne par ID
// ============================
export const getCampagneById = async (campagneId) => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes/${campagneId}`);
    const data = await res.json();
    return data; // renvoie un objet campagne
  } catch (error) {
    console.error("Erreur getCampagneById:", error);
    return null;
  }
};

// ============================
// 🔹 GET événements par campagne
// ============================
export const getEvenementsByCampagne = async (campagneId) => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes/${campagneId}/evenements`);
    const data = await res.json();
    return data; // renvoie un tableau d'événements
  } catch (error) {
    console.error("Erreur getEvenementsByCampagne:", error);
    return [];
  }
};

// ============================
// 🔹 POST créer une nouvelle campagne
// ============================
export const createCampagne = async (campagneData) => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(campagneData),
    });
    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Erreur createCampagne:", error);
    return null;
  }
};

// ============================
// 🔹 PUT mettre à jour une campagne
// ============================
export const updateCampagne = async (campagneId, campagneData) => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes/${campagneId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(campagneData),
    });
    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Erreur updateCampagne:", error);
    return null;
  }
};

// ============================
// 🔹 DELETE supprimer une campagne
// ============================
export const deleteCampagne = async (campagneId) => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes/${campagneId}`, {
      method: "DELETE",
    });
    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Erreur deleteCampagne:", error);
    return null;
  }
};

export const associateEventToCampagne = async (campagneId, evenementId) => {
  try {
    const res = await fetch(`${API_BASE_URL}/campagnes/${campagneId}/associer_evenement/${evenementId}`, {
      method: "POST",
    });
    const data = await res.json();
    return data; // Message de succès ou d'erreur
  } catch (error) {
    console.error("Erreur associateEventToCampagne:", error);
    return null;
  }
};