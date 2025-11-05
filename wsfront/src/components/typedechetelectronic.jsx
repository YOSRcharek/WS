import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAllElectronicWaste, deleteElectronicWaste } from "../services/typedechetService";

const getDechetsByType = async (typeID) => {
  const res = await fetch(`http://127.0.0.1:5000/dechets/type/${typeID}`);
  if (!res.ok) throw new Error("Erreur lors de la récupération des déchets");
  return res.json();
};
export default function ElectronicWasteListPage() {
  const navigate = useNavigate();
  const [wastes, setWastes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchElectronicWastes();
  }, []);
  // Modal
  const [modalOpen, setModalOpen] = useState(false);
  const [dechetsList, setDechetsList] = useState([]);
  const [modalTitle, setModalTitle] = useState("");
  const fetchElectronicWastes = async () => {
    try {
      setLoading(true);
      const data = await getAllElectronicWaste();
      setWastes(data);
    } catch (error) {
      console.error("Erreur lors de la récupération des ElectronicWaste :", error);
    } finally {
      setLoading(false);
    }
  };
  const handleViewDechets = async (typeID, typeAppareil) => {
    try {
      const data = await getDechetsByType(typeID);
      setDechetsList(data);
      setModalTitle(`Déchets liés à "${typeAppareil}"`);
      setModalOpen(true);
    } catch (error) {
      console.error("Erreur lors de la récupération des déchets :", error);
      alert("Impossible de récupérer les déchets liés à ce type.");
    }
  };

  if (loading) {
    return (
      <div className="text-center py-10 text-gray-600 text-lg">
        Chargement des ElectronicWaste...
      </div>
    );
  }
  const handleDelete = async (id) => {
    if (window.confirm("Voulez-vous vraiment supprimer ce déchet électronique ?")) {
      try {
        await deleteElectronicWaste(id);
        fetchElectronicWastes();
      } catch (error) {
        console.error("Erreur lors de la suppression :", error);
      }
    }
  };

  if (loading) {
    return (
      <div className="text-center py-10 text-gray-600 text-lg">
        Chargement des ElectronicWaste...
      </div>
    );
  }

  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800">Liste des ElectronicWaste</h2>
          <button
            onClick={() => navigate("/add-electronicwaste")}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + Ajouter
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-800 text-white">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold">Catégorie</th>
                  <th className="px-6 py-4 text-left font-semibold">Durée de Vie</th>
                  <th className="px-6 py-4 text-left font-semibold">Toxique</th>
                  <th className="px-6 py-4 text-left font-semibold">Type Électronique</th>
                  <th className="px-6 py-4 text-left font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {wastes.length > 0 ? (
                  wastes.map((waste, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-6 py-4">{waste.categorie || "—"}</td>
                      <td className="px-6 py-4">{waste.dureeVie || "—"}</td>
                      <td className="px-6 py-4">
                        {waste.toxic === "true" ? (
                          <span className="text-red-600 font-semibold">Oui</span>
                        ) : (
                          <span className="text-green-600 font-semibold">Non</span>
                        )}
                      </td>
                      <td className="px-6 py-4">{waste.typeAppareil || "—"}</td>
                      <td className="px-6 py-4 flex space-x-3">
                       <button
                          onClick={() => handleViewDechets(waste.typeID, waste.typeAppareil)}
                          className="text-purple-500 hover:underline"
                        >
                          Voir Déchets
                        </button>
                        <button
                          onClick={() => navigate(`/edit-electronictype/${waste.typeID}`)}
                          className="text-blue-500 hover:underline"
                        >
                          Éditer
                        </button>
                        <button
                          onClick={() => handleDelete(waste.typeID)}
                          className="text-red-500 hover:underline"
                        >
                          Supprimer
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="text-center py-6 text-gray-500 italic">
                      Aucun ElectronicWaste enregistré pour le moment.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
             {modalOpen && (
  <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-start pt-20 z-50">
    <div className="bg-white rounded-xl shadow-xl w-5/6 max-h-[80vh] overflow-y-auto p-6 relative">
      <h3 className="text-2xl font-bold mb-4"></h3>
      <button
        className="absolute top-4 right-4 text-gray-500 hover:text-gray-800"
        onClick={() => setModalOpen(false)}
      >
        ✕
      </button>

      {dechetsList.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full border border-gray-200">
            <thead className="bg-gray-800 text-white">
              <tr>
                <th className="px-4 py-2 text-left">Nom</th>
                <th className="px-4 py-2 text-left">Description</th>
                <th className="px-4 py-2 text-left">Couleur</th>
                <th className="px-4 py-2 text-left">Poids (kg)</th>
                <th className="px-4 py-2 text-left">Quantité</th>
                <th className="px-4 py-2 text-left">Recyclable</th>
                <th className="px-4 py-2 text-left">Date générée</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {dechetsList.map((d, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-4 py-2">{d.nomdechet || "—"}</td>
                  <td className="px-4 py-2">{d.description || "—"}</td>
                  <td className="px-4 py-2">{d.couleur || "—"}</td>
                  <td className="px-4 py-2">{d.poids || "—"}</td>
                  <td className="px-4 py-2">{d.quantite || "—"}</td>
                  <td className="px-4 py-2">
                    {d.isrecyclable === "true" ? "Oui" : "Non"}
                  </td>
                  <td className="px-4 py-2">{d.generatedDate || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="italic text-gray-500">Aucun déchet lié trouvé.</p>
      )}
    </div>
  </div>
)}
      </div>
    </div>
  );
}
