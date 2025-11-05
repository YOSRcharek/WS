<<<<<<< HEAD
import React, { useState, useEffect } from "react";
import {
  getCentres, addCentre, updateCentre, deleteCentre
} from "../services/centreRecyclageService";
import {
  getPointsCollecte, addPointCollecte, updatePointCollecte, deletePointCollecte
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
=======
import React from "react";

const recyclingCenters = [
  {
    name: "Centre EcoVert Nord",
    location: "Zone Industrielle Nord, Casablanca",
    hours: "Lun-Sam: 8h-18h",
    capacity: "500 tonnes/mois",
  },
  {
    name: "Centre RecycloPlus",
    location: "Avenue Hassan II, Rabat",
    hours: "Lun-Ven: 9h-17h",
    capacity: "350 tonnes/mois",
  },
  {
    name: "Centre GreenTech Sud",
    location: "Quartier Industriel, Marrakech",
    hours: "Lun-Sam: 7h-19h",
    capacity: "420 tonnes/mois",
  },
];

const collectionPoints = [
  {
    name: "Point Quartier Maarif",
    location: "Boulevard Zerktouni, Casablanca",
    types: "Plastique, Verre, Papier",
  },
  {
    name: "Point Centre Ville",
    location: "Place Mohammed V, Rabat",
    types: "Tous types de déchets",
  },
  {
    name: "Point Résidentiel Agdal",
    location: "Avenue des FAR, Rabat",
    types: "Organique, Plastique, Métal",
  },
  {
    name: "Point Médina",
    location: "Bab Ftouh, Marrakech",
    types: "Papier, Carton, Verre",
  },
];

export default function CentersPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h2 className="text-4xl font-bold text-gray-800 mb-12 text-center">
        Centres de Recyclage & Points de Collecte
      </h2>

      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">🏭</span> Centres de Recyclage
          </h3>
          <div className="space-y-4">
            {recyclingCenters.map((center, idx) => (
              <div
                key={idx}
                className="border-l-4 border-emerald-500 pl-4 py-3 bg-emerald-50 rounded-r-xl"
              >
                <h4 className="font-bold text-gray-800">{center.name}</h4>
                <p className="text-gray-600 text-sm mt-1">📍 {center.location}</p>
                <p className="text-gray-600 text-sm">⏰ {center.hours}</p>
                <p className="text-emerald-600 font-semibold text-sm mt-2">
                  Capacité: {center.capacity}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-xl p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="text-4xl mr-3">📍</span> Points de Collecte
          </h3>
          <div className="space-y-4">
            {collectionPoints.map((point, idx) => (
              <div
                key={idx}
                className="border-l-4 border-teal-500 pl-4 py-3 bg-teal-50 rounded-r-xl"
              >
                <h4 className="font-bold text-gray-800">{point.name}</h4>
                <p className="text-gray-600 text-sm mt-1">📍 {point.location}</p>
                <p className="text-teal-600 font-semibold text-sm mt-2">
                  Types: {point.types}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-br from-emerald-500 to-teal-500 rounded-3xl shadow-xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-4">Carte Interactive</h3>
        <div className="bg-white rounded-xl h-96 flex items-center justify-center text-gray-400">
          <div className="text-center">
            <div className="text-6xl mb-4">🗺️</div>
            <p className="text-gray-600 font-semibold">
              Carte des centres et points de collecte
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Visualisation géographique interactive
            </p>
          </div>
>>>>>>> doua
        </div>
      </div>
    </div>
  );
}
