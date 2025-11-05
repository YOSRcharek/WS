import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { addDechet } from "../services/dechetService";
import emailjs from "@emailjs/browser";

export default function AddWastePage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    typeDechet: "",
    nomdechet: "",
    description: "",
    couleur: "",
    poids: 0,
    isrecyclable: false,
    quantite: 0,
    generatedDate: "",
    categorie: "",
  });

  const [typesDechets, setTypesDechets] = useState([]);
  const [errors, setErrors] = useState({});

  // 🔹 Charger les types de déchets depuis le backend
  useEffect(() => {
    fetch("http://127.0.0.1:5000/dechets/sousclasses/individus")
      .then((res) => res.json())
      .then((data) => {
        const types = data.map((item) => ({
          id: item.typeID,
          label: `${item.sousClasseLabel || item.sousClasse || ""} - ${item.categorie || ""}`,
        }));
        setTypesDechets(types);
      })
      .catch((err) => console.error("Erreur fetch types de déchet:", err));
  }, []);

  // 🔹 Validation d’un champ
  const validateField = (name, value) => {
    switch (name) {
      case "typeDechet":
        return value ? "" : "Sélectionnez un type de déchet";
      case "nomdechet":
        return value.length >= 3 ? "" : "Le nom doit contenir au moins 3 caractères";
      case "poids":
        return value >= 0 ? "" : "Le poids doit être supérieur ou égal à 0";
      case "quantite":
        return value >= 0 ? "" : "La quantité doit être supérieure ou égale à 0";
      case "generatedDate":
        return value ? "" : "Sélectionnez une date";
      default:
        return "";
    }
  };

  // 🔹 Gestion du changement d’un champ
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const val = type === "checkbox" ? checked : value;

    // Mise à jour des données
    setFormData((prev) => ({ ...prev, [name]: val }));

    // Validation en temps réel
    setErrors((prev) => ({ ...prev, [name]: validateField(name, val) }));
  };

  // 🔹 Vérifie si le formulaire est valide (sans setState)
  const isFormValid = () => {
    return Object.keys(formData).every((key) => validateField(key, formData[key]) === "");
  };

  // 🔹 Soumission du formulaire
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isFormValid()) return;

    const selectedType = typesDechets.find((type) => type.id === formData.typeDechet);
    try {
      const payload = { ...formData, categorie: selectedType?.sousClasse || "" };
      await addDechet(formData.typeDechet, payload);

      // Envoi email après ajout
     await emailjs.send(
        "service_69jh4ti",       // Remplace par ton Service ID EmailJS
        "template_t1hm88s",      // Remplace par ton Template ID
        {
          to_email: "aymenkhelifa01@gmail.com",
          nomdechet: formData.nomdechet,
          
        },
        "B2ym1XbY-4rr2KVYB"       // Remplace par ta Public Key
      );

      alert("Déchet ajouté et email envoyé !");
      setFormData({
        typeDechet: "",
        categorie: "",
        nomdechet: "",
        description: "",
        couleur: "",
        poids: 0,
        isrecyclable: false,
        quantite: 0,
        generatedDate: "",
      });
      setErrors({});
      navigate("/waste-list");
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'ajout du déchet : " + err.message);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Ajouter un Déchet
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Type de déchet */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Type de Déchet
            </label>
            <select
              name="typeDechet"
              value={formData.typeDechet}
              onChange={handleChange}
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition ${
                errors.typeDechet ? "border-red-500" : "border-gray-200 focus:border-emerald-500"
              }`}
            >
              <option value="">Sélectionner un type</option>
              {typesDechets.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.label}
                </option>
              ))}
            </select>
            {errors.typeDechet && <p className="text-red-500 text-sm mt-1">{errors.typeDechet}</p>}
          </div>

          {/* Nom du déchet */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Nom du Déchet</label>
            <input
              name="nomdechet"
              value={formData.nomdechet}
              onChange={handleChange}
              type="text"
              placeholder="Ex: Bouteille plastique"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition ${
                errors.nomdechet ? "border-red-500" : "border-gray-200 focus:border-emerald-500"
              }`}
            />
            {errors.nomdechet && <p className="text-red-500 text-sm mt-1">{errors.nomdechet}</p>}
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="3"
              placeholder="Détails supplémentaires..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
            />
          </div>

          {/* Couleur */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Couleur</label>
            <input
              name="couleur"
              value={formData.couleur}
              onChange={handleChange}
              type="text"
              placeholder="Ex: blanche"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
            />
          </div>

          {/* Poids & Quantité */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Poids (kg)</label>
              <input
                name="poids"
                value={formData.poids}
                onChange={handleChange}
                type="number"
                step="0.01"
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition ${
                  errors.poids ? "border-red-500" : "border-gray-200 focus:border-emerald-500"
                }`}
              />
              {errors.poids && <p className="text-red-500 text-sm mt-1">{errors.poids}</p>}
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Quantité</label>
              <input
                name="quantite"
                value={formData.quantite}
                onChange={handleChange}
                type="number"
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition ${
                  errors.quantite ? "border-red-500" : "border-gray-200 focus:border-emerald-500"
                }`}
              />
              {errors.quantite && <p className="text-red-500 text-sm mt-1">{errors.quantite}</p>}
            </div>
          </div>

          {/* Recyclable */}
          <div className="flex items-center gap-4">
            <input
              name="isrecyclable"
              type="checkbox"
              checked={formData.isrecyclable}
              onChange={handleChange}
              className="h-5 w-5 text-emerald-500"
            />
            <label className="text-sm font-medium text-gray-700">Recyclable</label>
          </div>

          {/* Date */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Date de génération</label>
            <input
              name="generatedDate"
              value={formData.generatedDate}
              onChange={handleChange}
              type="date"
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition ${
                errors.generatedDate ? "border-red-500" : "border-gray-200 focus:border-emerald-500"
              }`}
            />
            {errors.generatedDate && <p className="text-red-500 text-sm mt-1">{errors.generatedDate}</p>}
          </div>

          {/* Bouton submit */}
          <button
            type="submit"
            disabled={!isFormValid()}
            className={`w-full py-4 rounded-xl font-semibold text-lg transition ${
              isFormValid()
                ? "bg-emerald-500 hover:bg-emerald-600 text-white"
                : "bg-gray-300 text-gray-500 cursor-not-allowed"
            }`}
          >
            Enregistrer le Déchet
          </button>
        </form>
      </div>
    </div>
  );
}
