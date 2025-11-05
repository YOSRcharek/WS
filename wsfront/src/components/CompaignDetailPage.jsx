import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
<<<<<<< HEAD
import { getCampagneById , getEvenementsByCampagne } from "../services/campagneService";
import {useNavigate } from "react-router-dom";
=======
import { getCampagneById } from "../services/campagneService";
>>>>>>> doua

const defaultConfig = {
  title: "Campagne Océans Propres",
  start_date: "1er Mars 2024",
  end_date: "31 Mai 2024",
  nom_plateforme: "EcoAction",
  description_campa:
    "Une initiative mondiale pour sensibiliser à la pollution marine et encourager des actions concrètes pour protéger nos océans.",
  contenu:
    "Notre campagne comprend des ateliers éducatifs, des nettoyages de plages organisés, des conférences et des défis communautaires.",
  target_audience: "Jeunes adultes, étudiants, familles",
  lien: "https://example.com/campagne-oceans",
  primary_color: "#10b981",
  background_color: "#f0fdf4",
  text_color: "#1f2937",
  button_color: "#059669",
  accent_color: "#34d399",
};

export default function CampaignDetailPage() {
  const { id } = useParams(); // Récupère l’ID depuis /campaign/:id
  const [campaign, setCampaign] = useState(null);
<<<<<<< HEAD
  const [events, setEvents] = useState(null);
  const navigate = useNavigate(); // Hook pour naviguer

 useEffect(() => {
  const fetchCampagne = async () => {
    try {

      const data = await getCampagneById(id);
      console.log(data)
      if (data) {
        setCampaign({
          id: data.id,
          title: data.title || defaultConfig.title,
          start_date: data.startDate || defaultConfig.start_date,
          end_date: data.endDate || defaultConfig.end_date,
          nom_plateforme: data.nom_plateforme || defaultConfig.nom_plateforme,
          description_campa: data.descriptioncampa || defaultConfig.description_campa,
          contenu: data.contenu || defaultConfig.contenu,
          target_audience: data.targetAudience || defaultConfig.target_audience,
          lien: data.lien || defaultConfig.lien,
          primary_color: data.primary_color || defaultConfig.primary_color,
          background_color: data.background_color || defaultConfig.background_color,
          text_color: data.text_color || defaultConfig.text_color,
          button_color: data.button_color || defaultConfig.button_color,
          accent_color: data.accent_color || defaultConfig.accent_color,
          evenements: data.evenements || [], // S'assurer que les événements sont bien présents
        });
      } else {
        setCampaign(defaultConfig);
      }
    } catch (err) {
      console.error("Erreur lors du chargement de la campagne:", err);
      setCampaign(defaultConfig);
    }
  };

  fetchCampagne();
}, [id]);

 useEffect(() => {
    const fetchEvents = async () => {
      try {
        const data = await getEvenementsByCampagne(id);
        setEvents(data); // Mettre à jour les événements
      } catch (err) {
        console.error("Erreur lors du chargement des événements:", err);
      }
    };

    if (id) {
      fetchEvents();
    }
=======

  useEffect(() => {
    const fetchCampagne = async () => {
      try {
        const data = await getCampagneById(id);
        if (data) {
          setCampaign({
            title: data.title || defaultConfig.title,
            start_date: data.startDate || defaultConfig.start_date,
            end_date: data.endDate || defaultConfig.end_date,
            nom_plateforme: data.nom_plateforme || defaultConfig.nom_plateforme,
            description_campa: data.descriptioncampa || defaultConfig.description_campa,
            contenu: data.contenu || defaultConfig.contenu,
            target_audience: data.targetAudience || defaultConfig.target_audience,
            lien: data.lien || defaultConfig.lien,
            primary_color: data.primary_color || defaultConfig.primary_color,
            background_color: data.background_color || defaultConfig.background_color,
            text_color: data.text_color || defaultConfig.text_color,
            button_color: data.button_color || defaultConfig.button_color,
            accent_color: data.accent_color || defaultConfig.accent_color,
          });
        } else {
          setCampaign(defaultConfig);
        }
      } catch (err) {
        console.error("Erreur lors du chargement de la campagne:", err);
        setCampaign(defaultConfig);
      }
    };

    fetchCampagne();
>>>>>>> doua
  }, [id]);

  if (!campaign) {
    return <div className="text-center py-10 text-gray-600">Chargement de la campagne...</div>;
  }
<<<<<<< HEAD
   console.log( campaign.id)

=======
>>>>>>> doua

  return (
    <main>
      {/* Header */}
      <header
        className="relative h-96 overflow-hidden"
        style={{
          background: `linear-gradient(135deg, ${campaign.button_color} 0%, ${campaign.primary_color} 50%, ${campaign.accent_color} 100%)`,
        }}
      >
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative h-full flex items-center justify-center text-center px-6">
          <div className="fade-in">
            <div className="text-7xl mb-4">📢</div>
            <h1 className="text-5xl font-bold text-white mb-4">{campaign.title}</h1>
            <div className="flex items-center justify-center gap-6 text-white text-lg flex-wrap">
              <div className="flex items-center gap-2">
                <span className="text-2xl">📅</span>
                <span>{campaign.start_date}</span> - <span>{campaign.end_date}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-2xl">🌐</span>
                <span>{campaign.nom_plateforme}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Stats + contenu */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 -mt-20 relative z-10">
          <StatCard icon="🎯" title={campaign.target_audience} subtitle="Public cible" primaryColor={campaign.primary_color} />
          <StatCard icon="📊" title="Active" subtitle="Statut" primaryColor={campaign.primary_color} />
          <StatCard icon="🔗" title="Disponible" subtitle="Lien externe" primaryColor={campaign.primary_color} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Description */}
          <div className="lg:col-span-2 space-y-8">
            <Section title="Description de la campagne" icon="📝">
              <p>{campaign.description_campa}</p>
              <div className="bg-emerald-50 border-l-4 border-emerald-500 p-4 rounded">
                <p className="text-emerald-800">
                  <strong>🎯 Public ciblé :</strong> {campaign.target_audience}
                </p>
              </div>
            </Section>

            <Section title="Contenu de la campagne" icon="📋">
              <div className="content-image">🖼️</div>
              <p>{campaign.contenu}</p>
            </Section>

            <Section title="Objectifs et actions" icon="🎯">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <GoalCard icon="🌊" title="Sensibilisation" desc="Éduquer sur l'impact de la pollution" bg="emerald" />
                <GoalCard icon="♻️" title="Action directe" desc="Organiser des nettoyages communautaires" bg="green" />
                <GoalCard icon="📚" title="Éducation" desc="Fournir des ressources pédagogiques" bg="purple" />
                <GoalCard icon="🤝" title="Communauté" desc="Créer un réseau d'ambassadeurs" bg="orange" />
              </div>
            </Section>
<<<<<<< HEAD

              <Section title="Événements de la campagne" icon="📝">
              <div>
                {events && events.length > 0 ? (
                  events.map((event, idx) => (
                    <div key={idx} className="bg-emerald-50 border-l-4 border-emerald-500 p-4 rounded mb-5">
                      <p
                        className="text-emerald-800"
                        onClick={() => navigate(`/event/${event.evenementID}`)} // Naviguer vers la page de détail de l'événement
                      >
                        <strong>📅 {event.nomevent}</strong>
                        <br />
                        <span>{event.dateDebut} - {event.dateFin}</span>
                      </p>
                    </div>
                  ))
                ) : (
                  <p>Aucun événement trouvé pour cette campagne.</p>
                )}
              </div>
            </Section>

=======
>>>>>>> doua
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
<<<<<<< HEAD
            <div className="bg-white rounded-2xl shadow-lg p-6 fade-in">
              <div className="badge bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-semibold inline-block mb-4">
                Campagne active
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">Rejoignez-nous !</h3>
              <p className="text-gray-600 mb-6">
                Participez à cette campagne et faites la différence.
              </p>
             <button
              onClick={() => navigate("/add-event", { state: { campaign } })} 
              rel="noopener noreferrer"
              className="w-full block text-white font-bold py-4 px-6 rounded-xl text-lg mb-4 text-center"
              style={{
                background: `linear-gradient(135deg, ${campaign.button_color} 0%, ${campaign.primary_color} 100%)`,
              }}
            >
              Ajouter un événement
            </button>

            </div>
           
=======
            <CTAButton link={campaign.lien} primaryColor={campaign.primary_color} buttonColor={campaign.button_color} />
>>>>>>> doua
            <PlatformCard plateforme={campaign.nom_plateforme} />
            <TimelineCard start={campaign.start_date} end={campaign.end_date} />
            <ShareCard />
          </div>
        </div>
      </div>
    </main>
  );
}

// --- Components (inchangés) ---
const StatCard = ({ icon, title, subtitle, primaryColor }) => (
  <div className="stat-card card-hover rounded-2xl p-6 text-center shadow-xl">
    <div className="info-icon mx-auto mb-3">{icon}</div>
    <div className="text-2xl font-bold mb-1" style={{ color: primaryColor }}>
      {title}
    </div>
    <div className="text-gray-600">{subtitle}</div>
  </div>
);

const Section = ({ title, icon, children }) => (
  <section className="bg-white rounded-2xl shadow-lg p-8 fade-in">
    <h2 className="text-3xl font-bold text-gray-800 mb-4 flex items-center">
      <span className="text-4xl mr-3">{icon}</span> {title}
    </h2>
    {children}
  </section>
);

const GoalCard = ({ icon, title, desc, bg }) => (
  <div className={`bg-${bg}-50 p-4 rounded-xl`}>
    <div className="text-2xl mb-2">{icon}</div>
    <h3 className={`font-bold text-${bg}-700 mb-2`}>{title}</h3>
    <p className="text-gray-600 text-sm">{desc}</p>
  </div>
);

<<<<<<< HEAD
const CTAButton = ({ link, primaryColor, buttonColor, campaign, onClick }) => (
=======
const CTAButton = ({ link, primaryColor, buttonColor }) => (
>>>>>>> doua
  <div className="bg-white rounded-2xl shadow-lg p-6 fade-in">
    <div className="badge bg-emerald-100 text-emerald-700 px-4 py-2 rounded-full text-sm font-semibold inline-block mb-4">
      Campagne active
    </div>
    <h3 className="text-2xl font-bold text-gray-800 mb-4">Rejoignez-nous !</h3>
    <p className="text-gray-600 mb-6">
      Participez à cette campagne et faites la différence.
    </p>
    <a
<<<<<<< HEAD
      href="#"
      onClick={onClick} // Ajout de onClick ici
    
=======
      href={link}
      target="_blank"
>>>>>>> doua
      rel="noopener noreferrer"
      className="w-full block text-white font-bold py-4 px-6 rounded-xl text-lg mb-4 text-center"
      style={{
        background: `linear-gradient(135deg, ${buttonColor} 0%, ${primaryColor} 100%)`,
      }}
    >
<<<<<<< HEAD
      Ajouter un événement
=======
      Participer maintenant
>>>>>>> doua
    </a>
  </div>
);

<<<<<<< HEAD

=======
>>>>>>> doua
const PlatformCard = ({ plateforme }) => (
  <div className="bg-white rounded-2xl shadow-lg p-6">
    <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
      <span className="text-2xl mr-2">🌐</span> Plateforme
    </h3>
    <div className="bg-gray-50 p-4 rounded-xl">
      <div className="text-sm text-gray-500 mb-1">Hébergée sur</div>
      <div className="font-semibold text-gray-800 text-lg">{plateforme}</div>
    </div>
  </div>
);

const TimelineCard = ({ start, end }) => (
  <div className="bg-white rounded-2xl shadow-lg p-6">
    <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
      <span className="text-2xl mr-2">📅</span> Calendrier
    </h3>
    <div className="space-y-3">
      <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
        <span className="text-xl">🚀</span>
        <div>
          <div className="text-sm text-gray-500">Début</div>
          <div className="font-semibold text-green-700">{start}</div>
        </div>
      </div>
      <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
        <span className="text-xl">🏁</span>
        <div>
          <div className="text-sm text-gray-500">Fin</div>
          <div className="font-semibold text-red-700">{end}</div>
        </div>
      </div>
    </div>
  </div>
);

const ShareCard = () => (
  <div className="bg-white rounded-2xl shadow-lg p-6">
    <h3 className="text-xl font-bold text-gray-800 mb-4">Partagez la campagne</h3>
    <div className="flex gap-3">
      <button className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-xl transition-all">📘</button>
      <button className="flex-1 bg-sky-400 hover:bg-sky-500 text-white py-3 rounded-xl transition-all">🐦</button>
      <button className="flex-1 bg-pink-500 hover:bg-pink-600 text-white py-3 rounded-xl transition-all">📷</button>
      <button className="flex-1 bg-green-500 hover:bg-green-600 text-white py-3 rounded-xl transition-all">💬</button>
    </div>
  </div>
);
