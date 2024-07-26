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
import InvoiceSending from './pages/InvoiceSending/InvoiceSending';
import InvoiceSendingConfirmation from './pages/InvoiceSending/InvoiceSendingConfirmation';
import InvoiceManagement from './pages/InvoiceManagementPage';
import HistoryPreviewInvoice from './pages/HistoryPreviewInvoice';
import InvoiceValidation from './pages/InvoiceValidation/InvoiceValidation';
import InvalidReport from './pages/InvoiceValidation/InvalidReport';
import ValidReport from './pages/InvoiceValidation/ValidReport';
import ResetPassword from './pages/UserAuth/ResetPasswordPage';
import InvoiceEdit from './pages/InvoiceEdit';

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
          path='/invoice-preview'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <PreviewInvoice token={token} />
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
          path='/invoice-validation-report-valid'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <ValidReport />
            </>
          }
        />
        <Route
          path='/invoice-validation-report-invalid'
          element={
            <>
              <Navbar token={token} setToken={setToken} />
              <InvalidReport />
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
      </Routes>
    </>
  );
}

export default PageList;
