import React, { useState, useEffect } from "react";
import { getBroyeurs, getCamionsBenne, getCompacteurs, getConteneurs } from "../../services/equipmentService";

export default function EquipmentListPage() {
  const [equipment, setEquipment] = useState({
    broyeurs: [],
    camionsBenne: [],
    compacteurs: [],
    conteneurs: []
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [broyeurs, camionsBenne, compacteurs, conteneurs] = await Promise.all([
          getBroyeurs(),
          getCamionsBenne(),
          getCompacteurs(),
          getConteneurs()
        ]);

        setEquipment({
          broyeurs,
          camionsBenne,
          compacteurs,
          conteneurs
        });
      } catch (error) {
        console.error("Error fetching equipment data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
        Équipements
      </h2>

      <div className="space-y-8">
        {/* Broyeurs Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🔨</span> Broyeurs
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {equipment.broyeurs.map((broyeur, idx) => (
              <div key={idx} className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg">{broyeur.nom}</h4>
                <div className="grid grid-cols-2 gap-4 mt-3">
                  <div>
                    <p className="text-xs text-gray-600">Capacité</p>
                    <p className="font-semibold text-gray-800">{broyeur.capacite}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Type</p>
                    <p className="font-semibold text-gray-800">{broyeur.type}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Camions Benne Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🚛</span> Camions Benne
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {equipment.camionsBenne.map((camion, idx) => (
              <div key={idx} className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg">{camion.nom}</h4>
                <div className="grid grid-cols-2 gap-4 mt-3">
                  <div>
                    <p className="text-xs text-gray-600">Capacité</p>
                    <p className="font-semibold text-gray-800">{camion.capacite}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">État</p>
                    <p className="font-semibold text-gray-800">{camion.etat}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Compacteurs Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">⚙️</span> Compacteurs
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {equipment.compacteurs.map((compacteur, idx) => (
              <div key={idx} className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg">{compacteur.nom}</h4>
                <div className="grid grid-cols-2 gap-4 mt-3">
                  <div>
                    <p className="text-xs text-gray-600">Puissance</p>
                    <p className="font-semibold text-gray-800">{compacteur.puissance}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Type</p>
                    <p className="font-semibold text-gray-800">{compacteur.type}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Conteneurs Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">📦</span> Conteneurs
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {equipment.conteneurs.map((conteneur, idx) => (
              <div key={idx} className="p-4 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg">{conteneur.nom}</h4>
                <div className="grid grid-cols-2 gap-4 mt-3">
                  <div>
                    <p className="text-xs text-gray-600">Volume</p>
                    <p className="font-semibold text-gray-800">{conteneur.volume}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Type</p>
                    <p className="font-semibold text-gray-800">{conteneur.type}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}