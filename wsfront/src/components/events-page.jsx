
import React, { useContext } from "react";
import { AppContext } from "../context/AppContext";
const upcomingEvents = [
  {
    emoji: "🌍",
    date: "15 Mars 2024",
    location: "Casablanca",
    title: "Journée Mondiale du Recyclage",
    description: "Grande collecte citoyenne et ateliers de sensibilisation au tri sélectif pour toute la famille.",
    participants: "250 participants attendus",
    button: "S'inscrire",
    color: "emerald",
  },
  {
    emoji: "🌱",
    date: "22 Mars 2024",
    location: "Rabat",
    title: "Atelier Compostage Urbain",
    description: "Apprenez à transformer vos déchets organiques en compost de qualité pour vos plantes.",
    participants: "50 places disponibles",
    button: "S'inscrire",
    color: "green",
  },
  {
    emoji: "🏫",
    date: "5 Avril 2024",
    location: "Marrakech",
    title: "Programme Écoles Vertes",
    description: "Sensibilisation des élèves aux enjeux environnementaux et mise en place du tri dans les écoles.",
    participants: "15 écoles participantes",
    button: "En savoir plus",
    color: "teal",
  },
];

const activeCampaigns = [
  {
    emoji: "💧",
    status: "En cours",
    title: "Zéro Plastique 2024",
    description: "Campagne nationale pour réduire l'utilisation du plastique à usage unique et promouvoir les alternatives durables.",
    objective: "10,000 kg",
    collected: "7,450 kg collectés",
    progress: 74.5,
    button: "Participer",
    color: "blue",
  },
  {
    emoji: "📱",
    status: "En cours",
    title: "Recyclage Électronique",
    description: "Collecte spéciale d'appareils électroniques usagés pour un recyclage responsable et sécurisé.",
    objective: "500 appareils",
    collected: "342 collectés",
    progress: 68.4,
    button: "Participer",
    color: "purple",
  },
];

export default function EventsPage() {
    const { setCurrentPage } = useContext(AppContext);
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex flex-col md:flex-row justify-between items-center mb-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-4 md:mb-0">
          Événements & Campagnes de Sensibilisation
        </h2>
        <div className="flex gap-4">
          <button
            onClick={() => setCurrentPage("add-event")}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + Créer Événement
          </button>
          <button
            onClick={() => setCurrentPage("add-campaign")}
            className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + Lancer Campagne
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Événements à venir */}
        <div>
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">📅</span> Événements à Venir
          </h3>
          <div className="space-y-6">
            {upcomingEvents.map((event, idx) => (
              <div key={idx} className="card-hover bg-white rounded-2xl shadow-lg overflow-hidden">
                <div className={`h-48 image-placeholder flex items-center justify-center text-6xl bg-gradient-to-br from-${event.color}-400 to-${event.color}-500`}>
                  {event.emoji}
                </div>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className={`bg-${event.color}-100 text-${event.color}-700 px-3 py-1 rounded-full text-sm font-semibold`}>
                      {event.date}
                    </span>
                    <span className="text-gray-500 text-sm">📍 {event.location}</span>
                  </div>
                  <h4 className="text-xl font-bold text-gray-800 mb-2">{event.title}</h4>
                  <p className="text-gray-600 mb-4">{event.description}</p>
                  <div className="flex items-center justify-between">
                    <span className={`text-${event.color}-600 font-semibold`}>{event.participants}</span>
                    <button className={`bg-${event.color}-500 text-white px-4 py-2 rounded-lg hover:bg-${event.color}-600 transition`}>
                      {event.button}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Campagnes actives */}
        <div>
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">📢</span> Campagnes Actives
          </h3>
          <div className="space-y-6">
            {activeCampaigns.map((campaign, idx) => (
              <div key={idx} className="card-hover bg-white rounded-2xl shadow-lg overflow-hidden">
                <div className={`h-48 image-placeholder flex items-center justify-center text-6xl bg-gradient-to-br from-${campaign.color}-400 to-${campaign.color}-500`}>
                  {campaign.emoji}
                </div>
                <div className="p-6">
                  <div className="mb-3">
                    <span className={`bg-${campaign.color}-100 text-${campaign.color}-700 px-3 py-1 rounded-full text-sm font-semibold`}>
                      {campaign.status}
                    </span>
                  </div>
                  <h4 className="text-xl font-bold text-gray-800 mb-2">{campaign.title}</h4>
                  <p className="text-gray-600 mb-4">{campaign.description}</p>
                  <div className="bg-gray-100 rounded-lg p-4 mb-4">
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-600">Objectif: {campaign.objective}</span>
                      <span className={`font-semibold text-${campaign.color}-600`}>{campaign.collected}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className={`bg-gradient-to-r from-${campaign.color}-500 to-${campaign.color}-600 h-3 rounded-full`}
                        style={{ width: `${campaign.progress}%` }}
                      ></div>
                    </div>
                  </div>
                  <button className={`w-full bg-${campaign.color}-500 text-white py-2 rounded-lg hover:bg-${campaign.color}-600 transition`}>
                    {campaign.button}
                  </button>
                </div>
              </div>
            ))}

            {/* Défi du mois */}
            <div className="bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl shadow-lg p-6 text-white">
              <h4 className="text-xl font-bold mb-4">🎯 Défi du Mois</h4>
              <p className="mb-4">Réduisez vos déchets de 30% ce mois-ci et gagnez des récompenses!</p>
              <div className="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur-sm">
                <div className="flex justify-between items-center">
                  <span>Participants</span>
                  <span className="text-2xl font-bold">1,247</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
