import React from "react";
import { useNavigate } from "react-router-dom";

const wastes = [
  { type: "Plastique", weight: "12 kg", location: "Casablanca", date: "20/10/2025", status: "Trié" },
  { type: "Papier", weight: "8 kg", location: "Rabat", date: "21/10/2025", status: "En attente" },
  { type: "Verre", weight: "15 kg", location: "Marrakech", date: "22/10/2025", status: "Trié" },
];

export default function WasteListPage() {
  const navigate = useNavigate();

  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800">Liste des Déchets</h2>
          <button
            onClick={() => navigate("/add-waste")}
            className="btn-primary text-white px-6 py-3 rounded-xl font-semibold"
          >
            + Ajouter
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="gradient-green text-white">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold">Type</th>
                  <th className="px-6 py-4 text-left font-semibold">Poids</th>
                  <th className="px-6 py-4 text-left font-semibold">Localisation</th>
                  <th className="px-6 py-4 text-left font-semibold">Date</th>
                  <th className="px-6 py-4 text-left font-semibold">Statut</th>
                  <th className="px-6 py-4 text-left font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {wastes.map((waste, idx) => (
                  <tr key={idx}>
                    <td className="px-6 py-4">{waste.type}</td>
                    <td className="px-6 py-4">{waste.weight}</td>
                    <td className="px-6 py-4">{waste.location}</td>
                    <td className="px-6 py-4">{waste.date}</td>
                    <td className="px-6 py-4">{waste.status}</td>
                    <td className="px-6 py-4">
                      <button className="text-blue-500 hover:underline mr-2">Éditer</button>
                      <button className="text-red-500 hover:underline">Supprimer</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
