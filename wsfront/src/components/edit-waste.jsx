import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

export default function EditDechetPage() {
  const { id } = useParams(); // ID du déchet RDF
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  const [formData, setFormData] = useState({
    nomdechet: "",
    description: "",
    couleur: "",
    quantite: "",
    poids: "",
    generatedDate: "",
    isrecyclable: "",
    typeDeDechet: "",
  });

  // Charger les infos du déchet depuis Fuseki
  useEffect(() => {
    const fetchDechet = async () => {
      try {
        const res = await axios.get(`http://localhost:5000/dechets/${id}`);
        const data = res.data;

        setFormData({
          nomdechet: data.nomdechet || "",
          description: data.description || "",
          couleur: data.couleur || "",
          quantite: data.quantite || "",
          poids: data.poids || "",
          generatedDate: data.generatedDate || "",
          isrecyclable: data.isrecyclable || "",
          typeDeDechet: data.typeDeDechet || "",
        });
      } catch (error) {
        console.error("Erreur lors du chargement du déchet :", error);
        alert("Impossible de charger le déchet.");
      } finally {
        setLoading(false);
      }
    };
    fetchDechet();
  }, [id]);

  // Gérer les champs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Mettre à jour le déchet
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.put(`http://localhost:5000/dechets/${id}`, formData);
      alert("✅ Déchet mis à jour avec succès !");
      navigate("/waste-list");
    } catch (err) {
      console.error("Erreur lors de la mise à jour :", err);
      alert("❌ Erreur lors de la mise à jour du déchet.");
    }
  };

  if (loading) return <div className="text-center py-10 text-gray-600">Chargement...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          ♻️ Modifier un Déchet
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Nom & Couleur */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nom du déchet
              </label>
              <input
                name="nomdechet"
                value={formData.nomdechet}
                onChange={handleChange}
                type="text"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Couleur
              </label>
              <input
                name="couleur"
                value={formData.couleur}
                onChange={handleChange}
                type="text"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              />
            </div>
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
            />
          </div>

          {/* Quantité & Poids */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Quantité
              </label>
              <input
                name="quantite"
                value={formData.quantite}
                onChange={handleChange}
                type="number"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Poids (kg)
              </label>
              <input
                name="poids"
                value={formData.poids}
                onChange={handleChange}
                type="number"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              />
            </div>
          </div>

          {/* Date & Recyclable */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date de génération
              </label>
              <input
                name="generatedDate"
                value={formData.generatedDate}
                onChange={handleChange}
                type="date"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Recyclable ?
              </label>
              <select
                name="isrecyclable"
                value={formData.isrecyclable}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              >
                <option value="">Sélectionner</option>
                <option value="true">Oui</option>
                <option value="false">Non</option>
              </select>
            </div>
          </div>

          {/* Type de déchet */}
        
          {/* Bouton */}
          <button
            type="submit"
            className="w-full bg-green-600 hover:bg-green-700 text-white py-4 rounded-xl font-semibold text-lg transition"
          >
            💾 Mettre à jour le déchet
          </button>
        </form>
      </div>
    </div>
  );
}
