import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import SignIn from './pages/UserAuth/SignIn';
import SignUp from './pages/UserAuth/SignUp';
import SettingsPage from './pages/UserAuth/SettingsPage';
import ResetPassword from './pages/UserAuth/ResetPasswordPage';
import InvoiceCreation from './pages/InvoiceCreation/InvoiceCreation';
import InvoiceCreationConfirmation from './pages/InvoiceCreation/InvoiceCreationConfirmation';
import CreationGUI from './pages/InvoiceCreation/CreationGUI';
import InvoiceSending from './pages/InvoiceSending/InvoiceSending';
import InvoiceSendingConfirmation from './pages/InvoiceSending/InvoiceSendingConfirmation';
import InvoiceManagement from './pages/InvoiceManagement/InvoiceManagementPage';
import HistoryPreviewInvoice from './pages/InvoiceManagement/HistoryPreviewInvoice';
import InvoiceEdit from './pages/InvoiceManagement/InvoiceEdit';
import InvoiceValidation from './pages/InvoiceValidation/InvoiceValidation';
import ValidationReport from './pages/InvoiceValidation/ValidationReport';
import DocPage from './pages/Documentation';

// Component that determines the routes of all the pages
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
              <CreationGUI token={token} editFlag={false} data={null} id={0} />
            </>
          }
        />
        <Route
          path='/invoice-creation-confirmation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceCreationConfirmation token={token} />
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
              <ValidationReport token={token} />
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
          path='/invoice-edit'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceEdit token={token} />
            </>
          }
        />
        <Route
          path='/invoice-preview-history'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <HistoryPreviewInvoice token={token} />
            </>
          }
        />
        <Route
          path='/invoice-sending'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceSending token={token} />
            </>
          }
        />
        <Route
          path='/invoice-sending-confirmation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvoiceSendingConfirmation token={token} />
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
        <Route
          path='/documentation'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <DocPage token={token} />
            </>
          }
        />
      </Routes>
    </>
  );
}

export default PageList;
