import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Navbar from './components/Navbar';

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
      </Routes>
    </>
  );
}

export default PageList;
