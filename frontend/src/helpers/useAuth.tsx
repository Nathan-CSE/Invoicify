import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

// Helper function to check the user is authenticated to redirect them if necessary
const useAuth = (token: string) => {
  const navigate = useNavigate();
  const location = useLocation();

  const checktoken = localStorage.getItem('token');

  const unAuthRoutes = ['/', '/sign-in', '/sign-up', '/reset-pw'];

  useEffect(() => {
    if (!checktoken) {
      navigate('/sign-in');
    } else if (checktoken && unAuthRoutes.includes(location.pathname)) {
      navigate('/dashboard');
    }
  }, [token, navigate]);
};

export default useAuth;
