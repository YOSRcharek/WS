import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export default function AddEventPage() {
  const navigate = useNavigate();
  const location = useLocation(); // Pour accéder aux props de la navigation

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

  // Récupérer la campagne si elle est passée via navigate
 const campaign = location.state?.campaign; // Accède à l'objet complet de la campagne
console.log(campaign); // Vérifiez ici si l'objet `campaign` est bien passé
const campaignId = campaign?.id; // Accède à l'id de la campagne
console.log(campaignId); // Vérifiez si l'ID est bien récupéré

  // 🟢 Gestion du changement de valeur des champs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // 🟢 Soumission du formulaire
  const handleSubmit = async (e) => {
    e.preventDefault();

    const eventData = {
      nomevent: formData.title,
      typeEvenement: formData.type,
      descriptionevent: formData.description,
      dateDebut: formData.date,
      dateFin: formData.date, // ou gérer une date de fin séparée
      lieu: formData.location,
      nombreParticipants: parseInt(formData.capacity) || 0,
      organizer: formData.organizer,
      contact: formData.contact,
      publicCible: "",
      zoneCible: "",
      objectifs: formData.objectives,
      // Ajouter la campaignId si une campagne est présente
       campagneID: campaign?.id, // Accède à l'id de la campagne
    };

    // Affichage dans la console pour vérifier que les données sont correctes
    console.log(eventData);

    try {
      const res = await fetch("http://127.0.0.1:5000/evenements", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(eventData),
      });

      const data = await res.json();

      if (res.ok) {
        alert("✅ " + data.message);

        // 🟢 Réinitialiser le formulaire
        setFormData({
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

        // 🟢 Redirection vers la liste des événements
        navigate("/events");
      } else {
        alert("⚠️ Erreur lors de la création de l'événement : " + data.message);
      }
    } catch (err) {
      console.error(err);
      alert("❌ Erreur serveur, impossible de créer l'événement.");
    }
  };

  // 🟢 Rendu du formulaire
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-8 text-center">
          Créer un Événement
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* --- Informations principales --- */}
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
                <option value="formation">Formation</option>
                <option value="collecte">Collecte Citoyenne</option>
                <option value="general">General</option>
              </select>
            </div>
          </div>

          {/* --- Description --- */}
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

          {/* --- Date & Heure --- */}
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Date
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

          {/* --- Lieu & Capacité --- */}
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
                placeholder="Adresse ou lieu"
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

          {/* --- Organisateur & Contact --- */}
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

          {/* --- Objectifs --- */}
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

          {/* --- Bouton --- */}
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
