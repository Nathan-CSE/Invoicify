import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const useAuth = (token: string) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/sign-in');
    }
  }, [token, navigate]);
};

export default useAuth;
