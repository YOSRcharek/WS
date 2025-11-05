import React, { useState, useEffect } from "react";
import AddCitizenForm from "./add-citizen-form";
import AddMunicipalityForm from "./add-municipality-form";

export default function UsersPage() {
  const [citoyens, setCitoyens] = useState([]);
  const [municipalites, setMunicipalites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCitizenForm, setShowCitizenForm] = useState(false);
  const [showMunicipalityForm, setShowMunicipalityForm] = useState(false);
  const [editingCitizen, setEditingCitizen] = useState(null);
  const [editingMunicipality, setEditingMunicipality] = useState(null);
  const [showingCitizens, setShowingCitizens] = useState(null);
  const [municipalityCitizens, setMunicipalityCitizens] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [citoyensRes, municipalitesRes] = await Promise.all([
        fetch('http://127.0.0.1:5000/citoyens'),
        fetch('http://localhost:5000/api/municipalites')
      ]);
      
      const citoyensData = await citoyensRes.json();
      const municipalitesData = await municipalitesRes.json();
      
      setCitoyens(citoyensData);
      setMunicipalites(municipalitesData);
      console.log('Municipality data sample:', municipalitesData[0]);
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCitizen = async (formData) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/citoyens', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (response.ok) {
        alert('Citoyen ajouté avec succès!');
        setShowCitizenForm(false);
        fetchData();
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de l\'ajout du citoyen');
    }
  };

  const handleAddMunicipality = async (formData) => {
    try {
      console.log('Sending data:', formData);
      const response = await fetch('http://localhost:5000/api/municipalites', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      const result = await response.json();
      console.log('Response:', result);
      
      if (response.ok) {
        alert('Municipalité ajoutée avec succès!');
        setShowMunicipalityForm(false);
        fetchData();
      } else {
        alert('Erreur: ' + (result.error || 'Erreur inconnue'));
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de l\'ajout de la municipalité: ' + error.message);
    }
  };

  const handleDeleteCitizen = async (citizenId) => {
    if (window.confirm('Voulez-vous vraiment supprimer ce citoyen ?')) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/citoyens/${citizenId}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          alert('Citoyen supprimé avec succès!');
          fetchData();
        }
      } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la suppression');
      }
    }
  };

  const handleEditCitizen = (citizen) => {
    setEditingCitizen(citizen);
  };

  const handleUpdateCitizen = async (formData) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/citoyens/${editingCitizen.citizenID}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (response.ok) {
        alert('Citoyen modifié avec succès!');
        setEditingCitizen(null);
        fetchData();
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la modification');
    }
  };

  const handleEditMunicipality = (municipality) => {
    console.log('Edit municipality clicked:', municipality);
    console.log('Municipality keys:', Object.keys(municipality));
    setEditingMunicipality(municipality);
  };

  const handleUpdateMunicipality = async (formData) => {
    try {
      const municipalityId = editingMunicipality.municipaliteID;
      const response = await fetch(`http://127.0.0.1:5000/api/municipalites/${municipalityId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (response.ok) {
        alert('Municipalité modifiée avec succès!');
        setEditingMunicipality(null);
        fetchData();
      } else {
        alert('Erreur lors de la modification: ' + response.status);
      }
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la modification');
    }
  };

  const handleDeleteMunicipality = async (municipalityId) => {
    if (window.confirm('Voulez-vous vraiment supprimer cette municipalité ?')) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/municipalites/${municipalityId}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          alert('Municipalité supprimée avec succès!');
          fetchData();
        } else {
          alert('Erreur lors de la suppression: ' + response.status);
        }
      } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la suppression');
      }
    }
  };

  const showMunicipalityCitizens = async (municipalityId, municipalityName) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/municipality-citizens/${municipalityId}`);
      const data = await response.json();
      setMunicipalityCitizens(data);
      setShowingCitizens(municipalityName);
    } catch (error) {
      console.error('Erreur:', error);
      alert('Erreur lors de la récupération des citoyens');
    }
  };

  return (
    <div className="page-content">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">Citoyens & Municipalités</h2>
        {/* Add buttons for creating new entries */}
        <div className="mt-8 flex justify-center space-x-4">
          <button 
            onClick={() => setShowCitizenForm(true)}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            ➕ Ajouter Citoyen
          </button>
          <button 
            onClick={() => setShowMunicipalityForm(true)}
            className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            ➕ Ajouter Municipalité
          </button>
          <button 
            onClick={() => window.location.href = '/ai-matching'}
            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            🤖 IA Matching
          </button>
          <button 
            onClick={() => window.location.href = '/citizen-requests'}
            className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-xl font-semibold transition"
          >
            📋 Demandes Citoyennes
          </button>
        </div>
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Citizens Section */}
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="text-4xl mr-3">👥</span>
              Citoyens Actifs
            </h3>

            <div className="mb-6 p-4 bg-emerald-50 rounded-xl">
              <div className="flex justify-between items-center">
                <span className="text-gray-700 font-semibold">Total Citoyens</span>
                <span className="text-3xl font-bold text-emerald-600">{citoyens.length}</span>
              </div>
            </div>

            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">Chargement...</p>
              </div>
            ) : (
              <div className="space-y-4">
                {citoyens.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">Aucun citoyen trouvé</p>
                ) : (
                  citoyens.map((citoyen, idx) => (
                    <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-emerald-50 transition">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-emerald-200 rounded-full flex items-center justify-center text-2xl">
                          👤
                        </div>
                        <div>
                          <h4 className="font-bold text-gray-800">{citoyen.neaemcitoyen || 'N/A'}</h4>
                          <p className="text-sm text-gray-600">{citoyen.addresscit || 'Adresse non spécifiée'}</p>
                          <p className="text-xs text-gray-500">Âge: {citoyen.age || 'N/A'} | Tel: {citoyen.phoneNumber || 'N/A'}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <p className="font-bold text-emerald-600">{citoyen.citizenID}</p>
                          <p className="text-xs text-gray-500">ID Citoyen</p>
                        </div>
                        <div className="flex space-x-2">
                          <button 
                            onClick={() => handleEditCitizen(citoyen)}
                            className="text-blue-600 hover:text-blue-800 p-1"
                          >
                            ✏️
                          </button>
                          <button 
                            onClick={() => handleDeleteCitizen(citoyen.citizenID)}
                            className="text-red-600 hover:text-red-800 p-1"
                          >
                            🗑️
                          </button>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>

          {/* Municipalities Section */}
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="text-4xl mr-3">🏛️</span>
              Municipalités Partenaires
            </h3>

            <div className="mb-6 p-4 bg-teal-50 rounded-xl">
              <div className="flex justify-between items-center">
                <span className="text-gray-700 font-semibold">Municipalités</span>
                <span className="text-3xl font-bold text-teal-600">{municipalites.length}</span>
              </div>
            </div>

            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">Chargement...</p>
              </div>
            ) : (
              <div className="space-y-4">
                {municipalites.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">Aucune municipalité trouvée</p>
                ) : (
                  municipalites.map((muni, idx) => (
                    <div key={idx} className="p-6 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl border-l-4 border-emerald-500 relative">
                      <div className="absolute top-4 right-4 flex space-x-2">
                        <button 
                          onClick={() => handleEditMunicipality(muni)}
                          className="text-blue-600 hover:text-blue-800 p-1"
                        >
                          ✏️
                        </button>
                        <button 
                          onClick={() => handleDeleteMunicipality(muni.municipaliteID)}
                          className="text-red-600 hover:text-red-800 p-1"
                        >
                          🗑️
                        </button>
                      </div>
                      <button
                        onClick={() => showMunicipalityCitizens(muni.municipaliteID, muni.nom)}
                        className="mt-3 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
                      >
                        👥 Afficher les citoyens
                      </button>
                      <h4 className="font-bold text-gray-800 text-lg mb-2 pr-16">{muni.nom || 'Nom non spécifié'}</h4>
                      <div className="grid grid-cols-2 gap-4 mt-4">
                        <div>
                          <p className="text-sm text-gray-600">Région</p>
                          <p className="text-lg font-bold text-emerald-600">{muni.region || 'N/A'}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Population</p>
                          <p className="text-lg font-bold text-emerald-600">{muni.population || 'N/A'}</p>
                        </div>
                      </div>
                      <div className="mt-3 text-sm text-gray-600">
                        <p>📍 {muni.adresse || 'Adresse non spécifiée'}</p>
                        <p>📞 {muni.telephone || 'N/A'} | ✉️ {muni.email || 'N/A'}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>

      </div>

      {showCitizenForm && (
        <AddCitizenForm
          onSubmit={handleAddCitizen}
          onCancel={() => setShowCitizenForm(false)}
        />
      )}

      {showMunicipalityForm && (
        <AddMunicipalityForm
          onSubmit={handleAddMunicipality}
          onCancel={() => setShowMunicipalityForm(false)}
        />
      )}

      {editingCitizen && (
        <AddCitizenForm
          initialData={editingCitizen}
          onSubmit={handleUpdateCitizen}
          onCancel={() => setEditingCitizen(null)}
          isEdit={true}
        />
      )}

      {editingMunicipality && (
        <AddMunicipalityForm
          initialData={editingMunicipality}
          onSubmit={handleUpdateMunicipality}
          onCancel={() => setEditingMunicipality(null)}
          isEdit={true}
        />
      )}

      {showingCitizens && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4 max-h-96 overflow-y-auto">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              Citoyens de {showingCitizens}
            </h3>
            <div className="space-y-3">
              {municipalityCitizens.length > 0 ? (
                municipalityCitizens.map((citizen, idx) => (
                  <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                    <div className="font-semibold">{citizen.nom}</div>
                    <div className="text-sm text-gray-600">{citizen.adresse}</div>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-4">
                  Aucun citoyen assigné à cette municipalité
                </p>
              )}
            </div>
            <button
              onClick={() => setShowingCitizens(null)}
              className="mt-6 w-full bg-gray-500 text-white py-3 rounded-xl font-semibold hover:bg-gray-600 transition"
            >
              Fermer
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
