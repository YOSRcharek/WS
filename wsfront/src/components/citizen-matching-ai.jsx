import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CitizenMatchingAI() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleMatch = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/match-citizens", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error:", error);
      setResults({ status: "error", message: "Connection failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-2xl p-8">
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => navigate("/users")}
            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg font-semibold transition"
          >
            ← Retour
          </button>
          <h2 className="text-4xl font-bold text-gray-800 text-center flex-1">
            🤖 Smart Citizen-Municipality Matching AI
          </h2>
          <div className="w-20"></div>
        </div>
        
        <div className="text-center mb-8">
          <p className="text-gray-600 mb-6">
            L'IA analyse automatiquement les adresses des citoyens pour les assigner aux bonnes municipalités
          </p>
          
          <button
            onClick={handleMatch}
            disabled={loading}
            className={`px-8 py-4 rounded-xl font-semibold text-lg transition ${
              loading 
                ? "bg-gray-400 text-gray-700" 
                : "bg-emerald-500 hover:bg-emerald-600 text-white"
            }`}
          >
            {loading ? "🔄 Analyse en cours..." : "🚀 Lancer l'analyse IA"}
          </button>
        </div>

        {results && (
          <div className="mt-8">
            {results.status === "success" ? (
              <div className="bg-green-50 border border-green-200 rounded-xl p-6">
                <h3 className="text-xl font-bold text-green-800 mb-4">
                  ✅ Analyse terminée avec succès !
                </h3>
                <p className="text-green-700 mb-4">
                  <strong>{results.total_matched}</strong> citoyens ont été assignés automatiquement
                </p>
                
                {results.matches.length > 0 && (
                  <div className="space-y-3">
                    <h4 className="font-semibold text-green-800">Correspondances trouvées :</h4>
                    {results.matches.map((match, idx) => (
                      <div key={idx} className="bg-white p-4 rounded-lg border border-green-200">
                        <div className="flex justify-between items-center">
                          <span className="font-medium">{match.citizen}</span>
                          <span className="text-green-600">→</span>
                          <span className="font-medium text-green-700">{match.municipality}</span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{match.reason}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-red-50 border border-red-200 rounded-xl p-6">
                <h3 className="text-xl font-bold text-red-800 mb-2">❌ Erreur</h3>
                <p className="text-red-700">{results.message}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}