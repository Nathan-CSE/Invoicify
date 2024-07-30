import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const useAuth = (token: string) => {
  const navigate = useNavigate();
  const location = useLocation();
  const unAuthRoutes = ['/', '/sign-in', '/sign-up', '/reset-pw']
  console.log('this is token: ', token);

  useEffect(() => {
    if (!token) {
      navigate('/sign-in');
    } else if (token && unAuthRoutes.includes(location.pathname)) {
      navigate('/dashboard');
    }
  }, [token, navigate]);
};

export default useAuth;
