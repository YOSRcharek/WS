import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function CitizenRequests() {
  const navigate = useNavigate();
  const [requests, setRequests] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    citizenName: "",
    municipalityName: "",
    requestType: "",
    description: "",
    priority: "Normal"
  });
  const [citizens, setCitizens] = useState([]);
  const [municipalities, setMunicipalities] = useState([]);

  useEffect(() => {
    fetchRequests();
    fetchCitizens();
    fetchMunicipalities();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/citizen-requests");
      const data = await response.json();
      setRequests(data);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const fetchCitizens = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/citoyens");
      const data = await response.json();
      setCitizens(data);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const fetchMunicipalities = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/municipalites");
      const data = await response.json();
      setMunicipalities(data);
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/citizen-requests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        alert("Demande soumise avec succès!");
        setFormData({ citizenName: "", municipalityName: "", requestType: "", description: "", priority: "Normal" });
        setShowForm(false);
        fetchRequests();
      }
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const updateStatus = async (requestId, newStatus) => {
    try {
      await fetch(`http://127.0.0.1:5000/citizen-requests/${requestId}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
      });
      fetchRequests();
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case "Urgent": return "bg-red-100 text-red-700";
      case "Élevée": return "bg-orange-100 text-orange-700";
      default: return "bg-blue-100 text-blue-700";
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "Résolu": return "bg-green-100 text-green-700";
      case "En cours": return "bg-yellow-100 text-yellow-700";
      default: return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-8">
        <button
          onClick={() => navigate("/users")}
          className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg font-semibold transition"
        >
          ← Retour
        </button>
        <h2 className="text-4xl font-bold text-gray-800 flex-1 text-center">Demandes Citoyennes</h2>
        <button
          onClick={() => setShowForm(true)}
          className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-xl font-semibold"
        >
          + Nouvelle Demande
        </button>
      </div>

      {/* Requests List */}
      <div className="space-y-4">
        {requests.map((req, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-800">{req.citizenName}</h3>
                <p className="text-gray-600">{req.requestType}</p>
                <p className="text-sm text-gray-500">Municipalité: {req.municipalityName}</p>
              </div>
              <div className="flex space-x-2">
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getPriorityColor(req.priority)}`}>
                  {req.priority}
                </span>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(req.status)}`}>
                  {req.status}
                </span>
              </div>
            </div>
            <p className="text-gray-700 mb-4">{req.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-500">{new Date(req.dateCreated).toLocaleDateString()}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Nouvelle Demande</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <select
                value={formData.citizenName}
                onChange={(e) => setFormData({...formData, citizenName: e.target.value})}
                className="w-full px-4 py-3 border rounded-xl"
                required
              >
                <option value="">Sélectionner un citoyen</option>
                {citizens.map((citizen, idx) => (
                  <option key={idx} value={citizen.neaemcitoyen || 'Citoyen'}>
                    {citizen.neaemcitoyen || 'Nom non spécifié'}
                  </option>
                ))}
              </select>
              <select
                value={formData.municipalityName}
                onChange={(e) => setFormData({...formData, municipalityName: e.target.value})}
                className="w-full px-4 py-3 border rounded-xl"
                required
              >
                <option value="">Sélectionner une municipalité</option>
                {municipalities.map((muni, idx) => (
                  <option key={idx} value={muni.nom || 'Municipalité'}>
                    {muni.nom || 'Nom non spécifié'}
                  </option>
                ))}
              </select>
              <select
                value={formData.requestType}
                onChange={(e) => setFormData({...formData, requestType: e.target.value})}
                className="w-full px-4 py-3 border rounded-xl"
                required
              >
                <option value="">Type de demande</option>
                <option value="Collecte non effectuée">Collecte non effectuée</option>
                <option value="Poubelle endommagée">Poubelle endommagée</option>
                <option value="Dépôt sauvage">Dépôt sauvage</option>
                <option value="Information">Demande d'information</option>
                <option value="Autre">Autre</option>
              </select>
              <textarea
                placeholder="Description détaillée"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                className="w-full px-4 py-3 border rounded-xl"
                rows="4"
                required
              />
              <select
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
                className="w-full px-4 py-3 border rounded-xl"
              >
                <option value="Normal">Normal</option>
                <option value="Élevée">Élevée</option>
                <option value="Urgent">Urgent</option>
              </select>
              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-xl"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-emerald-500 text-white py-3 rounded-xl"
                >
                  Soumettre
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}