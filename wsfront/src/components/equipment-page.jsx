import React from "react";

const transportFleet = [
  {
    name: "Camion Compacteur #001",
    capacity: "15 tonnes",
    status: "Actif",
    zone: "Casablanca Nord",
    dailyCollections: 12,
    statusColor: "green",
  },
  {
    name: "Camion Benne #002",
    capacity: "12 tonnes",
    status: "Actif",
    zone: "Rabat Centre",
    dailyCollections: 10,
    statusColor: "green",
  },
  {
    name: "Camion Recyclage #003",
    capacity: "10 tonnes",
    status: "Maintenance",
    zone: "Marrakech Sud",
    returnIn: "2 jours",
    statusColor: "amber",
  },
];

const sortingEquipment = [
  {
    name: "Tapis de Tri Automatique",
    capacity: "50 tonnes/jour",
    efficiency: "95%",
    location: "Centre EcoVert",
  },
  {
    name: "Compacteur Industriel",
    capacity: "30 tonnes/jour",
    efficiency: "5:1",
    location: "Centre RecycloPlus",
  },
  {
    name: "Broyeur Multi-matériaux",
    capacity: "40 tonnes/jour",
    types: "Plastique, Bois",
    location: "Centre GreenTech",
  },
];

const fleetStats = [
  { label: "Véhicules Actifs", value: 18 },
  { label: "Distance Totale", value: "2,450 km" },
  { label: "Collectes/Mois", value: 1240 },
  { label: "Efficacité", value: "94%" },
];

export default function EquipmentPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
        Équipements & Services de Transport
      </h2>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        {/* Flotte de Transport */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🚛</span> Flotte de Transport
          </h3>

          <div className="space-y-4">
            {transportFleet.map((truck, idx) => (
              <div
                key={idx}
                className={`p-6 ${
                  truck.status === "Maintenance" ? "bg-gray-50" : "bg-gradient-to-r from-emerald-50 to-green-50"
                } rounded-xl`}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h4 className="font-bold text-gray-800 text-lg">{truck.name}</h4>
                    <p className="text-sm text-gray-600 mt-1">Capacité: {truck.capacity}</p>
                  </div>
                  <span
                    className={`bg-${truck.statusColor}-500 text-white px-3 py-1 rounded-full text-sm font-semibold`}
                  >
                    {truck.status}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-gray-600">Zone</p>
                    <p className="font-semibold text-gray-800">{truck.zone}</p>
                  </div>
                  <div>
                    {truck.dailyCollections && (
                      <>
                        <p className="text-xs text-gray-600">Collectes/jour</p>
                        <p className="font-semibold text-emerald-600">{truck.dailyCollections}</p>
                      </>
                    )}
                    {truck.returnIn && (
                      <>
                        <p className="text-xs text-gray-600">Retour prévu</p>
                        <p className="font-semibold text-amber-600">{truck.returnIn}</p>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Équipements de Tri */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">⚙️</span> Équipements de Tri
          </h3>

          <div className="space-y-4">
            {sortingEquipment.map((eq, idx) => (
              <div key={idx} className="p-6 bg-gradient-to-r from-teal-50 to-cyan-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg mb-3">{eq.name}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Capacité</span>
                    <span className="font-semibold text-gray-800">{eq.capacity}</span>
                  </div>
                  {eq.efficiency && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Efficacité</span>
                      <span className="font-semibold text-emerald-600">{eq.efficiency}</span>
                    </div>
                  )}
                  {eq.types && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Types traités</span>
                      <span className="font-semibold text-emerald-600">{eq.types}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-gray-600">Localisation</span>
                    <span className="font-semibold text-gray-800">{eq.location}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Statistiques de la flotte */}
      <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-3xl shadow-xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-6">Statistiques de la Flotte</h3>
        <div className="grid md:grid-cols-4 gap-6">
          {fleetStats.map((stat, idx) => (
            <div key={idx} className="bg-white bg-opacity-20 rounded-xl p-6 backdrop-blur-sm">
              <p className="text-emerald-100 mb-2">{stat.label}</p>
              <p className="text-4xl font-bold">{stat.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
