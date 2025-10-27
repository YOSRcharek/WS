import "./App.css"; 
import Header from "./components/Header";
import HomePage from "./components/home-page";
import AddWastePage from "./components/add-waste-page";
import WasteListPage from "./components/waste-list-page";
import WasteTypesPage from "./components/waste-types-page";
import CentersPage from "./components/centers-page";
import UsersPage from "./components/users-page";
import EquipmentPage from "./components/equipment-page";
import AddEventPage from "./components/add-event-page";
import AddCampaignPage from "./components/add-campaign-page";
import EventsPage from "./components/events-page";
import DashboardPage from "./components/dashboard-page";
import React, { useContext } from 'react';
import { AppContext, AppProvider } from "./context/AppContext";

function Pages() {
  const { currentPage } = useContext(AppContext);

  switch (currentPage) {
    case "home": return <HomePage />;
    case "add-waste": return <AddWastePage />;
    case "waste-list": return <WasteListPage />;
    case "waste-types": return <WasteTypesPage />;
    case "centers": return <CentersPage />;
    case "users": return <UsersPage />;
    case "equipment": return <EquipmentPage />;
    case "add-event": return <AddEventPage />;
    case "add-campaign": return <AddCampaignPage />;
    case "events": return <EventsPage />;
    case "dashboard": return <DashboardPage />;
    default: return <HomePage />;
  }
}

function AppContent() {
  const { setCurrentPage } = useContext(AppContext);

  return (
    <div className="bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 min-h-screen">
      <Header setActivePage={setCurrentPage} />
      <Pages />
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}
