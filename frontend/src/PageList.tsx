import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import InvoiceCreation from './pages/InvoiceCreation';
import InvoiceCreationConfirmation from './pages/InvoiceCreationConfirmation';
import CreationGUI from './pages/CreationGUI';
import Navbar from './components/Navbar';
import SettingsPage from './pages/SettingsPage';
import PreviewInvoice from './pages/PreviewInvoice';
import ResetPassword from './pages/ResetPasswordPage';
import InvoiceManagement from './pages/InvoiceManagementPage';

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
              <InvoiceCreation token={token} />
            </>
          }
        />
        <Route
          path='/invoice-creation-GUI'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <CreationGUI token={token} />
            </>
          }
        />
        <Route
          path='/invoice-confirmation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceCreationConfirmation token={token} />
            </>
          }
        />
        <Route
          path='/invoice-preview'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <PreviewInvoice token={token} />
            </>
          }
        />
        <Route
          path='/invoice-management'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceManagement token={token} />
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
