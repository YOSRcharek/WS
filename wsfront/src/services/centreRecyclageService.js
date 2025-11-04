// services/centreRecyclageService.js
const API_URL = "http://localhost:5000/centres";

export const getCentres = async () => {
  const response = await fetch(API_URL);
  const data = await response.json();

  // Ajouter centreID basé sur centerName pour correspondre à Flask
  data.results = data.results.map(c => ({
    ...c,
    centreID: "C" + (c.centerName || "").replace(/\s+/g, "_")
  }));

  return data;
};

export const addCentre = async (centreData) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(centreData),
  });
  return response.json();
};

export const updateCentre = async (id, centreData) => {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(centreData),
  });
  return response.json();
};

export const deleteCentre = async (id) => {
  const response = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });
  return response.json();
};
