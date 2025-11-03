import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const emojis = ["🌍", "🌱", "🏫", "💧", "📱", "🎯", "♻️"];

export default function EventsPage() {
  const navigate = useNavigate();
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const [activeCampaigns, setActiveCampaigns] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/evenements");
        const data = await res.json();
        if (!data.results || !Array.isArray(data.results)) return;

        setUpcomingEvents(
          data.results.map((event) => ({
            ...event,
            emoji: emojis[Math.floor(Math.random() * emojis.length)],
            color: "emerald",
          }))
        );
      } catch (error) {
        console.error(error);
      }
    };

    const fetchCampaigns = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/campagnes");
        const data = await res.json();

        setActiveCampaigns(
          data.map((camp) => ({
            ...camp,
            emoji: emojis[Math.floor(Math.random() * emojis.length)],
            color: "blue",
            status: "En cours",
            collected: `${Math.floor(Math.random() * 10000)} kg collectés`,
            progress: Math.floor(Math.random() * 100),
            button: "Participer",
          }))
        );
      } catch (error) {
        console.error(error);
      }
    };

    fetchEvents();
    fetchCampaigns();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex flex-col md:flex-row justify-between items-center mb-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-4 md:mb-0">
          Événements & Campagnes de Sensibilisation
        </h2>
        <div className="flex gap-4">
          <button
            onClick={() => navigate("/add-event")}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + Créer Événement
          </button>
          <button
            onClick={() => navigate("/add-campaign")}
            className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            + Lancer Campagne
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Événements à venir */}
        <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-4xl mr-3">📅</span>
                Événements à Venir
              </div>

              <button
                onClick={() => navigate("/event-list")}
                className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium text-sm transition shadow-sm"
              >
                ⚙️ Gérer Événements
              </button>
            </h3>

          <div className="space-y-6">
            {upcomingEvents.map((event, idx) => (
              <div key={idx} className="card-hover bg-white rounded-2xl shadow-lg overflow-hidden"   onClick={() => navigate(`/event/${event.evenementID}`)}>
                <div className={`h-48 image-placeholder flex items-center justify-center text-6xl bg-gradient-to-br from-${event.color}-400 to-${event.color}-500`}>
                  {event.emoji}
                </div>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <span className={`bg-${event.color}-100 text-${event.color}-700 px-3 py-1 rounded-full text-sm font-semibold`}>
                      {event.dateDebut} - {event.dateFin}
                    </span>
                    <span className="text-gray-500 text-sm">📍 {event.lieu}</span>
                  </div>
                  <h4 className="text-xl font-bold text-gray-800 mb-2">{event.nomevent}</h4>
                  <p className="text-gray-600 mb-4">{event.descriptionevent}</p>
                  <div className="flex items-center justify-between">
                    <span className={`text-${event.color}-600 font-semibold`}>
                      {event.nombreParticipants} participants
                    </span>
                    <button className={`bg-${event.color}-500 text-white px-4 py-2 rounded-lg hover:bg-${event.color}-600 transition`}>
                      S'inscrire
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Campagnes actives */}
           <div>
           <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-4xl mr-3">📢</span>
            Campagnes Actives
            </div>

            <button
              onClick={() => navigate("/campaign-list")}
              className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium text-sm transition shadow-sm"
            >
              ⚙️ Gérer Campagnes
            </button>
          </h3>
          <div className="space-y-6">
            {activeCampaigns.map((campaign, idx) => (
              <div key={idx} className="card-hover bg-white rounded-2xl shadow-lg overflow-hidden" onClick={() => navigate(`/campaign/${campaign.campaignID}`)}>
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
                      <div className={`bg-gradient-to-r from-${campaign.color}-500 to-${campaign.color}-600 h-3 rounded-full`} style={{ width: `${campaign.progress}%` }}></div>
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
              <p className="mb-4">
                Réduisez vos déchets de 30% ce mois-ci et gagnez des récompenses!
              </p>
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
