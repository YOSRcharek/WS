import React from "react";

const citizens = [
  { name: "Ahmed Benali", city: "Casablanca - Maarif", recycled: 245 },
  { name: "Fatima Zahra", city: "Rabat - Agdal", recycled: 189 },
  { name: "Youssef Alami", city: "Marrakech - Guéliz", recycled: 312 },
  { name: "Samira Idrissi", city: "Tanger - Centre", recycled: 156 },
];

const municipalities = [
  { name: "Municipalité de Casablanca", points: 45, citizens: 4250 },
  { name: "Municipalité de Rabat", points: 32, citizens: 3180 },
  { name: "Municipalité de Marrakech", points: 28, citizens: 2890 },
];

export default function UsersPage() {
  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">Citoyens & Municipalités</h2>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Citizens Section */}
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="text-4xl mr-3">👥</span>
              Citoyens Actifs
            </h3>

            <div className="mb-6 p-4 bg-emerald-50 rounded-xl">
              <div className="flex justify-between items-center">
                <span className="text-gray-700 font-semibold">Total Citoyens</span>
                <span className="text-3xl font-bold text-emerald-600">12,547</span>
              </div>
            </div>

            <div className="space-y-4">
              {citizens.map((citizen, idx) => (
                <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-emerald-50 transition">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-emerald-200 rounded-full flex items-center justify-center text-2xl">
                      👤
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-800">{citizen.name}</h4>
                      <p className="text-sm text-gray-600">{citizen.city}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-emerald-600">{citizen.recycled} kg</p>
                    <p className="text-xs text-gray-500">Recyclés</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Municipalities Section */}
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="text-4xl mr-3">🏛️</span>
              Municipalités Partenaires
            </h3>

            <div className="mb-6 p-4 bg-teal-50 rounded-xl">
              <div className="flex justify-between items-center">
                <span className="text-gray-700 font-semibold">Municipalités</span>
                <span className="text-3xl font-bold text-teal-600">24</span>
              </div>
            </div>

            <div className="space-y-4">
              {municipalities.map((muni, idx) => (
                <div key={idx} className="p-6 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl border-l-4 border-emerald-500">
                  <h4 className="font-bold text-gray-800 text-lg mb-2">{muni.name}</h4>
                  <div className="grid grid-cols-2 gap-4 mt-4">
                    <div>
                      <p className="text-sm text-gray-600">Points de collecte</p>
                      <p className="text-xl font-bold text-emerald-600">{muni.points}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Citoyens actifs</p>
                      <p className="text-xl font-bold text-emerald-600">{muni.citizens}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
