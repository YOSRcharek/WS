import React from 'react';
import { Link } from 'react-router-dom';

export default function TransportListPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">Services de Transport</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Camions de Déchets */}
        <Link to="/transport/camions" className="bg-white rounded-3xl shadow-xl p-8 hover:shadow-2xl transition-shadow">
          <div className="flex items-center mb-6">
            <span className="text-4xl mr-4">🚛</span>
            <h3 className="text-2xl font-bold text-gray-800">Camions de Déchets</h3>
          </div>

          <div className="mt-6 text-emerald-600 font-semibold flex items-center">
            Voir les détails
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </Link>

        {/* Transport de Déchets Dangereux */}
        <Link to="/transport/dangereux" className="bg-white rounded-3xl shadow-xl p-8 hover:shadow-2xl transition-shadow">
          <div className="flex items-center mb-6">
            <span className="text-4xl mr-4">⚠️</span>
            <h3 className="text-2xl font-bold text-gray-800">Transport de Déchets Dangereux</h3>
          </div>

          <div className="mt-6 text-emerald-600 font-semibold flex items-center">
            Voir les détails
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </Link>
      </div>
    </div>
  );
}