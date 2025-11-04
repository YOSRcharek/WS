import React, { useState, useEffect } from 'react';
import { getCamionsBenne, createCamionBenne, updateCamionBenne, deleteCamionBenne } from '../../services/equipmentService';

export default function CamionsBennePage() {
  const [camions, setCamions] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentCamion, setCurrentCamion] = useState(null);
  const [formData, setFormData] = useState({
    nomEquipement: '',
    capacite: '',
    etat: 'disponible',
    localisation: '',
    volumeBenne: '',
    serviceTransport: ''
  });
  const [services, setServices] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const camionsData = await getCamionsBenne();
        setCamions(camionsData);
        
        try {
          const [camionsResponse, dangereuxResponse] = await Promise.all([
            fetch('http://localhost:5000/api/camions-dechets'),
            fetch('http://localhost:5000/api/transports-dechets-dangereux')
          ]);
          
          const allServices = [];
          if (camionsResponse.ok) {
            const camionsData = await camionsResponse.json();
            camionsData.forEach(service => {
              allServices.push({
                ...service,
                displayName: `Camion Déchets - ${service.id}`
              });
            });
          }
          if (dangereuxResponse.ok) {
            const dangereuxData = await dangereuxResponse.json();
            dangereuxData.forEach(service => {
              allServices.push({
                ...service,
                displayName: `Transport Dangereux - ${service.id}`
              });
            });
          }
          
          setServices(allServices);
        } catch (err) {
          console.log('Services non disponibles');
        }
      } catch (error) {
        console.error("Erreur lors du chargement:", error);
        setError(error.response?.data?.message || "Erreur lors du chargement");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let camionId;
      if (currentCamion) {
        await updateCamionBenne(currentCamion.id, formData);
        camionId = currentCamion.id;
      } else {
        const result = await createCamionBenne(formData);
        camionId = result.id;
      }
      
      // Assigner au service si sélectionné
      if (formData.serviceTransport && camionId) {
        try {
          await fetch(`http://localhost:5000/api/equipements/${camionId}/assign/${formData.serviceTransport}`, {
            method: 'POST'
          });
        } catch (err) {
          console.log('Erreur assignation:', err);
        }
      }
      
      setIsModalOpen(false);
      setCurrentCamion(null);
      setFormData({ nomEquipement: '', capacite: '', etat: 'disponible', localisation: '', volumeBenne: '', serviceTransport: '' });
      
      // Recharger les camions et services
      const [camionsData, camionsResponse, dangereuxResponse] = await Promise.all([
        getCamionsBenne(),
        fetch('http://localhost:5000/api/camions-dechets'),
        fetch('http://localhost:5000/api/transports-dechets-dangereux')
      ]);
      
      setCamions(camionsData);
      
      // Recharger les services
      const allServices = [];
      if (camionsResponse.ok) {
        const camionsServicesData = await camionsResponse.json();
        camionsServicesData.forEach(service => {
          allServices.push({
            ...service,
            displayName: `Camion Déchets - ${service.id}`
          });
        });
      }
      if (dangereuxResponse.ok) {
        const dangereuxData = await dangereuxResponse.json();
        dangereuxData.forEach(service => {
          allServices.push({
            ...service,
            displayName: `Transport Dangereux - ${service.id}`
          });
        });
      }
      setServices(allServices);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      setError(error.response?.data?.message || 'Erreur lors de la sauvegarde');
    }
  };

  const handleEdit = (camion) => {
    setCurrentCamion(camion);
    setFormData({
      nomEquipement: camion.nomEquipement,
      capacite: camion.capacite,
      etat: camion.etat,
      localisation: camion.localisation,
      volumeBenne: camion.volumeBenne || ''
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce camion benne ?')) {
      try {
        await deleteCamionBenne(id);
        const data = await getCamionsBenne();
        setCamions(data);
      } catch (error) {
        console.error('Erreur lors de la suppression:', error);
        setError(error.response?.data?.message || 'Erreur lors de la suppression');
      }
    }
  };

  const openAddModal = () => {
    setCurrentCamion(null);
    setFormData({ nomEquipement: '', capacite: '', etat: 'disponible', localisation: '', volumeBenne: '', serviceTransport: '' });
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
              <span className="text-4xl mr-3">🚚</span> Camions Benne
            </h2>
          </div>
          <button
            onClick={openAddModal}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors"
          >
            + Ajouter un camion benne
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
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nom</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Capacité</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Volume Benne</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">État</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Localisation</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Service Assigné</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {camions.map((camion, index) => (
                <tr key={camion.id || index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{camion.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{camion.nomEquipement}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{camion.capacite}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{camion.volumeBenne}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{camion.etat}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{camion.localisation}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{camion.serviceAssigne}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button
                      onClick={() => handleEdit(camion)}
                      className="text-indigo-600 hover:text-indigo-900 mr-4"
                    >
                      Modifier
                    </button>
                    <button
                      onClick={() => handleDelete(camion.id)}
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
                {currentCamion ? 'Modifier le camion benne' : 'Ajouter un camion benne'}
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="nomEquipement" className="block text-sm font-medium text-gray-700 mb-2">
                  Nom de l'équipement *
                </label>
                <input
                  type="text"
                  id="nomEquipement"
                  name="nomEquipement"
                  value={formData.nomEquipement}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="capacite" className="block text-sm font-medium text-gray-700 mb-2">
                    Capacité *
                  </label>
                  <input
                    type="number"
                    id="capacite"
                    name="capacite"
                    value={formData.capacite}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="volumeBenne" className="block text-sm font-medium text-gray-700 mb-2">
                    Volume de la benne *
                  </label>
                  <input
                    type="number"
                    id="volumeBenne"
                    name="volumeBenne"
                    value={formData.volumeBenne}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  >
                    <option value="disponible">Disponible</option>
                    <option value="en_maintenance">En maintenance</option>
                    <option value="hors_service">Hors service</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="localisation" className="block text-sm font-medium text-gray-700 mb-2">
                    Localisation *
                  </label>
                  <input
                    type="text"
                    id="localisation"
                    name="localisation"
                    value={formData.localisation}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                </div>
              </div>

              <div>
                <label htmlFor="serviceTransport" className="block text-sm font-medium text-gray-700 mb-2">
                  Service de Transport
                </label>
                <select
                  id="serviceTransport"
                  name="serviceTransport"
                  value={formData.serviceTransport}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Sélectionner un service</option>
                  {services.map(service => (
                    <option key={service.id} value={service.id}>{service.displayName}</option>
                  ))}
                </select>
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
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {currentCamion ? 'Mettre à jour' : 'Créer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}