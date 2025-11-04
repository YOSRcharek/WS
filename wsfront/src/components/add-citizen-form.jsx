import { useState } from "react";

export default function AddCitizenForm({ onSubmit, onCancel, initialData, isEdit }) {
  const [formData, setFormData] = useState({
    neaemcitoyen: initialData?.neaemcitoyen || "",
    addresscit: initialData?.addresscit || "",
    age: initialData?.age || "",
    email: initialData?.email || "",
    phoneNumber: initialData?.phoneNumber || "",
    type: initialData?.type || "Resident"
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
        <h3 className="text-2xl font-bold text-gray-800 mb-6">{isEdit ? 'Modifier le Citoyen' : 'Ajouter un Citoyen'}</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Nom</label>
            <input
              name="neaemcitoyen"
              value={formData.neaemcitoyen}
              onChange={handleChange}
              type="text"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Adresse</label>
            <input
              name="addresscit"
              value={formData.addresscit}
              onChange={handleChange}
              type="text"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Âge</label>
            <input
              name="age"
              value={formData.age}
              onChange={handleChange}
              type="number"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
            <input
              name="email"
              value={formData.email}
              onChange={handleChange}
              type="email"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Téléphone</label>
            <input
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange}
              type="tel"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Type</label>
            <select
              name="type"
              value={formData.type}
              onChange={handleChange}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-emerald-500 focus:outline-none"
              required
            >
              <option value="Resident">Résident</option>
              <option value="Business">Entreprise</option>
            </select>
          </div>
          <div className="flex space-x-4 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-xl font-semibold hover:bg-gray-300 transition"
            >
              Annuler
            </button>
            <button
              type="submit"
              className="flex-1 bg-emerald-500 text-white py-3 rounded-xl font-semibold hover:bg-emerald-600 transition"
            >
              {isEdit ? 'Modifier' : 'Ajouter'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}