import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/HomePage';
import HomePage from './pages/HomePage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import InvoiceCreation from './pages/InvoiceCreation';

function PageList() {
  return (
    <>
      <Routes>
        {/* <Route path='/' element={<HomePage />} /> */}
        {/* <Route path='/invoice-creation' element={<InvoiceCreation />} /> */}
        <Route path='/sign-in' element={<SignIn />} />
        <Route path='/sign-up' element={<SignUp />} />
        <Route path='/' element={<InvoiceCreation />} />
      </Routes>
    </>
  );
}

export default PageList;
