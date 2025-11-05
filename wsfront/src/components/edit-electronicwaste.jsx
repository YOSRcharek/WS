// src/pages/EditElectronicWastePage.jsx
import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getElectronicWaste, updateElectronicWaste } from "../services/typedechetService";

export default function EditElectronicWastePage() {
  const { id } = useParams(); // id du electronicWaste
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    typeAppareil: "",
    categorie: "",
    dureeVie: 0,
    toxic: false,
    recyclable: false
  });

  const [loading, setLoading] = useState(true);

  // 🔹 Charger les données existantes
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getElectronicWaste(id);
        setFormData({
          typeAppareil: data.typeAppareil || "",
          categorie: data.categorie || "",
          dureeVie: data.dureeVie || 0,
          toxic: data.toxic === "true",
          recyclable: data.recyclable === "true"
        });
      } catch (err) {
        console.error("Erreur lors du chargement du ElectronicWaste :", err);
        alert("Erreur lors du chargement du ElectronicWaste");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateElectronicWaste(id, formData);
      alert("ElectronicWaste mis à jour avec succès !");
      navigate("/waste-electronic");
    } catch (err) {
      console.error("Erreur lors de la mise à jour :", err);
      alert("Erreur lors de la mise à jour du ElectronicWaste");
    }
  };

  if (loading) {
    return <div className="text-center py-10 text-gray-600 text-lg">Chargement du ElectronicWaste...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">Modifier ElectronicWaste</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Type Electronique</label>
            <input
              name="typeAppareil"
              value={formData.typeAppareil}
              onChange={handleChange}
              type="text"
              placeholder="Ex: Smartphone"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Catégorie</label>
            <input
              name="categorie"
              value={formData.categorie}
              onChange={handleChange}
              type="text"
              placeholder="Ex: Télécommunication"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Durée de Vie (en années)</label>
            <input
              name="dureeVie"
              value={formData.dureeVie}
              onChange={handleChange}
              type="number"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none transition"
            />
          </div>

          <div className="flex items-center gap-4">
            <input
              name="toxic"
              type="checkbox"
              checked={formData.toxic}
              onChange={handleChange}
              className="h-5 w-5 text-red-500"
            />
            <label className="text-sm font-medium text-gray-700">Toxique</label>
          </div>

         

          <button
            type="submit"
            className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-4 rounded-xl font-semibold text-lg transition"
          >
            Mettre à jour
          </button>
        </form>
      </div>
    </div>
  );
}
