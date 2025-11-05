import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { addElectronicWaste } from "../services/typedechetService";

export default function AddElectronicWastePage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    categorie: "",
    typeElectronique: "",
    dureeVie: 0,
    toxic: false,
   
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.categorie || !formData.typeElectronique) {
      alert("Veuillez remplir tous les champs obligatoires !");
      return;
    }

    try {
      console.log("Payload envoyé:", formData);
      await addElectronicWaste(formData);
      alert("ElectronicWaste ajouté avec succès !");
      setFormData({
        categorie: "",
        typeElectronique: "",
        dureeVie: 0,
        toxic: false,
       
      });
      navigate("/waste-electronic");
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'ajout de l'ElectronicWaste : " + err.message);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Ajouter un Déchet Électronique
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Catégorie */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Catégorie
            </label>
            <input
              name="categorie"
              value={formData.categorie}
              onChange={handleChange}
              type="text"
              placeholder="Ex: Smartphone"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
             
            />
          </div>

          {/* Type électronique */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Type d'électronique
            </label>
            <input
              name="typeElectronique"
              value={formData.typeElectronique}
              onChange={handleChange}
              type="text"
              placeholder="Ex: Téléphone portable"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
             
            />
          </div>

          {/* Durée de vie */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Durée de Vie (années)
            </label>
            <input
              name="dureeVie"
              value={formData.dureeVie}
              onChange={handleChange}
              type="number"
              min="0"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
         
            />
          </div>

          {/* Toxique */}
          <div className="flex items-center gap-4">
            <input
              name="toxic"
              type="checkbox"
              checked={formData.toxic}
              onChange={handleChange}
              className="h-5 w-5 text-red-500"
            />
            <label className="text-sm font-medium text-gray-700">
              Toxique
            </label>
          </div>

          {/* Recyclable */}
         

          <button
            type="submit"
            className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-4 rounded-xl font-semibold text-lg transition"
          >
            Enregistrer le Déchet Électronique
          </button>
        </form>
      </div>
    </div>
  );
}
