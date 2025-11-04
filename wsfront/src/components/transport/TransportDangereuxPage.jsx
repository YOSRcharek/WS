import React, { useState, useEffect } from 'react';
import { getTransportsDangereux, createTransportDangereux, updateTransportDangereux, deleteTransportDangereux } from '../../services/transportService';

export default function TransportDangereuxPage() {
  const [transports, setTransports] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTransport, setCurrentTransport] = useState(null);
  const [formData, setFormData] = useState({
    zoneCouverture: '',
    capaciteMax: '',
    etat: 'actif',
    typeDechetDangereux: '',
    normesSecurite: ''
  });

  useEffect(() => {
    const fetchTransports = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getTransportsDangereux();
        setTransports(data);
      } catch (error) {
        console.error("Erreur lors du chargement des transports:", error);
        setError(error.response?.data?.message || "Erreur lors du chargement des transports");
      } finally {
        setLoading(false);
      }
    };

    fetchTransports();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (currentTransport) {
        await updateTransportDangereux(currentTransport.id, formData);
      } else {
        await createTransportDangereux(formData);
      }
      setIsModalOpen(false);
      setCurrentTransport(null);
      setFormData({ zoneCouverture: '', capaciteMax: '', etat: 'actif', typeDechetDangereux: '', normesSecurite: '' });
      const data = await getTransportsDangereux();
      setTransports(data);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      setError(error.response?.data?.message || 'Erreur lors de la sauvegarde');
    }
  };

  const handleEdit = (transport) => {
    setCurrentTransport(transport);
    setFormData({
      zoneCouverture: transport.zoneCouverture || '',
      capaciteMax: transport.capaciteMax || '',
      etat: transport.etat || 'actif',
      typeDechetDangereux: transport.typeDechetDangereux || '',
      normesSecurite: transport.normesSecurite || ''
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce transport ?')) {
      try {
        await deleteTransportDangereux(id);
        const data = await getTransportsDangereux();
        setTransports(data);
      } catch (error) {
        console.error('Erreur lors de la suppression:', error);
        setError(error.response?.data?.message || 'Erreur lors de la suppression');
      }
    }
  };

  const openAddModal = () => {
    setCurrentTransport(null);
    setFormData({ zoneCouverture: '', capaciteMax: '', etat: 'actif', typeDechetDangereux: '', normesSecurite: '' });
    setIsModalOpen(true);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="bg-white rounded-3xl shadow-xl p-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center">
            <button
              onClick={() => window.history.back()}
              className="mr-4 text-gray-600 hover:text-gray-800 text-2xl"
            >
              ←
            </button>
            <h2 className="text-3xl font-bold text-gray-800 flex items-center">
              <span className="text-4xl mr-3">⚠️</span> Transport Déchets Dangereux
            </h2>
          </div>
          <button
            onClick={openAddModal}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors"
          >
            + Ajouter un transport
          </button>
        </div>

        {loading && (
          <div className="text-center py-4">
            <p className="text-gray-600">Chargement des données...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            <p>{error}</p>
          </div>
        )}

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capacité Max</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type Déchet Dangereux</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Normes Sécurité</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">État</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Zone Couverture</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transports.map((transport, index) => (
                <tr key={transport.id || index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{transport.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transport.capaciteMax}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transport.typeDechetDangereux}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transport.normesSecurite}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transport.etat}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{transport.zoneCouverture}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => handleEdit(transport)}
                      className="text-indigo-600 hover:text-indigo-900 mr-4"
                    >
                      Modifier
                    </button>
                    <button
                      onClick={() => handleDelete(transport.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Supprimer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal de formulaire */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl p-8 w-full max-w-2xl">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-gray-800">
                {currentTransport ? 'Modifier le transport' : 'Ajouter un transport'}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="zoneCouverture" className="block text-sm font-medium text-gray-700 mb-2">
                    Zone de couverture *
                  </label>
                  <input
                    type="text"
                    id="zoneCouverture"
                    name="zoneCouverture"
                    value={formData.zoneCouverture}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="capaciteMax" className="block text-sm font-medium text-gray-700 mb-2">
                    Capacité maximale *
                  </label>
                  <input
                    type="number"
                    id="capaciteMax"
                    name="capaciteMax"
                    value={formData.capaciteMax}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="etat" className="block text-sm font-medium text-gray-700 mb-2">
                    État *
                  </label>
                  <select
                    id="etat"
                    name="etat"
                    value={formData.etat}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    required
                  >
                    <option value="actif">Actif</option>
                    <option value="inactif">Inactif</option>
                    <option value="maintenance">En maintenance</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="typeDechetDangereux" className="block text-sm font-medium text-gray-700 mb-2">
                    Type de déchet dangereux *
                  </label>
                  <input
                    type="text"
                    id="typeDechetDangereux"
                    name="typeDechetDangereux"
                    value={formData.typeDechetDangereux}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="normesSecurite" className="block text-sm font-medium text-gray-700 mb-2">
                  Normes de sécurité *
                </label>
                <textarea
                  id="normesSecurite"
                  name="normesSecurite"
                  value={formData.normesSecurite}
                  onChange={handleInputChange}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                  required
                />
              </div>

              <div className="flex justify-end space-x-4 pt-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                  {currentTransport ? 'Mettre à jour' : 'Créer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}