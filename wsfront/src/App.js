import "./App.css";
import Header from "./components/Header";
import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
import AppRoutes from "./routes"; // <-- import des routes

export default function App() {
  return (
    <Router>
      <div className="bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50 min-h-screen">
        <Header />
        <AppRoutes />
      </div>
    </Router>
  );
}
