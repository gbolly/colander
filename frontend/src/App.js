import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import GradientBackground from './components/GradientBG';
import ErrorPage from './components/ErrorPage';
import Home from './pages/home';
import CandidateList from './pages/candidates/CandidateList';
import Navbar from './components/Navbar';

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';


const App = () => {
  return (
    <GradientBackground>
      <div className="container">
        <Navbar />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} errorElement={<ErrorPage />} />
            <Route
              path="candidates"
              element={<CandidateList />}
              errorElement={<ErrorPage />}
            />
          </Routes>
        </BrowserRouter>
      </div>
    </GradientBackground>
  );
}

export default App;
