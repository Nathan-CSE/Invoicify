import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/HomePage';
import HomePage from './pages/HomePage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';

function PageList() {
  return (
    <>
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/sign-in' element={<SignIn />} />
        <Route path='/sign-up' element={<SignUp />} />
      </Routes>
    </>
  );
}

export default PageList;
