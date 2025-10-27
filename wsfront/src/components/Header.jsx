import React, { useState } from "react";

export default function Header({ setActivePage }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const pages = [
    { id: "home", label: "Accueil" },
    { id: "waste-types", label: "Types de Déchets" },
    { id: "centers", label: "Centres & Points" },
    { id: "users", label: "Citoyens & Municipalités" },
    { id: "equipment", label: "Équipements" },
    { id: "events", label: "Événements" },
    { id: "dashboard", label: "Dashboard" },
    { id: "add-event", label: "Créer Événement" },
    { id: "add-campaign", label: "Créer Campagne" },
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

          <div className="hidden md:flex space-x-8">
            {pages.slice(0, 7).map((page) => (
              <button
                key={page.id}
                onClick={() => setActivePage(page.id)}
                className="nav-link text-gray-700 hover:text-emerald-600 font-medium"
              >
                {page.label}
              </button>
            ))}
          </div>

          <button onClick={toggleMenu} className="md:hidden text-gray-700">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>

      {mobileOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-4 py-3 space-y-2">
            {pages.map((page) => (
              <button
                key={page.id}
                onClick={() => {
                  setActivePage(page.id);
                  setMobileOpen(false);
                }}
                className="block py-2 text-gray-700 hover:text-emerald-600 w-full text-left"
              >
                {page.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}
