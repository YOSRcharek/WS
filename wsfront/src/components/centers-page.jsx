import React from "react";

const recyclingCenters = [
  {
    name: "Centre EcoVert Nord",
    location: "Zone Industrielle Nord, Casablanca",
    hours: "Lun-Sam: 8h-18h",
    capacity: "500 tonnes/mois",
  },
  {
    name: "Centre RecycloPlus",
    location: "Avenue Hassan II, Rabat",
    hours: "Lun-Ven: 9h-17h",
    capacity: "350 tonnes/mois",
  },
  {
    name: "Centre GreenTech Sud",
    location: "Quartier Industriel, Marrakech",
    hours: "Lun-Sam: 7h-19h",
    capacity: "420 tonnes/mois",
  },
];

const collectionPoints = [
  {
    name: "Point Quartier Maarif",
    location: "Boulevard Zerktouni, Casablanca",
    types: "Plastique, Verre, Papier",
  },
  {
    name: "Point Centre Ville",
    location: "Place Mohammed V, Rabat",
    types: "Tous types de déchets",
  },
  {
    name: "Point Résidentiel Agdal",
    location: "Avenue des FAR, Rabat",
    types: "Organique, Plastique, Métal",
  },
  {
    name: "Point Médina",
    location: "Bab Ftouh, Marrakech",
    types: "Papier, Carton, Verre",
  },
];

export default function CentersPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
        Centres de Recyclage & Points de Collecte
      </h2>

      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🏭</span> Centres de Recyclage
          </h3>
          <div className="space-y-4">
            {recyclingCenters.map((center, idx) => (
              <div
                key={idx}
                className="border-l-4 border-emerald-500 pl-4 py-3 bg-emerald-50 rounded-r-xl"
              >
                <h4 className="font-bold text-gray-800">{center.name}</h4>
                <p className="text-gray-600 text-sm mt-1">📍 {center.location}</p>
                <p className="text-gray-600 text-sm">⏰ {center.hours}</p>
                <p className="text-emerald-600 font-semibold text-sm mt-2">
                  Capacité: {center.capacity}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">📍</span> Points de Collecte
          </h3>
          <div className="space-y-4">
            {collectionPoints.map((point, idx) => (
              <div
                key={idx}
                className="border-l-4 border-teal-500 pl-4 py-3 bg-teal-50 rounded-r-xl"
              >
                <h4 className="font-bold text-gray-800">{point.name}</h4>
                <p className="text-gray-600 text-sm mt-1">📍 {point.location}</p>
                <p className="text-teal-600 font-semibold text-sm mt-2">
                  Types: {point.types}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-br from-emerald-500 to-teal-500 rounded-3xl shadow-xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-4">Carte Interactive</h3>
        <div className="bg-white rounded-xl h-96 flex items-center justify-center text-gray-400">
          <div className="text-center">
            <div className="text-6xl mb-4">🗺️</div>
            <p className="text-gray-600 font-semibold">
              Carte des centres et points de collecte
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Visualisation géographique interactive
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
