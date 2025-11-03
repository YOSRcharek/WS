import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getEvenements,
  deleteEvenement,
} from "../services/eventService"; // ton service backend

export default function EventListPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
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

  if (loading) {
    return (
      <div className="text-center py-20 text-gray-500">
        Chargement des événements...
      </div>
    );
  }

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

        {/* Tableau */}
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
                {events.length > 0 ? (
                  events.map((event, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4">{event.nomevent || "—"}</td>
                      <td className="px-6 py-4">{event.dateDebut || "—"}</td>
                      <td className="px-6 py-4">{event.dateFin || "—"}</td>
                      <td className="px-6 py-4">{event.lieu || "—"}</td>
                      <td className="px-6 py-4">{event.typeEvenement || "—"}</td>
                      <td className="px-6 py-4">
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
