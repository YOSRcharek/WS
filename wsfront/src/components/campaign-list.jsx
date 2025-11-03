import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getAllCampagnes,
  deleteCampagne,
} from "../services/campagneService"; // ton service backend

export default function CampaignListPage() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // --- Charger toutes les campagnes ---
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getAllCampagnes();
        if (Array.isArray(data)) {
          setCampaigns(data);
        } else if (data.results) {
          setCampaigns(data.results);
        } else {
          console.warn("Format inattendu :", data);
          setCampaigns([]);
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des campagnes :", error);
        setCampaigns([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // --- Supprimer une campagne ---
  const handleDelete = async (id) => {
    if (window.confirm("Voulez-vous vraiment supprimer cette campagne ?")) {
      try {
        await deleteCampagne(id);
        setCampaigns((prev) => prev.filter((c) => c.campaignID !== id));
      } catch (error) {
        console.error("Erreur lors de la suppression :", error);
      }
    }
  };

  if (loading) {
    return (
      <div className="text-center py-20 text-gray-500">
        Chargement des campagnes...
      </div>
    );
  }

  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* En-tête */}
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800 flex items-center gap-2">
            📢 Liste des Campagnes
          </h2>
          <button
            onClick={() => navigate("/add-campaign")}
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-semibold shadow-sm text-sm"
          >
            ➕ Ajouter
          </button>
        </div>

        {/* Tableau */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-purple-600 text-white">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold">Titre</th>
                  <th className="px-6 py-4 text-left font-semibold">Description</th>
                  <th className="px-6 py-4 text-left font-semibold">Date Début</th>
                  <th className="px-6 py-4 text-left font-semibold">Date Fin</th>
                  <th className="px-6 py-4 text-left font-semibold">Public Cible</th>
                  <th className="px-6 py-4 text-left font-semibold">Événements liés</th>
                  <th className="px-6 py-4 text-left font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {campaigns.length > 0 ? (
                  campaigns.map((camp, idx) => (
                    <tr key={idx} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4">{camp.title || "—"}</td>
                      <td className="px-6 py-4">{camp.descriptioncampa || "—"}</td>
                      <td className="px-6 py-4">{camp.startDate || "—"}</td>
                      <td className="px-6 py-4">{camp.endDate || "—"}</td>
                      <td className="px-6 py-4">{camp.targetAudience || "—"}</td>
                      <td className="px-6 py-4 text-center">
                        {camp.evenements?.length || 0}
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => navigate(`/edit-campaign/${camp.campaignID}`)}
                          className="text-blue-600 hover:underline mr-3"
                        >
                          ✏️ Éditer
                        </button>
                        <button
                          onClick={() => handleDelete(camp.campaignID)}
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
                      colSpan="7"
                    >
                      Aucune campagne trouvée.
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
