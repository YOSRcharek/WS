import React from "react";
import { Link } from "react-router-dom";

export default function EquipmentPage() {
  const equipmentTypes = [
    {
      id: "broyeurs",
      name: "Broyeurs",
      icon: "🔨",
      description: "Équipements pour broyer et réduire la taille des déchets",
      color: "from-blue-100 to-blue-200",
      link: "/equipment/broyeurs"
    },
    {
      id: "camions-benne",
      name: "Camions Benne",
      icon: "🚛",
      description: "Véhicules de transport des déchets",
      color: "from-green-100 to-green-200",
      link: "/equipment/camions-benne"
    },
    {
      id: "compacteurs",
      name: "Compacteurs",
      icon: "⚙️",
      description: "Machines pour compacter les déchets",
      color: "from-purple-100 to-purple-200",
      link: "/equipment/compacteurs"
    },
    {
      id: "conteneurs",
      name: "Conteneurs",
      icon: "📦",
      description: "Conteneurs pour le stockage des déchets",
      color: "from-yellow-100 to-yellow-200",
      link: "/equipment/conteneurs"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-12">
        <h2 className="text-4xl font-bold text-gray-800">
          Équipements
        </h2>
        <button 
          onClick={() => window.open('/ai-chat.html', '_blank')}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
        >
          🤖 Chat AI
        </button>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {equipmentTypes.map((equipment) => (
          <Link
            key={equipment.id}
            to={equipment.link}
            className={`block p-6 rounded-xl shadow-lg bg-gradient-to-r ${equipment.color} hover:shadow-xl transition-shadow`}
          >
            <div className="flex items-center">
              <span className="text-4xl mr-4">{equipment.icon}</span>
              <div>
                <h3 className="text-2xl font-bold text-gray-800">{equipment.name}</h3>
                <p className="text-gray-600 mt-1">{equipment.description}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}