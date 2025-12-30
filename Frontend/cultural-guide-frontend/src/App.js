import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ChatWidget from "./components/ChatWidget";
import HomePage from "./pages/HomePage";
import QuizPage from "./pages/QuizPage";
import "./App.css";

function App() {
  // Global state for chat context to persist across pages
  const [globalChatContext, setGlobalChatContext] = useState(null);

  return (
    <Router>
      <div className="App">
        <Header />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage setGlobalCountry={setGlobalChatContext} />} />
            <Route path="/quiz/:countryName" element={<QuizPage />} />
            {/* Fallback route */}
            <Route path="*" element={<HomePage setGlobalCountry={setGlobalChatContext} />} />
          </Routes>
        </main>

        <ChatWidget globalContextCountry={globalChatContext} />
      </div>
    </Router>
  );
}

export default App;
