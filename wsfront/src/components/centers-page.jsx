import React, { useState, useEffect } from "react";
import {
  getCentres, addCentre, updateCentre, deleteCentre
} from "../services/centreRecyclageService";
import {
  getPointsCollecte, addPointCollecte, updatePointCollecte, deletePointCollecte, addPointCollecteNLP, filterPointsCollecte
} from "../services/pointsCollecteService";

export default function CentersPage() {
  const [recyclingCenters, setRecyclingCenters] = useState([]);
  const [collectionPoints, setCollectionPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Pour le formulaire CRUD centres
  const [formData, setFormData] = useState({
    centerName: "",
    capacity_center: "",
    energyConsumption: "",
    location_center: "",
    typeDeDechetTraite: "",
    operation_Status: "",
    recyclingRate: "",
    type: "centre_de_recyclage",
  });
  const [editingId, setEditingId] = useState(null);
  const [showForm, setShowForm] = useState(false);

  // Pour le formulaire CRUD points de collecte
  const [pointFormData, setPointFormData] = useState({
    name: "",
    location: "",
    description: "",
    type: "mobile",
    centre_id: "",
  });
  const [editingPointId, setEditingPointId] = useState(null);
  const [showPointForm, setShowPointForm] = useState(false);

  // Pour l'IA NLP
  const [nlpPhrase, setNlpPhrase] = useState("");
  const [showNlpForm, setShowNlpForm] = useState(false);

  // Pour le filtrage des points
  const [filteredPoints, setFilteredPoints] = useState([]);
  const [showFilteredPoints, setShowFilteredPoints] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [centersData, pointsData] = await Promise.all([
        getCentres(),
        getPointsCollecte()
      ]);
      setRecyclingCenters(centersData.results || []);
      setCollectionPoints(pointsData.results || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePointChange = (e) => {
    const { name, value } = e.target;
    setPointFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await updateCentre(editingId, formData);
      } else {
        await addCentre(formData);
      }
      setFormData({
        centerName: "",
        capacity_center: "",
        energyConsumption: "",
        location_center: "",
        typeDeDechetTraite: "",
        operation_Status: "",
        recyclingRate: "",
        type: "centre_de_recyclage",
      });
      setEditingId(null);
      setShowForm(false);
      fetchData();
    } catch (err) {
      alert("Erreur: " + err.message);
    }
  };

  const handlePointSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingPointId) {
        await updatePointCollecte(editingPointId, pointFormData);
      } else {
        await addPointCollecte(pointFormData);
      }
      setPointFormData({
        name: "",
        location: "",
        description: "",
        type: "mobile",
        centre_id: "",
      });
      setEditingPointId(null);
      setShowPointForm(false);
      fetchData();
    } catch (err) {
      alert("Erreur: " + err.message);
    }
  };

  const handleEdit = (center) => {
    setFormData(center);
    setEditingId(center.centreID);
    setShowForm(true);
  };

  const handleEditPoint = (point) => {
    setPointFormData(point);
    setEditingPointId(point.pointID);
    setShowPointForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Voulez-vous vraiment supprimer ce centre ?")) {
      console.log("Supprimer centre ID:", id); // debug
      await deleteCentre(id);
      fetchData(); // recharger les données
    }
  };

  const handleDeletePoint = async (point) => {
    if (window.confirm("Voulez-vous vraiment supprimer ce point de collecte ?")) {
      await deletePointCollecte(point.pointID);
      fetchData();
    }
  };

  const handleNlpSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await addPointCollecteNLP(nlpPhrase);
      alert(result.message || "Point ajouté avec succès via IA !");
      setNlpPhrase("");
      setShowNlpForm(false);
      fetchData();
    } catch (err) {
      alert("Erreur IA: " + err.message);
    }
  };

  const handleFilterPoints = async () => {
    try {
      const result = await filterPointsCollecte();
      setFilteredPoints(result.points_filtered || []);
      setShowFilteredPoints(true);
    } catch (err) {
      alert("Erreur lors du filtrage: " + err.message);
    }
  };


  if (loading)
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-gray-500 text-lg animate-pulse">Chargement des centres...</p>
      </div>
    );

  if (error)
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-red-500 text-lg">{error}</p>
      </div>
    );

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <h2 className="text-4xl font-extrabold text-gray-800 mb-8 text-center">
        Centres de Recyclage & Points de Collecte
      </h2>

      {/* Boutons pour ouvrir les formulaires */}
      <div className="text-center mb-8 space-x-4">
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-emerald-500 hover:bg-emerald-600 text-white font-bold px-6 py-2 rounded-full transition"
        >
          {showForm ? "Fermer le formulaire" : "Ajouter un centre"}
        </button>
        <button
          onClick={() => setShowPointForm(!showPointForm)}
          className="bg-teal-500 hover:bg-teal-600 text-white font-bold px-6 py-2 rounded-full transition"
        >
          {showPointForm ? "Fermer le formulaire" : "Ajouter un point de collecte"}
        </button>
        <button
          onClick={() => setShowNlpForm(!showNlpForm)}
          className="bg-purple-500 hover:bg-purple-600 text-white font-bold px-6 py-2 rounded-full transition"
        >
          {showNlpForm ? "Fermer IA" : "Ajouter via IA"}
        </button>
        <button
          onClick={handleFilterPoints}
          className="bg-orange-500 hover:bg-orange-600 text-white font-bold px-6 py-2 rounded-full transition"
        >
          Filtrer Points
        </button>
      </div>

      {/* Formulaire CRUD Centres */}
      {showForm && (
        <div className="bg-white p-6 rounded-3xl shadow-2xl mb-8">
          <h3 className="text-2xl font-bold mb-4">
            {editingId ? "Modifier le centre" : "Ajouter un centre"}
          </h3>
          <form className="grid grid-cols-1 md:grid-cols-2 gap-4" onSubmit={handleSubmit}>
            <input
              type="text"
              name="centerName"
              placeholder="Nom du centre"
              value={formData.centerName}
              onChange={handleChange}
              required
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="text"
              name="location_center"
              placeholder="Localisation"
              value={formData.location_center}
              onChange={handleChange}
              required
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="number"
              name="capacity_center"
              placeholder="Capacité (tonnes)"
              value={formData.capacity_center}
              onChange={handleChange}
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="text"
              name="operation_Status"
              placeholder="Statut"
              value={formData.operation_Status}
              onChange={handleChange}
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="text"
              name="typeDeDechetTraite"
              placeholder="Type de déchets traités"
              value={formData.typeDeDechetTraite}
              onChange={handleChange}
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="number"
              name="recyclingRate"
              placeholder="Taux de recyclage (%)"
              value={formData.recyclingRate}
              onChange={handleChange}
              className="border p-2 rounded-lg w-full"
            />
            <select
              name="type"
              value={formData.type}
              onChange={handleChange}
              className="border p-2 rounded-lg w-full"
            >
              <option value="centre_de_recyclage">Centre de Recyclage</option>
              <option value="centre_de_compostage">Centre de Compostage</option>
              <option value="centre_de_traitement_dangereux">Traitement déchets dangereux</option>
              <option value="usine_recyclage_metaux">Usine recyclage métaux</option>
            </select>
            <button
              type="submit"
              className="bg-emerald-500 hover:bg-emerald-600 text-white font-bold px-6 py-2 rounded-full md:col-span-2 transition"
            >
              {editingId ? "Modifier" : "Ajouter"}
            </button>
          </form>
        </div>
      )}

      {/* Formulaire CRUD Points de Collecte */}
      {showPointForm && (
        <div className="bg-white p-6 rounded-3xl shadow-2xl mb-8">
          <h3 className="text-2xl font-bold mb-4">
            {editingPointId ? "Modifier le point de collecte" : "Ajouter un point de collecte"}
          </h3>
          <form className="grid grid-cols-1 md:grid-cols-2 gap-4" onSubmit={handlePointSubmit}>
            <input
              type="text"
              name="name"
              placeholder="Nom du point"
              value={pointFormData.name}
              onChange={handlePointChange}
              required
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="text"
              name="location"
              placeholder="Localisation"
              value={pointFormData.location}
              onChange={handlePointChange}
              required
              className="border p-2 rounded-lg w-full"
            />
            <input
              type="text"
              name="description"
              placeholder="Description"
              value={pointFormData.description}
              onChange={handlePointChange}
              className="border p-2 rounded-lg w-full"
            />
            <select
              name="type"
              value={pointFormData.type}
              onChange={handlePointChange}
              className="border p-2 rounded-lg w-full"
            >
              <option value="mobile">Mobile</option>
              <option value="poubelle">Poubelle Publique</option>
            </select>
            <select
              name="centre_id"
              value={pointFormData.centre_id}
              onChange={handlePointChange}
              className="border p-2 rounded-lg w-full"
            >
              <option value="">Sélectionner un centre (optionnel)</option>
              {recyclingCenters.map(center => (
                <option key={center.centreID} value={center.centreID}>
                  {center.centerName}
                </option>
              ))}
            </select>
            <button
              type="submit"
              className="bg-teal-500 hover:bg-teal-600 text-white font-bold px-6 py-2 rounded-full md:col-span-2 transition"
            >
              {editingPointId ? "Modifier" : "Ajouter"}
            </button>
          </form>
        </div>
      )}

      {/* Formulaire IA NLP */}
      {showNlpForm && (
        <div className="bg-white p-6 rounded-3xl shadow-2xl mb-8">
          <h3 className="text-2xl font-bold mb-4">
            Ajouter un point de collecte via IA
          </h3>
          <p className="text-gray-600 mb-4">
            Exemple: "Ajoute un point de collecte mobile nommé Point ven11 à Tunis associé au centre Cpo"
          </p>
          <form onSubmit={handleNlpSubmit}>
            <textarea
              value={nlpPhrase}
              onChange={(e) => setNlpPhrase(e.target.value)}
              placeholder="Entrez une phrase pour créer un point de collecte..."
              required
              className="border p-2 rounded-lg w-full h-24 resize-none"
            />
            <button
              type="submit"
              className="bg-purple-500 hover:bg-purple-600 text-white font-bold px-6 py-2 rounded-full mt-4 transition"
            >
              Ajouter via IA
            </button>
          </form>
        </div>
      )}

      {/* Liste des centres */}
      <div className="grid lg:grid-cols-2 gap-10 mb-12">
        {recyclingCenters.map((center, idx) => (
          <div 
            key={center.centreID || idx} 
            className="bg-white rounded-3xl shadow-2xl p-6 hover:scale-105 transition-transform duration-300"
          >
            <div className="flex justify-between items-start mb-4">
              <h4 className="font-bold text-gray-800 text-lg">{center.centerName}</h4>
              <div className="space-x-2">
                <button 
                  onClick={() => handleEdit(center)}
                  className="text-blue-500 hover:text-blue-700 font-semibold"
                >
                  Modifier
                </button>
                <button 
                  onClick={() => handleDelete(center.centreID)}
                  className="text-red-500 hover:text-red-700 font-semibold"
                >
                  Supprimer
                </button>
              </div>
            </div>
            <p className="text-gray-600 text-sm">📍 {center.location_center || 'Localisation non disponible'}</p>
            <p className="text-gray-600 text-sm">⏰ Statut: {center.operation_Status || 'Non spécifié'}</p>
            <p className="text-emerald-600 font-semibold text-sm mt-2">
              Capacité: {center.capacity_center || 'Non spécifiée'} tonnes
            </p>
            <p className="text-emerald-600 font-semibold text-sm">
              Taux de recyclage: {center.recyclingRate || 'Non spécifié'}%
            </p>
          </div>
        ))}
      </div>

      {/* Points de collecte */}
      <div className="bg-white rounded-3xl shadow-2xl p-8 mb-12">
        <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <span className="text-4xl mr-3">📍</span> Points de Collecte
        </h3>
        <div className="space-y-4">
          {collectionPoints.length > 0 ? (
            collectionPoints.map((point, idx) => (
              <div
                key={point.pointID || idx}
                className="border-l-4 border-teal-500 pl-4 py-4 bg-teal-50 rounded-r-2xl shadow-inner hover:shadow-md transition-shadow duration-300"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-gray-800">{point.name}</h4>
                    <p className="text-gray-600 text-sm mt-1">📍 {point.location}</p>
                    <p className="text-teal-600 font-semibold text-sm mt-2">
                      Description: {point.description || 'Non spécifiée'}
                    </p>
                    <p className="text-teal-600 font-semibold text-sm">
                      Type: {point.type || 'Non spécifié'}
                    </p>
                  </div>
                  <div className="space-x-2">
                    <button
                      onClick={() => handleEditPoint(point)}
                      className="text-blue-500 hover:text-blue-700 font-semibold"
                    >
                      Modifier
                    </button>
                    <button
                      onClick={() => handleDeletePoint(point)}
                      className="text-red-500 hover:text-red-700 font-semibold"
                    >
                      Supprimer
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-600">Aucun point de collecte trouvé.</p>
          )}
        </div>
      </div>

      {/* Points de collecte filtrés */}
      {showFilteredPoints && (
        <div className="bg-white rounded-3xl shadow-2xl p-8 mb-12">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🔍</span> Points de Collecte Filtrés (Capacité {'>'} 100)
          </h3>
          <div className="space-y-4">
            {filteredPoints.length > 0 ? (
              filteredPoints.map((point, idx) => (
                <div
                  key={point.point_uri || idx}
                  className="border-l-4 border-orange-500 pl-4 py-4 bg-orange-50 rounded-r-2xl shadow-inner hover:shadow-md transition-shadow duration-300"
                >
                  <div>
                    <h4 className="font-bold text-gray-800">{point.name}</h4>
                    <p className="text-gray-600 text-sm mt-1">📍 {point.location}</p>
                    <p className="text-orange-600 font-semibold text-sm mt-2">
                      Centre: {point.centre_uri}
                    </p>
                    <p className="text-orange-600 font-semibold text-sm">
                      Capacité du centre: {point.capacity} tonnes
                    </p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-600">Aucun point de collecte filtré trouvé.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
