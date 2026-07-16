import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SessionsList from './pages/SessionsList';
import SeatSelection from './pages/SeatSelection';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>🎬 Cinema Booking</h1>
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<SessionsList />} />
            <Route path="/sessions/:sessionId/seats" element={<SeatSelection />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;