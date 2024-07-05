import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import SignIn from './pages/UserAuth/SignIn';
import SignUp from './pages/UserAuth/SignUp';
import SettingsPage from './pages/UserAuth/SettingsPage';
import InvoiceCreation from './pages/InvoiceCreation/InvoiceCreation';
import InvoiceCreationConfirmation from './pages/InvoiceCreation/InvoiceCreationConfirmation';
import CreationGUI from './pages/InvoiceCreation/CreationGUI';
import Navbar from './components/Navbar';
import PreviewInvoice from './pages/PreviewInvoice';
import InvoiceValidation from './pages/InvoiceValidation/InvoiceValidation';
import InvoiceValidationReport from './pages/InvoiceValidation/InvoiceValidationReport';
import ResetPassword from './pages/UserAuth/ResetPasswordPage';

function PageList() {
  const [token, setToken] = React.useState('');
  React.useEffect(() => {
    const checktoken = localStorage.getItem('token');
    if (checktoken) {
      setToken(checktoken);
    }
  }, []);

  return (
    <>
      <Routes>
        <Route
          path='/'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <HomePage token={token} />
            </>
          }
        />
        <Route
          path='/dashboard'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <DashboardPage token={token} setToken={setToken} />
            </>
          }
        />
        <Route
          path='/sign-in'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <SignIn token={token} setToken={setToken} />
            </>
          }
        />
        <Route
          path='/sign-up'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <SignUp token={token} setToken={setToken} />
            </>
          }
        />
        <Route
          path='/reset-pw'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <ResetPassword token={token} />
            </>
          }
        />
        <Route
          path='/invoice-creation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceCreation />
            </>
          }
        />
        <Route
          path='/invoice-creation-GUI'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <CreationGUI />
            </>
          }
        />
        <Route
          path='/invoice-confirmation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceCreationConfirmation />
            </>
          }
        />
        <Route
          path='/invoice-preview'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <PreviewInvoice />
            </>
          }
        />
        <Route 
          path='/invoice-validation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceValidation token={token} />
            </>
          } 
        />
        <Route 
          path='/invoice-validation-report'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceValidationReport />
            </>
          } 
        />
        <Route
          path='/settings'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <SettingsPage token={token} />
            </>
          }
        />
      </Routes>
    </>
  );
}

export default PageList;
