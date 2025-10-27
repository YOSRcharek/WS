import { useState, useContext } from "react";
import { AppContext } from "../context/AppContext";

export default function AddEventPage() {
  const { events, setEvents, setCurrentPage } = useContext(AppContext);

  const [formData, setFormData] = useState({
    title: "",
    type: "",
    description: "",
    date: "",
    time: "",
    location: "",
    capacity: "",
    organizer: "",
    contact: "",
    objectives: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setEvents([
      ...events,
      { id: Date.now(), participants: 0, status: "planifie", ...formData },
    ]);
    alert("Événement créé avec succès !");
    setFormData({
      title: "", type: "", description: "", date: "", time: "",
      location: "", capacity: "", organizer: "", contact: "", objectives: ""
    });
    setCurrentPage("events"); // redirige vers la page events
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Créer un Événement
        </h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Titre de l'Événement
              </label>
              <input
                name="title"
                value={formData.title}
                onChange={handleChange}
                type="text"
                placeholder="Ex: Journée Mondiale du Recyclage"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Type d'Événement
              </label>
              <select
                name="type"
                value={formData.type}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              >
                <option value="">Sélectionner un type</option>
                <option value="sensibilisation">Sensibilisation</option>
                <option value="formation">Formation</option>
                <option value="collecte">Collecte Citoyenne</option>
                <option value="atelier">Atelier Pratique</option>
                <option value="conference">Conférence</option>
                <option value="nettoyage">Nettoyage Communautaire</option>
              </select>
            </div>
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
              placeholder="Décrivez votre événement..."
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
              required
            />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date de l'Événement
              </label>
              <input
                name="date"
                value={formData.date}
                onChange={handleChange}
                type="date"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Heure
              </label>
              <input
                name="time"
                value={formData.time}
                onChange={handleChange}
                type="time"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Lieu
              </label>
              <input
                name="location"
                value={formData.location}
                onChange={handleChange}
                type="text"
                placeholder="Adresse ou lieu de l'événement"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nombre de Participants Max
              </label>
              <input
                name="capacity"
                value={formData.capacity}
                onChange={handleChange}
                type="number"
                placeholder="Ex: 100"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Organisateur
              </label>
              <input
                name="organizer"
                value={formData.organizer}
                onChange={handleChange}
                type="text"
                placeholder="Nom de l'organisateur"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
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
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Objectifs de l'Événement
            </label>
            <textarea
              name="objectives"
              value={formData.objectives}
              onChange={handleChange}
              rows="3"
              placeholder="Quels sont les objectifs à atteindre ?"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg transition"
          >
            Créer l'Événement
          </button>
        </form>
      </div>
    </div>
  );
}
