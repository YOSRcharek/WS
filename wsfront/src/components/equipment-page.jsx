import React, { useState, useEffect } from "react";
import { getAllEquipments, getBroyeurs, getCamionsBenne, getCompacteurs, getConteneurs } from "../services/equipmentService";
import { getAllTransportServices, getCamionsDechets, getTransportsDangereux } from "../services/transportService";

export default function EquipmentPage() {
  const [equipment, setEquipment] = useState({
    broyeurs: [],
    camionsBenne: [],
    compacteurs: [],
    conteneurs: []
  });

  const [transportServices, setTransportServices] = useState({
    camionsDechets: [],
    transportsDangereux: []
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [broyeurs, camionsBenne, compacteurs, conteneurs, camionsDechets, transportsDangereux] = await Promise.all([
          getBroyeurs(),
          getCamionsBenne(),
          getCompacteurs(),
          getConteneurs(),
          getCamionsDechets(),
          getTransportsDangereux()
        ]);

        setEquipment({
          broyeurs,
          camionsBenne,
          compacteurs,
          conteneurs
        });

        setTransportServices({
          camionsDechets,
          transportsDangereux
        });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-12">
        <h2 className="text-4xl font-bold text-gray-800">
          Équipements & Services de Transport
        </h2>
        <button 
          onClick={() => window.open('/ai-chat.html', '_blank')}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
        >
          🤖 Chat AI
        </button>
      </div>

      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        {/* Équipements */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">⚙️</span> Équipements
          </h3>

          <div className="space-y-6">
            {/* Broyeurs */}
            <div>
              <h4 className="text-xl font-semibold text-gray-700 mb-3">Broyeurs</h4>
              <div className="space-y-3">
                {equipment.broyeurs.map((broyeur, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl">
                    <h5 className="font-bold text-gray-800">{broyeur.nom}</h5>
                    <div className="grid grid-cols-2 gap-2 mt-2">
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

            {/* Camions Benne */}
            <div>
              <h4 className="text-xl font-semibold text-gray-700 mb-3">Camions Benne</h4>
              <div className="space-y-3">
                {equipment.camionsBenne.map((camion, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl">
                    <h5 className="font-bold text-gray-800">{camion.nom}</h5>
                    <div className="grid grid-cols-2 gap-2 mt-2">
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

            {/* Compacteurs */}
            <div>
              <h4 className="text-xl font-semibold text-gray-700 mb-3">Compacteurs</h4>
              <div className="space-y-3">
                {equipment.compacteurs.map((compacteur, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
                    <h5 className="font-bold text-gray-800">{compacteur.nom}</h5>
                    <div className="grid grid-cols-2 gap-2 mt-2">
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

            {/* Conteneurs */}
            <div>
              <h4 className="text-xl font-semibold text-gray-700 mb-3">Conteneurs</h4>
              <div className="space-y-3">
                {equipment.conteneurs.map((conteneur, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl">
                    <h5 className="font-bold text-gray-800">{conteneur.nom}</h5>
                    <div className="grid grid-cols-2 gap-2 mt-2">
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

        {/* Services de Transport */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🚛</span> Services de Transport
          </h3>

          <div className="space-y-6">
            {/* Camions de Déchets */}
            <div>
              <h4 className="text-xl font-semibold text-gray-700 mb-3">Camions de Déchets</h4>
              <div className="space-y-3">
                {transportServices.camionsDechets.map((camion, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-emerald-50 to-green-50 rounded-xl">
                    <h5 className="font-bold text-gray-800">{camion.nom}</h5>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      <div>
                        <p className="text-xs text-gray-600">Type de déchets</p>
                        <p className="font-semibold text-gray-800">{camion.typeDechets}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Zone de service</p>
                        <p className="font-semibold text-gray-800">{camion.zone}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Transport de Déchets Dangereux */}
            <div>
              <h4 className="text-xl font-semibold text-gray-700 mb-3">Transport de Déchets Dangereux</h4>
              <div className="space-y-3">
                {transportServices.transportsDangereux.map((transport, idx) => (
                  <div key={idx} className="p-4 bg-gradient-to-r from-red-50 to-rose-50 rounded-xl">
                    <h5 className="font-bold text-gray-800">{transport.nom}</h5>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      <div>
                        <p className="text-xs text-gray-600">Type de déchets</p>
                        <p className="font-semibold text-gray-800">{transport.typeDechets}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Précautions</p>
                        <p className="font-semibold text-gray-800">{transport.precautions}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>


    </div>
  );
}
