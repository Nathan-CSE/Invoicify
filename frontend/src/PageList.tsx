import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import InvoiceCreation from './pages/InvoiceCreation';
import InvoiceCreationConfirmation from './pages/InvoiceCreationConfirmation';
import CreationGUI from './pages/CreationGUI';

function PageList() {
  return (
    <>
      <Routes>
        {/* <Route path='/' element={<HomePage />} /> */}
        <Route path='/' element={<InvoiceCreation />} />
        <Route path='/invoice-creation' element={<InvoiceCreation />} />
        <Route path='/invoice-creation-GUI' element={<CreationGUI />} />
        <Route path='/invoice-confirmation' element={<InvoiceCreationConfirmation />} />
        <Route path='/sign-in' element={<SignIn />} />
        <Route path='/sign-up' element={<SignUp />} />
      </Routes>
    </>
  );
}

export default PageList;
