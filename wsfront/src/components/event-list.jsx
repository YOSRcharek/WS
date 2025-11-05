import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getEvenements,
  deleteEvenement,
  generateAndExecuteSPARQL, // Import de la méthode de génération SPARQL
} from "../services/eventService"; // ton service backend

export default function EventListPage() {
  const [events, setEvents] = useState([]);  // État des événements
  const [loading, setLoading] = useState(true); // État de chargement
  const [prompt, setPrompt] = useState(""); // Etat pour la zone de texte du prompt
  const [sparqlResult, setSparqlResult] = useState(null); // Etat pour stocker la réponse de l'IA
  const navigate = useNavigate();

  // --- Charger les événements depuis Flask ---
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getEvenements();
        if (Array.isArray(data)) {
          setEvents(data);
        } else if (data.results) {
          setEvents(data.results);
        } else {
          console.warn("Format inattendu :", data);
          setEvents([]);
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des événements :", error);
        setEvents([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // --- Supprimer un événement ---
  const handleDelete = async (id) => {
    if (window.confirm("Voulez-vous vraiment supprimer cet événement ?")) {
      try {
        await deleteEvenement(id);
        setEvents((prev) => prev.filter((event) => event.evenementID !== id));
      } catch (error) {
        console.error("Erreur lors de la suppression :", error);
      }
    }
  };

  // --- Soumettre le prompt à l'IA ---
  const handleGenerateSPARQL = async () => {
    try {
      const response = await generateAndExecuteSPARQL(prompt);
      if (response && response.results) {
        setSparqlResult(response.results);  // Si la requête renvoie des résultats, les stocker
      }
    } catch (error) {
      console.error("Erreur lors de l'exécution du SPARQL :", error);
      setSparqlResult({ error: "Erreur lors de l'exécution de la requête SPARQL." });
    }
  };

  if (loading) {
    return (
      <div className="text-center py-20 text-gray-500">
        Chargement des événements...
      </div>
    );
  }

  // --- Fusionner les événements existants et les résultats SPARQL ---
  const eventsToDisplay = sparqlResult && sparqlResult.length > 0
    ? sparqlResult  // Si la requête SPARQL a retourné des résultats, les afficher
    : events;       // Sinon, afficher les événements chargés depuis l'API

  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* En-tête */}
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800 flex items-center gap-2">
            📅 Liste des Événements
          </h2>
          <button
            onClick={() => navigate("/add-event")}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-semibold shadow-sm text-sm"
          >
            ➕ Ajouter
          </button>
        </div>

        {/* Zone pour le prompt SPARQL */}
        <div className="mb-8">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Entrez votre prompt pour générer une requête SPARQL :
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition mb-4"
            rows="4"
            placeholder="Exemple : Génère une requête SPARQL pour récupérer les événements à venir."
          />
          <button
            onClick={handleGenerateSPARQL}
            className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded-lg font-semibold"
          >
            Générer SPARQL
          </button>
        </div>

        {/* Affichage de la réponse de l'IA */}
        

        {/* Tableau des événements */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-green-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold">Nom</th>
                  <th className="px-6 py-4 text-left font-semibold">Date Début</th>
                  <th className="px-6 py-4 text-left font-semibold">Date Fin</th>
                  <th className="px-6 py-4 text-left font-semibold">Lieu</th>
                  <th className="px-6 py-4 text-left font-semibold">Type</th>
                  <th className="px-6 py-4 text-left font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {eventsToDisplay.length > 0 ? (
                  eventsToDisplay.map((event, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4">{event.nomevent || "—"}</td>
                      <td className="px-6 py-4">{event.dateDebut || "—"}</td>
                      <td className="px-6 py-4">{event.dateFin || "—"}</td>
                      <td className="px-6 py-4">{event.lieu || "—"}</td>
                      <td className="px-6 py-4">{event.typeEvenement || "—"}</td>
                      <td className="px-6 py-4">
                         <button
                        onClick={() => navigate(`/event/${event.evenementID}`)}
                          className="text-blue-600 hover:underline mr-3"
                        >
                          Details
                        </button>
                        <button
                          onClick={() => navigate(`/edit-event/${event.evenementID}`)}
                          className="text-blue-600 hover:underline mr-3"
                        >
                          ✏️ Éditer
                        </button>
                        <button
                          onClick={() => handleDelete(event.evenementID)}
                          className="text-red-500 hover:underline"
                        >
                          🗑️ Supprimer
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      className="px-6 py-4 text-center text-gray-500"
                      colSpan="6"
                    >
                      Aucun événement trouvé.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
