import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/HomePage';
import HomePage from './pages/HomePage';

function PageList() {
  return (
    <>
      <Routes>
        <Route path='/' element={<HomePage />} />
      </Routes>
    </>
  );
}

export default PageList;
