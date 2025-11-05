import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDechets, deleteDechet,assignDechetToCitoyen, getCitoyens ,getDechetsByCitoyen,get_all_citoyens } from "../services/dechetService";

export default function WasteListPage() {
  const navigate = useNavigate();
  const [wastes, setWastes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState(""); // 🔍 État pour la recherche
     const [citoyens, setCitoyens] = useState([]); // liste des citoyens
const [selectedCitoyen, setSelectedCitoyen] = useState("");
  const [dechetsCitoyen, setDechetsCitoyen] = useState([]);
  // 🔄 Charger les déchets depuis l'API Flask
  useEffect(() => {
    fetchDechets();
    fetchCitoyens();

  }, []);

  const fetchDechets = async () => {
    try {
      setLoading(true);
      const data = await getDechets();
      setWastes(data);
    } catch (error) {
      console.error("Erreur lors de la récupération des déchets :", error);
    } finally {
      setLoading(false);
    }
  };
  const fetchCitoyens = async () => {
  try {
    const response = await fetch("http://localhost:5000/citoyens"); // URL de ton API Flask
    if (!response.ok) throw new Error("Erreur réseau");
    const data = await response.json(); // récupère les citoyens en JSON
    setCitoyens(data); // met à jour l'état
  } catch (err) {
    console.error("Erreur fetch citoyens:", err);
  }
};
    const filteredWastes = wastes.filter(w =>
    w.nomdechet?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    w.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    w.couleur?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    w.categorie?.toLowerCase().includes(searchTerm.toLowerCase())
  );
   // 📊 Statistiques simples
  const totalDechets = wastes.length;
  const totalPoids = wastes.reduce((sum, w) => sum + (parseFloat(w.poids) || 0), 0);
  const totalQuantite = wastes.reduce((sum, w) => sum + (parseInt(w.quantite) || 0), 0);
  const totalRecyclables = wastes.filter(w => w.isrecyclable === "true").length;
  const totalNonRecyclables = totalDechets - totalRecyclables;

  const handleAssignCitoyen = async (dechetID, citoyenID) => {
    if (!citoyenID) return;
    try {
      await assignDechetToCitoyen(dechetID, citoyenID);
      alert(`Déchet ${dechetID} affecté au citoyen ${citoyenID} !`);
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'affectation : " + err.message);
    }
  };
   const handleSelectCitoyen = async (citoyenId) => {
    setSelectedCitoyen(citoyenId);
    if (!citoyenId) {
      setDechetsCitoyen([]);
      return;
    }
    try {
      const data = await getDechetsByCitoyen(citoyenId);
      setDechetsCitoyen(data);
    } catch (error) {
      console.error(error);
    }
  };
  // 🗑️ Supprimer un déchet
  const handleDelete = async (id) => {
    if (window.confirm("Voulez-vous vraiment supprimer ce déchet ?")) {
      try {
        await deleteDechet(id);
        fetchDechets(); // 🔄 Recharge la liste après suppression
      } catch (error) {
        console.error("Erreur lors de la suppression :", error);
      }
    }
  };

  if (loading) {
    return (
      <div className="text-center py-10 text-gray-600 text-lg">
        Chargement des déchets...
      </div>
    );
  }

  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800">Liste des Déchets</h2>
            <button
            onClick={() => navigate("/aipage")}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + AI prompt
          </button>
          <button
            onClick={() => navigate("/add-waste")}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + Ajouter
          </button>
        
        </div>
          {/* 🔍 Champ de recherche */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Rechercher par nom, description, couleur ou catégorie..."
            className="w-full md:w-1/2 px-4 py-2 border rounded-xl shadow focus:outline-none focus:ring-2 focus:ring-green-600"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
              {/* 📊 Statistiques */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-6 mb-8">
          <div className="bg-green-100 text-green-800 p-4 rounded-xl shadow text-center">
            <div className="text-xl font-bold">{totalDechets}</div>
            <div>Déchets totaux</div>
          </div>
          <div className="bg-blue-100 text-blue-800 p-4 rounded-xl shadow text-center">
            <div className="text-xl font-bold">{totalPoids.toFixed(2)} kg</div>
            <div>Poids total</div>
          </div>
          <div className="bg-purple-100 text-purple-800 p-4 rounded-xl shadow text-center">
            <div className="text-xl font-bold">{totalQuantite}</div>
            <div>Quantité totale</div>
          </div>
          <div className="bg-yellow-100 text-yellow-800 p-4 rounded-xl shadow text-center">
            <div className="text-xl font-bold">{totalRecyclables}</div>
            <div>Recyclables</div>
          </div>
          <div className="bg-red-100 text-red-800 p-4 rounded-xl shadow text-center">
            <div className="text-xl font-bold">{totalNonRecyclables}</div>
            <div>Non recyclables</div>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-green-600 text-white">
                <tr>
                  
                  <th className="px-6 py-4 text-left font-semibold">Nom</th>
                  <th className="px-6 py-4 text-left font-semibold">Description</th>
                  <th className="px-6 py-4 text-left font-semibold">Couleur</th>
                  <th className="px-6 py-4 text-left font-semibold">Poids (kg)</th>
                  <th className="px-6 py-4 text-left font-semibold">Quantité</th>
                  <th className="px-6 py-4 text-left font-semibold">Date</th>
                  <th className="px-6 py-4 text-left font-semibold">Recyclable</th>
             


                  <th className="px-6 py-4 text-left font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {filteredWastes.length > 0 ? (
                  filteredWastes.map((waste, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-6 py-4">{waste.nomdechet || "—"}</td>
                      <td className="px-6 py-4">{waste.description || "—"}</td>
                      <td className="px-6 py-4">{waste.couleur || "—"}</td>
                      <td className="px-6 py-4">{waste.poids || "—"}</td>
                      <td className="px-6 py-4">{waste.quantite || "—"}</td>
                      <td className="px-6 py-4">{waste.generatedDate || "—"}</td>
                      <td className="px-6 py-4">
                        {waste.isrecyclable === "true" ? (
                          <span className="text-green-600 font-semibold">Oui</span>
                        ) : (
                          <span className="text-red-600 font-semibold">Non</span>
                        )}
                      </td>
                      

                      <td className="px-6 py-4 flex space-x-3">
                        <button
                          onClick={() => navigate(`/edit-waste/${waste.dechetID}`)}
                          className="text-blue-500 hover:underline"
                        >
                          Éditer
                        </button>
                        <button
                          onClick={() => handleDelete(waste.dechetID)}
                          className="text-red-500 hover:underline"
                        >
                          Supprimer
                        </button>
<select
  onChange={(e) => handleAssignCitoyen(waste.dechetID, e.target.value)}
  className="border rounded px-2 py-1 text-sm"
>
  <option value="">Affecter à un citoyen</option>
  {citoyens.map((c) => (
    <option
      key={c.citizenID}      // clé unique pour React
      value={c.citizenID}    // value = citizenID pour l'assignation
    >
      {c.neaemcitoyen}       {/* nom du citoyen affiché */}
    </option>
  ))}
</select>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan="10"
                      className="text-center py-6 text-gray-500 italic"
                    >
                      Aucun déchet trouvé.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Liste des Déchets par Citoyen</h2>

        {/* 🔹 Sélection du citoyen */}
        <div className="mb-6">
          <select
            value={selectedCitoyen}
            onChange={(e) => handleSelectCitoyen(e.target.value)}
            className="border rounded px-4 py-2"
          >
            <option value="">Affecter à un citoyen</option>
  {citoyens.map((c) => (
    <option
      key={c.citizenID}      // clé unique pour React
      value={c.citizenID}    // value = citizenID pour l'assignation
    >
      {c.neaemcitoyen}       {/* nom du citoyen affiché */}
    </option>
  ))}
          </select>
        </div>

        {/* 🔹 Tableau des déchets générés par le citoyen */}
        {selectedCitoyen && (
          <div className="bg-white rounded-3xl shadow-xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-green-600 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left font-semibold">Nom</th>
                    <th className="px-6 py-4 text-left font-semibold">Description</th>
                    <th className="px-6 py-4 text-left font-semibold">Couleur</th>
                    <th className="px-6 py-4 text-left font-semibold">Poids</th>
                    <th className="px-6 py-4 text-left font-semibold">Quantité</th>
                    <th className="px-6 py-4 text-left font-semibold">Date</th>
                    <th className="px-6 py-4 text-left font-semibold">Recyclable</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {dechetsCitoyen.length > 0 ? (
                    dechetsCitoyen.map((d, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-6 py-4">{d.nomdechet || "—"}</td>
                        <td className="px-6 py-4">{d.description || "—"}</td>
                        <td className="px-6 py-4">{d.couleur || "—"}</td>
                        <td className="px-6 py-4">{d.poids || "—"}</td>
                        <td className="px-6 py-4">{d.quantite || "—"}</td>
                        <td className="px-6 py-4">{d.generatedDate || "—"}</td>
                        <td className="px-6 py-4">{d.isrecyclable === "true" ? "Oui" : "Non"}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="7" className="text-center py-6 text-gray-500 italic">
                        Aucun déchet généré par ce citoyen.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
    </div>
    
  );
}