import React, { useState, useEffect } from "react";
import { getCamionsDechets, getTransportsDangereux } from "../../services/transportService";

export default function TransportServiceListPage() {
  const [transportServices, setTransportServices] = useState({
    camionsDechets: [],
    transportsDangereux: []
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [camionsDechets, transportsDangereux] = await Promise.all([
          getCamionsDechets(),
          getTransportsDangereux()
        ]);

        setTransportServices({
          camionsDechets,
          transportsDangereux
        });
      } catch (error) {
        console.error("Error fetching transport services data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
        Services de Transport
      </h2>

      <div className="space-y-8">
        {/* Camions de Déchets Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🚛</span> Camions de Déchets
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {transportServices.camionsDechets.map((camion, idx) => (
              <div key={idx} className="p-4 bg-gradient-to-r from-emerald-50 to-green-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg">Service #{camion.id}</h4>
                <div className="grid grid-cols-2 gap-4 mt-3">
                  <div>
                    <p className="text-xs text-gray-600">Type de déchets transportés</p>
                    <p className="font-semibold text-gray-800">{camion.typeDechetTransporte}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Zone de couverture</p>
                    <p className="font-semibold text-gray-800">{camion.zoneCouverture}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Capacité maximale</p>
                    <p className="font-semibold text-gray-800">{camion.capaciteMax}</p>
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

        {/* Transport de Déchets Dangereux Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">⚠️</span> Transport de Déchets Dangereux
          </h3>
          <div className="grid md:grid-cols-2 gap-4">
            {transportServices.transportsDangereux.map((transport, idx) => (
              <div key={idx} className="p-4 bg-gradient-to-r from-red-50 to-rose-50 rounded-xl">
                <h4 className="font-bold text-gray-800 text-lg">Service #{transport.id}</h4>
                <div className="grid grid-cols-2 gap-4 mt-3">
                  <div>
                    <p className="text-xs text-gray-600">Type de déchets dangereux</p>
                    <p className="font-semibold text-gray-800">{transport.typeDechetDangereux}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Normes de sécurité</p>
                    <p className="font-semibold text-gray-800">{transport.normesSecurite}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Zone de couverture</p>
                    <p className="font-semibold text-gray-800">{transport.zoneCouverture}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Capacité maximale</p>
                    <p className="font-semibold text-gray-800">{transport.capaciteMax}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">État</p>
                    <p className="font-semibold text-gray-800">{transport.etat}</p>
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