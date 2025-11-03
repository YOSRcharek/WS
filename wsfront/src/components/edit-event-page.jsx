import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getEvenement, updateEvenement } from "../services/eventService";

export default function EditEventPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  const [formData, setFormData] = useState({
    nomevent: "",
    typeEvenement: "",
    descriptionevent: "",
    dateDebut: "",
    dateFin: "",
    lieu: "",
    nombreParticipants: 0,
  });

  // Charger les données existantes
  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getEvenement(id);
        setFormData({
          nomevent: data.nomevent || "",
          typeEvenement: data.typeEvenement || "",
          descriptionevent: data.descriptionevent || "",
          dateDebut: data.dateDebut || "",
          dateFin: data.dateFin || "",
          lieu: data.lieu || "",
          nombreParticipants: data.nombreParticipants || 0,
        });
      } catch (error) {
        console.error("Erreur lors du chargement :", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await updateEvenement(id, formData);
      alert(res.message);
      navigate("/events");
    } catch (err) {
      console.error(err);
      alert("Erreur lors de la mise à jour.");
    }
  };

  if (loading) return <div className="text-center py-10">Chargement...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          ✏️ Modifier un Événement
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nom de l'Événement
              </label>
              <input
                name="nomevent"
                value={formData.nomevent}
                onChange={handleChange}
                type="text"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Type
              </label>
              <select
                name="typeEvenement"
                value={formData.typeEvenement}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              >
                <option value="">Sélectionner un type</option>
                <option value="Collecte">Collecte</option>
                <option value="Formation">Formation</option>
                <option value="Sensibilisation">Sensibilisation</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Description
            </label>
            <textarea
              name="descriptionevent"
              value={formData.descriptionevent}
              onChange={handleChange}
              rows="3"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
            />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date Début
              </label>
              <input
                name="dateDebut"
                value={formData.dateDebut}
                onChange={handleChange}
                type="date"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date Fin
              </label>
              <input
                name="dateFin"
                value={formData.dateFin}
                onChange={handleChange}
                type="date"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Lieu
            </label>
            <input
              name="lieu"
              value={formData.lieu}
              onChange={handleChange}
              type="text"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Nombre de participants
            </label>
            <input
              name="nombreParticipants"
              value={formData.nombreParticipants}
              onChange={handleChange}
              type="number"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-semibold text-lg transition"
          >
            💾 Sauvegarder les modifications
          </button>
        </form>
      </div>
    </div>
  );
}
