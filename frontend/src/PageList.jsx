import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/HomePage';
import HomePage from './pages/HomePage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import InvoiceCreation from './pages/InvoiceCreation';
import InvoiceCreationConfirmation from './pages/InvoiceCreationConfirmation';

function PageList() {
  return (
    <>
      <Routes>
        {/* <Route path='/' element={<HomePage />} /> */}
        <Route path='/' element={<InvoiceCreation />} />
        <Route path='/invoice-creation' element={<InvoiceCreation />} />
        <Route path='/invoice-confirmation' element={<InvoiceCreationConfirmation />} />
        <Route path='/sign-in' element={<SignIn />} />
        <Route path='/sign-up' element={<SignUp />} />
      </Routes>
    </>
  );
}

export default PageList;
