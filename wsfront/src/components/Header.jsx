import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation(); // ✅ pour détecter la route active

  const pages = [
    { id: "home", label: "Accueil", path: "/" },
    { id: "waste-types", label: "Types de Déchets", path: "/waste-types" },
    { id: "centers", label: "Centres & Points", path: "/centers" },
    { id: "users", label: "Citoyens & Municipalités", path: "/users" },
    { id: "equipment", label: "Équipements", path: "/equipment" },
    { id: "events", label: "Événements", path: "/events" },
    { id: "dashboard", label: "Dashboard", path: "/dashboard" },
    { id: "ai-matching", label: "IA Matching", path: "/ai-matching" },
    { id: "citizen-requests", label: "Demandes Citoyennes", path: "/citizen-requests" },
    { id: "add-event", label: "Créer Événement", path: "/add-event" },
    { id: "add-campaign", label: "Créer Campagne", path: "/add-campaign" },
  ];

  const toggleMenu = () => setMobileOpen(!mobileOpen);

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 gradient-green rounded-full flex items-center justify-center text-white text-2xl font-bold">
              W
            </div>
            <span className="text-2xl font-bold text-emerald-700">WasteWise</span>
          </div>

          {/* Liens desktop */}
          <div className="hidden md:flex space-x-8">
            {pages.slice(0, 7).map((page) => {
              const isActive = location.pathname === page.path;
              return (
                <button
                  key={page.id}
                  onClick={() => navigate(page.path)}
                  className={`nav-link font-medium ${
                    isActive
                      ? "text-emerald-600 active-link"
                      : "text-gray-700 hover:text-emerald-600"
                  }`}
                >
                  {page.label}
                </button>
              );
            })}
          </div>

          {/* Bouton mobile */}
          <button onClick={toggleMenu} className="md:hidden text-gray-700">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      {/* Menu mobile */}
      {mobileOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-4 py-3 space-y-2">
            {pages.map((page) => {
              const isActive = location.pathname === page.path;
              return (
                <button
                  key={page.id}
                  onClick={() => {
                    navigate(page.path);
                    setMobileOpen(false);
                  }}
                  className={`block py-2 w-full text-left ${
                    isActive
                      ? "text-emerald-600 font-semibold active-link"
                      : "text-gray-700 hover:text-emerald-600"
                  }`}
                >
                  {page.label}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
}
