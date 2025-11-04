import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AddWastePage() {
  const navigate = useNavigate(); // hook pour naviguer
  const [formData, setFormData] = useState({
    type: "",
    weight: "",
    location: "",
    description: "",
    date: "",
    status: "en-attente",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Ici tu pourrais faire un POST vers ton API ou mettre à jour le state global
    alert("Déchet ajouté avec succès !");
    setFormData({
      type: "",
      weight: "",
      location: "",
      description: "",
      date: "",
      status: "en-attente",
    });
    navigate("/waste-list"); // navigation vers la liste des déchets
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Ajouter un Déchet
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Type de Déchet
              </label>
              <select
                name="type"
                value={formData.type}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
                required
              >
                <option value="">Sélectionner un type</option>
                <option value="plastique">Plastique</option>
                <option value="verre">Verre</option>
                <option value="papier">Papier/Carton</option>
                <option value="metal">Métal</option>
                <option value="organique">Organique</option>
                <option value="electronique">Électronique</option>
                <option value="dangereux">Dangereux</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Poids (kg)
              </label>
              <input
                name="weight"
                value={formData.weight}
                onChange={handleChange}
                type="number"
                step="0.1"
                placeholder="Ex: 2.5"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Localisation
            </label>
            <input
              name="location"
              value={formData.location}
              onChange={handleChange}
              type="text"
              placeholder="Adresse ou coordonnées"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Détails supplémentaires..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date de Collecte
              </label>
              <input
                name="date"
                value={formData.date}
                onChange={handleChange}
                type="date"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Statut
              </label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
              >
                <option value="en-attente">En Attente</option>
                <option value="collecte">En Collecte</option>
                <option value="traite">Traité</option>
                <option value="recycle">Recyclé</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-4 rounded-xl font-semibold text-lg transition"
          >
            Enregistrer le Déchet
          </button>
        </form>
      </div>
    </div>
  );
}
