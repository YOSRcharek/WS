import React from "react";

const statsCards = [
  { icon: "📅", label: "Événements Actifs", value: 24, change: "+12%", color: "emerald" },
  { icon: "👥", label: "Participants Total", value: "8,547", change: "+28%", color: "blue" },
  { icon: "📢", label: "Campagnes en Cours", value: 8, change: "+15%", color: "purple" },
  { icon: "⭐", label: "Taux de Satisfaction", value: "96%", change: "+5%", color: "amber" },
];

const monthlyParticipation = [
  { month: "Janvier", value: 1240, percent: 62 },
  { month: "Février", value: 1580, percent: 79 },
  { month: "Mars", value: 2000, percent: 100 },
];

const eventTypes = [
  { icon: "🌍", label: "Sensibilisation", value: 12, bg: "emerald-50", text: "emerald-600" },
  { icon: "🎓", label: "Formation", value: 8, bg: "blue-50", text: "blue-600" },
  { icon: "🤝", label: "Collecte Citoyenne", value: 4, bg: "purple-50", text: "purple-600" },
];

const environmentalImpact = [
  { icon: "♻️", label: "Déchets Collectés", value: "12.5 tonnes" },
  { icon: "🌱", label: "CO₂ Évité", value: "8.2 tonnes" },
  { icon: "🌳", label: "Arbres Sauvés", value: 340 },
];

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
        Dashboard Événements & Campagnes
      </h2>

      {/* Statistiques */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {statsCards.map((card, idx) => (
          <div key={idx} className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-4xl">{card.icon}</div>
              <div className={`bg-${card.color}-100 text-${card.color}-600 px-3 py-1 rounded-full text-sm font-semibold`}>
                {card.change}
              </div>
            </div>
            <h3 className="text-gray-600 text-sm font-semibold mb-2">{card.label}</h3>
            <p className="text-3xl font-bold text-gray-800">{card.value}</p>
          </div>
        ))}
      </div>

      {/* Participation et types d'événements */}
      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">Participation par Mois</h3>
          <div className="space-y-4">
            {monthlyParticipation.map((item, idx) => (
              <div key={idx}>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600 font-medium">{item.month}</span>
                  <span className="font-bold text-emerald-600">{item.value}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-gradient-to-r from-emerald-400 to-teal-500 h-3 rounded-full"
                    style={{ width: `${item.percent}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">Types d'Événements</h3>
          <div className="space-y-4">
            {eventTypes.map((type, idx) => (
              <div key={idx} className={`flex items-center justify-between p-4 bg-${type.bg} rounded-xl`}>
                <div className="flex items-center space-x-3">
                  <div className="text-3xl">{type.icon}</div>
                  <span className="font-semibold text-gray-800">{type.label}</span>
                </div>
                <span className={`text-2xl font-bold text-${type.text}`}>{type.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Impact environnemental */}
      <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-3xl shadow-xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-6">Impact Environnemental</h3>
        <div className="grid md:grid-cols-3 gap-6">
          {environmentalImpact.map((impact, idx) => (
            <div key={idx} className="bg-white bg-opacity-20 rounded-xl p-6 backdrop-blur-sm">
              <div className="text-4xl mb-3">{impact.icon}</div>
              <p className="text-emerald-100 mb-2">{impact.label}</p>
              <p className="text-3xl font-bold">{impact.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
