// src/pages/AISparqlPage.jsx
import { useState } from "react";

export default function AISparqlPage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);
    setError("");

    try {
      const res = await fetch("http://localhost:5000/sparql-generator", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();

      if (data.status === "success") {
        setResults(data.results);
      } else {
        setError(data.message || "Erreur inconnue");
      }
    } catch (err) {
      console.error(err);
      setError("Erreur de communication avec le serveur");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6 text-center">Générateur de requêtes SPARQL par IA</h2>

      <form onSubmit={handleSubmit} className="mb-6">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ex: 'Liste tous les déchets recyclables avec poids > 5kg'"
          className="w-full border-2 border-gray-300 rounded-xl p-4 h-28 focus:border-emerald-500 focus:outline-none resize-none"
          required
        />
        <button
          type="submit"
          className="mt-4 w-full bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-xl font-semibold transition"
          disabled={loading}
        >
          {loading ? "Chargement..." : "Exécuter la requête"}
        </button>
      </form>

      {error && <p className="text-red-600 font-medium mb-4">{error}</p>}

      {results.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full border border-gray-200 rounded-xl overflow-hidden">
            <thead className="bg-gray-800 text-white">
              <tr>
                {Object.keys(results[0]).map((key) => (
                  <th key={key} className="px-4 py-2 text-left font-semibold">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {results.map((item, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  {Object.keys(item).map((key) => (
                    <td key={key} className="px-4 py-2">{item[key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {results.length === 0 && !loading && !error && (
        <p className="text-gray-500 italic mt-4 text-center">Aucun résultat pour le moment.</p>
      )}
    </div>
  );
}
