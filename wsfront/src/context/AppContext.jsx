import { createContext, useState } from "react";

export const AppContext = createContext();

export function AppProvider({ children }) {
  const [wastes, setWastes] = useState([]);
  const [events, setEvents] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
   const [dechets, setdechets] = useState([]);
  const [typededechet, settypededechet] = useState([]);
  const [currentPage, setCurrentPage] = useState("home");

  return (
    <AppContext.Provider value={{
      wastes, setWastes,dechets, setdechets,typededechet, settypededechet,
      events, setEvents,
      campaigns, setCampaigns,
      currentPage, setCurrentPage
    }}>
      {children}
    </AppContext.Provider>
  );
}
