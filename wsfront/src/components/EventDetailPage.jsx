import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getEvenement } from "../services/eventService";

export default function EventDetailPage() {
  const { id } = useParams(); // ✅ récupère /event/:id
  const [config, setConfig] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      const data = await getEvenement(id);
      if (data) {
        // Mapper les noms depuis le backend vers le design
        setConfig({
          nom_event: data.nomevent || "Événement",
          date_debut: data.dateDebut || "Non spécifié",
          date_fin: data.dateFin || "Non spécifié",
          lieu: data.lieu || "Non spécifié",
          zone_cible: data.zoneCible || "",
          description_event: data.descriptionevent || "",
          type_evenement: data.typeEvenement || "",
          public_cible: data.publicCible || "",
          organisateur: "Association locale",
          campagne_associee: data.campaignID || "Aucune",
          nombre_benevoles: data.nombreBenevoles || 0,
          nombre_participants: data.nombreParticipants || 0,
          quantite_collecte: data.quantitecollecte || "0kg",
          primary_color: "#10b981",
          background_color: "#f0fdf4",
          text_color: "#1f2937",
          button_color: "#059669",
          accent_color: "#34d399",
        });
      }
    };

    fetchEvent();
  }, [id]);

  // Effet pour appliquer les styles dynamiques
  useEffect(() => {
    if (!config) return;

    document.body.style.background = `linear-gradient(to bottom right, ${config.background_color}, ${config.accent_color}20)`;
    const headers = document.querySelectorAll("h1, h2, h3");
    headers.forEach((h) => (h.style.color = config.text_color));

    const statCards = document.querySelectorAll(".stat-card .text-emerald-600");
    statCards.forEach((card) => (card.style.color = config.primary_color));

    const ctaButton = document.getElementById("cta-button");
    if (ctaButton) {
      ctaButton.style.background = `linear-gradient(135deg, ${config.button_color} 0%, ${config.primary_color} 100%)`;
    }

    const gradientHeader = document.querySelector(".gradient-green");
    if (gradientHeader) {
      gradientHeader.style.background = `linear-gradient(135deg, ${config.button_color} 0%, ${config.primary_color} 50%, ${config.accent_color} 100%)`;
    }
  }, [config]);

  if (!config) {
    return <div className="text-center py-10 text-gray-600">Chargement des détails...</div>;
  }

  return (
    <main>
      <header className="relative h-96 gradient-green overflow-hidden">
        <div className="absolute inset-0 gradient-overlay"></div>
        <div className="relative h-full flex items-center justify-center text-center px-6">
          <div className="fade-in">
            <div className="text-7xl mb-4">🌱</div>
            <h1 id="nom-event" className="text-5xl font-bold text-white mb-4">{config.nom_event}</h1>
            <div className="flex items-center justify-center gap-6 text-white text-lg flex-wrap">
              <div className="flex items-center gap-2">
                <span className="text-2xl">📅</span> {config.date_debut} - {config.date_fin}
              </div>
              <div className="flex items-center gap-2">
                <span className="text-2xl">📍</span> {config.lieu}
              </div>
              <div className="flex items-center gap-2">
                <span className="text-2xl">🎯</span> {config.zone_cible}
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-12">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12 -mt-20 relative z-10">
          <div className="stat-card card-hover rounded-2xl p-6 text-center shadow-xl">
            <div className="info-icon mx-auto mb-3">👥</div>
            <div id="nombre-participants" className="text-3xl font-bold text-emerald-600 mb-1">{config.nombre_participants}</div>
            <div className="text-gray-600">Participants</div>
          </div>
          <div className="stat-card card-hover rounded-2xl p-6 text-center shadow-xl">
            <div className="info-icon mx-auto mb-3">🙋‍♀️</div>
            <div id="nombre-benevoles" className="text-3xl font-bold text-emerald-600 mb-1">{config.nombre_benevoles}</div>
            <div className="text-gray-600">Bénévoles</div>
          </div>
          <div className="stat-card card-hover rounded-2xl p-6 text-center shadow-xl">
            <div className="info-icon mx-auto mb-3">♻️</div>
            <div id="quantite-collecte" className="text-3xl font-bold text-emerald-600 mb-1">{config.quantite_collecte}</div>
            <div className="text-gray-600">Objectif collecte</div>
          </div>
          <div className="stat-card card-hover rounded-2xl p-6 text-center shadow-xl">
            <div className="info-icon mx-auto mb-3">🏷️</div>
            <div id="type-evenement" className="text-lg font-bold text-emerald-600 mb-1">{config.type_evenement}</div>
            <div className="text-gray-600">Type</div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            {/* À propos */}
            <section className="bg-white rounded-2xl shadow-lg p-8 fade-in">
              <h2 className="text-3xl font-bold text-gray-800 mb-4 flex items-center">
                <span className="text-4xl mr-3">📖</span> À propos de l'événement
              </h2>
              <p id="description-event" className="text-gray-600 text-lg leading-relaxed mb-6">{config.description_event}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="bg-emerald-50 border-l-4 border-emerald-500 p-4 rounded">
                  <p className="text-emerald-800"><strong>🎯 Public ciblé :</strong> {config.public_cible}</p>
                </div>
                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                  <p className="text-blue-800"><strong>📍 Zone d'action :</strong> {config.zone_cible}</p>
                </div>
              </div>
            </section>

            {/* Programme */}
            <section className="bg-white rounded-2xl shadow-lg p-8 slide-in">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                <span className="text-4xl mr-3">📋</span> Programme
              </h2>
              <div className="space-y-4">
                <div className="flex items-start gap-4 p-4 bg-emerald-50 rounded-xl">
                  <div className="text-2xl">☀️</div>
                  <div>
                    <div className="font-bold text-emerald-700">9h00 - Accueil</div>
                    <div className="text-gray-600">Inscription et distribution du matériel</div>
                  </div>
                </div>
                <div className="flex items-start gap-4 p-4 bg-emerald-50 rounded-xl">
                  <div className="text-2xl">🧹</div>
                  <div>
                    <div className="font-bold text-emerald-700">9h30 - Nettoyage</div>
                    <div className="text-gray-600">Action de nettoyage en équipes</div>
                  </div>
                </div>
                <div className="flex items-start gap-4 p-4 bg-emerald-50 rounded-xl">
                  <div className="text-2xl">🍽️</div>
                  <div>
                    <div className="font-bold text-emerald-700">12h00 - Pause déjeuner</div>
                    <div className="text-gray-600">Repas bio et local offert</div>
                  </div>
                </div>
                <div className="flex items-start gap-4 p-4 bg-emerald-50 rounded-xl">
                  <div className="text-2xl">🎉</div>
                  <div>
                    <div className="font-bold text-emerald-700">13h00 - Clôture</div>
                    <div className="text-gray-600">Bilan et remerciements</div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg p-6 fade-in">
              <div className="badge bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-semibold inline-block mb-4">Places limitées</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Participez !</h3>
              <p className="text-gray-600 mb-6">Inscrivez-vous dès maintenant et faites partie du changement.</p>
              <button id="cta-button" className="btn-primary w-full text-white font-bold py-4 px-6 rounded-xl text-lg">S'inscrire maintenant</button>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center"><span className="text-2xl mr-2">👥</span> Organisation</h3>
              <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-xl">
                  <div className="text-sm text-gray-500 mb-1">Organisateur</div>
                  <div id="organisateur" className="font-semibold text-gray-800">{config.organisateur}</div>
                </div>
                <div className="bg-gray-50 p-4 rounded-xl">
                  <div className="text-sm text-gray-500 mb-1">Campagne associée</div>
                  <div id="campagne-associee" className="font-semibold text-gray-800">{config.campagne_associee}</div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center"><span className="text-2xl mr-2">ℹ️</span> Informations pratiques</h3>
              <div className="space-y-3 text-gray-600">
                <div className="flex items-center gap-3"><span className="text-xl">🎫</span> Gratuit</div>
                <div className="flex items-center gap-3"><span className="text-xl">👕</span> Tenue décontractée</div>
                <div className="flex items-center gap-3"><span className="text-xl">🌤️</span> En extérieur</div>
                <div className="flex items-center gap-3"><span className="text-xl">♿</span> Accessible PMR</div>
              </div>
            </div>

            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Partagez l'événement</h3>
              <div className="flex gap-3">
                <button className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-xl transition-all">📘</button>
                <button className="flex-1 bg-sky-400 hover:bg-sky-500 text-white py-3 rounded-xl transition-all">🐦</button>
                <button className="flex-1 bg-pink-500 hover:bg-pink-600 text-white py-3 rounded-xl transition-all">📷</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
