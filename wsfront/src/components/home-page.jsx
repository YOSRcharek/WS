import React from "react";
import { useNavigate } from "react-router-dom";

const services = [
  { emoji: "♻️", title: "Tri Intelligent", description: "Système de classification automatique des déchets pour un tri optimal et efficace" },
  { emoji: "🚛", title: "Collecte Optimisée", description: "Planification intelligente des itinéraires de collecte pour réduire les coûts" },
  { emoji: "🌱", title: "Recyclage Durable", description: "Suivi complet du processus de recyclage pour un impact environnemental positif" },
];

const stats = [
  { value: "2,450", label: "Tonnes Recyclées" },
  { value: "156", label: "Points de Collecte" },
  { value: "12,500", label: "Citoyens Actifs" },
  { value: "98%", label: "Satisfaction" },
];

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="page-content">
      {/* Hero Section */}
      <section className="relative h-full py-24 overflow-hidden">
        <div className="absolute inset-0 gradient-green opacity-90"></div>
        <div className="absolute inset-0">
          <svg className="absolute bottom-0 w-full h-32 text-white" viewBox="0 0 1440 120" fill="currentColor">
            <path d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
          </svg>
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 fade-in">WasteWise</h1>
          <p className="text-xl md:text-2xl text-emerald-50 mb-8 max-w-3xl mx-auto fade-in">
            Plateforme intelligente pour l'optimisation du tri, de la collecte et du recyclage des déchets
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center fade-in">
            <button onClick={() => navigate("/add-waste")} className="btn-primary text-white px-8 py-4 rounded-full font-semibold text-lg">
              Ajouter un Déchet
            </button>
            
            <button onClick={() => navigate("/waste-list")} className="bg-white text-emerald-600 px-8 py-4 rounded-full font-semibold text-lg hover:bg-emerald-50 transition">
              Voir les Déchets
            </button>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mt-6 fade-in">
            <button onClick={() => navigate("/add-event")} className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-4 rounded-full font-semibold text-lg transition">
              Créer un Événement
            </button>
            <button onClick={() => navigate("/add-campaign")} className="bg-purple-500 hover:bg-purple-600 text-white px-8 py-4 rounded-full font-semibold text-lg transition">
              Lancer une Campagne
            </button>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center text-gray-800 mb-16">Nos Services</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {services.map((service, idx) => (
              <div key={idx} className="card-hover bg-gradient-to-br from-emerald-50 to-green-50 p-8 rounded-2xl shadow-lg">
                <div className="waste-icon mb-6 text-4xl">{service.emoji}</div>
                <h3 className="text-2xl font-bold text-gray-800 mb-4">{service.title}</h3>
                <p className="text-gray-600 leading-relaxed">{service.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-20 gradient-green">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            {stats.map((stat, idx) => (
              <div key={idx} className="stat-card p-8 rounded-2xl">
                <div className="text-4xl font-bold text-emerald-600 mb-2">{stat.value}</div>
                <div className="text-gray-600 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
