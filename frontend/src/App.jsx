import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Utensils, MessageSquare, Calendar, Info } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import Menu from './components/Menu';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-50 text-gray-900 font-sans">
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            <Link to="/" className="text-2xl font-bold text-orange-600 flex items-center gap-2">
              <Utensils className="h-6 w-6" />
              SmartDine AI
            </Link>
            <nav className="flex gap-6">
              <Link to="/menu" className="hover:text-orange-600 flex items-center gap-1 font-medium"><Utensils className="h-4 w-4"/> Menu</Link>
              <Link to="/chat" className="hover:text-orange-600 flex items-center gap-1 font-medium"><MessageSquare className="h-4 w-4"/> AI Assistant</Link>
            </nav>
          </div>
        </header>

        <main className="flex-1 max-w-6xl mx-auto w-full p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/menu" element={<Menu />} />
            <Route path="/chat" element={<ChatInterface />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="flex flex-col items-center justify-center text-center mt-20 gap-8">
      <h1 className="text-5xl font-extrabold text-gray-900">Good Food. <span className="text-orange-600">Smart Assistance.</span></h1>
      <p className="text-lg text-gray-600 max-w-2xl">
        Welcome to SmartDine Restaurant. Experience our delicious menu and try out our interactive AI Agent that can help you with recommendations, orders, and reservations.
      </p>
      <div className="flex gap-4">
        <Link to="/menu" className="bg-gray-900 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition">View Menu</Link>
        <Link to="/chat" className="bg-orange-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-orange-700 transition">Chat with AI</Link>
      </div>
    </div>
  );
}

export default App;
