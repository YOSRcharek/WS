import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCampagne } from "../services/campagneService"; // ✅ Import du service backend

export default function AddCampaignPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: "",
    type: "",
    description: "",
    startDate: "",
    endDate: "",
    target: "",
    goalType: "",
    goalValue: "",
    budget: "",
    actions: "",
    coordinator: "",
    contact: "",
  });

  const [loading, setLoading] = useState(false);

  // 🟢 Gérer les changements des inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // 🟢 Soumettre le formulaire et envoyer au backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const newCampagne = await createCampagne(formData); // 🔥 Appel API vers Flask
      if (newCampagne) {
        alert("✅ Campagne ajoutée avec succès !");
        navigate("/events"); // redirige après ajout
      } else {
        alert("❌ Erreur lors de l'ajout de la campagne.");
      }
    } catch (error) {
      console.error("Erreur handleSubmit:", error);
      alert("⚠️ Erreur de connexion au serveur.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Lancer une Campagne
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nom de la Campagne
              </label>
              <input
                name="title"
                value={formData.title}
                onChange={handleChange}
                type="text"
                placeholder="Ex: Zéro Plastique 2024"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Type de Campagne
              </label>
              <select
                name="type"
                value={formData.type}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                required
              >
                <option value="">Sélectionner un type</option>
                <option value="reduction">Réduction des Déchets</option>
                <option value="recyclage">Promotion du Recyclage</option>
                <option value="sensibilisation">Sensibilisation Environnementale</option>
                <option value="collecte">Collecte Spécialisée</option>
                <option value="education">Éducation Écologique</option>
                <option value="innovation">Innovation Verte</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Description de la Campagne
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Décrivez les objectifs et actions de votre campagne..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
              required
            />
          </div>

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
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
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
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                required
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Public Cible
              </label>
              <select
                name="target"
                value={formData.target}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                required
              >
                <option value="">Sélectionner le public</option>
                <option value="citoyens">Citoyens</option>
                <option value="ecoles">Écoles</option>
                <option value="entreprises">Entreprises</option>
                <option value="municipalites">Municipalités</option>
                <option value="tous">Tous</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Type d'Objectif
              </label>
              <select
                name="goalType"
                value={formData.goalType}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                required
              >
                <option value="">Sélectionner</option>
                <option value="weight">Poids (kg)</option>
                <option value="items">Nombre d'objets</option>
                <option value="participants">Nombre de participants</option>
                <option value="percentage">Pourcentage de réduction</option>
              </select>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Objectif Quantitatif
              </label>
              <input
                name="goalValue"
                type="number"
                value={formData.goalValue}
                onChange={handleChange}
                placeholder="Ex: 10000"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Budget (MAD)
              </label>
              <input
                name="budget"
                type="number"
                value={formData.budget}
                onChange={handleChange}
                placeholder="Ex: 50000"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Actions Prévues
            </label>
            <textarea
              name="actions"
              value={formData.actions}
              onChange={handleChange}
              rows="3"
              placeholder="Listez les principales actions de la campagne..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Coordinateur
              </label>
              <input
                name="coordinator"
                value={formData.coordinator}
                onChange={handleChange}
                type="text"
                placeholder="Nom du coordinateur"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Contact
              </label>
              <input
                name="contact"
                value={formData.contact}
                onChange={handleChange}
                type="email"
                placeholder="email@exemple.com"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full ${
              loading ? "bg-gray-400" : "bg-purple-500 hover:bg-purple-600"
            } text-white py-4 rounded-xl font-semibold text-lg transition`}
          >
            {loading ? "Envoi en cours..." : "Lancer la Campagne"}
          </button>
        </form>
      </div>
    </div>
  );
}
