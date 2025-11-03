import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getCampagneById, updateCampagne } from "../services/campagneService";

export default function EditCampaignPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    title: "",
    descriptioncampa: "",
    contenu: "",
    contenuimage: "",
    image: "",
    lien: "",
    nomPlateforme: "",
    startDate: "",
    endDate: "",
    targetAudience: "",
  });

  const [loading, setLoading] = useState(false);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    const fetchCampagne = async () => {
      try {
        const campagne = await getCampagneById(id);
        if (campagne) {
          setFormData({
            title: campagne.title || "",
            descriptioncampa: campagne.descriptioncampa || "",
            contenu: campagne.contenu || "",
            contenuimage: campagne.contenuimage || "",
            image: campagne.image || "",
            lien: campagne.lien || "",
            nomPlateforme: campagne.nomPlateforme || "",
            startDate: campagne.startDate || "",
            endDate: campagne.endDate || "",
            targetAudience: campagne.targetAudience || "",
          });
        }
      } catch (error) {
        console.error("Erreur fetchCampagne:", error);
      } finally {
        setLoadingData(false);
      }
    };
    fetchCampagne();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const updated = await updateCampagne(id, formData);
      if (updated) {
        alert("✅ Campagne mise à jour avec succès !");
        navigate("/events");
      } else {
        alert("❌ Erreur lors de la mise à jour de la campagne.");
      }
    } catch (error) {
      console.error("Erreur handleSubmit:", error);
      alert("⚠️ Erreur de connexion au serveur.");
    } finally {
      setLoading(false);
    }
  };

  if (loadingData) {
    return <p className="text-center text-gray-500 mt-20">Chargement...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          ✏️ Modifier la Campagne
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Titre */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Nom de la Campagne
            </label>
            <input
              name="title"
              value={formData.title}
              onChange={handleChange}
              type="text"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="descriptioncampa"
              value={formData.descriptioncampa}
              onChange={handleChange}
              rows="4"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
              required
            />
          </div>

          {/* Dates */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date de Début
              </label>
              <input
                name="startDate"
                type="date"
                value={formData.startDate}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date de Fin
              </label>
              <input
                name="endDate"
                type="date"
                value={formData.endDate}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
                required
              />
            </div>
          </div>

          {/* Image + Lien */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Image (URL)
              </label>
              <input
                name="image"
                value={formData.image}
                onChange={handleChange}
                type="text"
                placeholder="https://..."
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Lien associé
              </label>
              <input
                name="lien"
                value={formData.lien}
                onChange={handleChange}
                type="text"
                placeholder="https://..."
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
              />
            </div>
          </div>

          {/* Plateforme et Audience */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nom de la Plateforme
              </label>
              <input
                name="nomPlateforme"
                value={formData.nomPlateforme}
                onChange={handleChange}
                type="text"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Public Cible
              </label>
              <input
                name="targetAudience"
                value={formData.targetAudience}
                onChange={handleChange}
                type="text"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:outline-none transition"
              />
            </div>
          </div>

          {/* Bouton */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full ${
              loading ? "bg-gray-400" : "bg-green-600 hover:bg-green-700"
            } text-white py-4 rounded-xl font-semibold text-lg transition`}
          >
            {loading ? "Mise à jour..." : "Mettre à jour la Campagne"}
          </button>
        </form>
      </div>
    </div>
  );
}
