// routes.jsx
import React from "react";
import { Routes, Route } from "react-router-dom";

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
import EventDetailPage from "./components/EventDetailPage";
import DashboardPage from "./components/dashboard-page";
import CampaignDetailPage from "./components/CompaignDetailPage";
import EventListPage from "./components/event-list";
import CampaignListPage from "./components/campaign-list";
import EditEventPage from "./components/edit-event-page";
import EditCampaignPage from "./components/edit-campaign-page";
import Editdechet from "./components/edit-waste";

import MetalType from "./components/typedechetmetal";
import ElectronicType from "./components/typedechetelectronic";
import ADDMetalType from "./components/add-metalwaste";
import ADDelectronicType from "./components/add-electronicwaste";
import Editelectronic from "./components/edit-electronicwaste";

import AIpage from "./components/aipage";









export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      
       <Route path="/aipage" element={<AIpage />} />
      <Route path="/add-waste" element={<AddWastePage />} />
      <Route path="/edit-waste/:id" element={<Editdechet />} />
      <Route path="/waste-list" element={<WasteListPage />} />
      <Route path="/add-metalwaste" element={<ADDMetalType />} />
      <Route path="/add-electronicwaste" element={<ADDelectronicType />} />
      <Route path="/waste-types" element={<WasteTypesPage />} />
      <Route path="/waste-metal" element={<MetalType />} />
      <Route path="/waste-electronic" element={<ElectronicType />} />
      <Route path="/edit-electronictype/:id" element={<Editelectronic />} />

      
      <Route path="/centers" element={<CentersPage />} />
      <Route path="/users" element={<UsersPage />} />
      <Route path="/equipment" element={<EquipmentPage />} />
      <Route path="/add-event" element={<AddEventPage />} />
      <Route path="/edit-event/:id" element={<EditEventPage />} />
      <Route path="/add-campaign" element={<AddCampaignPage />} />
      <Route path="/edit-campaign/:id" element={<EditCampaignPage />} />
      <Route path="/events" element={<EventsPage />} />
      <Route path="/event/:id" element={<EventDetailPage />} />
      <Route path="/event-list" element={<EventListPage />} />
      <Route path="/campaign-list" element={<CampaignListPage />} />
      <Route path="/campaign/:id" element={<CampaignDetailPage/>} />
      <Route path="/dashboard" element={<DashboardPage />} />
    </Routes>
  );
}
