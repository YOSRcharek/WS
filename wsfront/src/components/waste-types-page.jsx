import React from "react";

const wasteTypes = [
  { emoji: "🥤", name: "Plastique", description: "Bouteilles, emballages, sacs plastiques", status: "Recyclable", amount: "450 kg/mois", color: "emerald" },
  { emoji: "🍾", name: "Verre", description: "Bouteilles, bocaux, contenants en verre", status: "100% Recyclable", amount: "320 kg/mois", color: "emerald" },
  { emoji: "📄", name: "Papier/Carton", description: "Journaux, cartons, documents", status: "Recyclable", amount: "580 kg/mois", color: "emerald" },
  { emoji: "🥫", name: "Métal", description: "Canettes, conserves, ferraille", status: "Recyclable", amount: "280 kg/mois", color: "emerald" },
  { emoji: "🍎", name: "Organique", description: "Restes alimentaires, déchets verts", status: "Compostable", amount: "720 kg/mois", color: "emerald" },
  { emoji: "💻", name: "Électronique", description: "Appareils, batteries, câbles", status: "Traitement Spécial", amount: "95 kg/mois", color: "amber" },
];

export default function WasteTypesPage() {
  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
          Types de Déchets & Classification
        </h2>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {wasteTypes.map((waste, idx) => (
            <div key={idx} className="card-hover bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="h-48 image-placeholder flex items-center justify-center text-6xl">
                {waste.emoji}
              </div>
              <div className="p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-3">{waste.name}</h3>
                <p className="text-gray-600 mb-4">{waste.description}</p>
                <div className="flex items-center justify-between">
                  <span className={`text-${waste.color}-600 font-semibold`}>{waste.status}</span>
                  <span className={`bg-${waste.color}-100 text-${waste.color}-700 px-3 py-1 rounded-full text-sm`}>{waste.amount}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
