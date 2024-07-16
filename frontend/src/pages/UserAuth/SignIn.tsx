import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Link, useNavigate } from 'react-router-dom';
import ErrorModal from '../../components/ErrorModal';
import axios, { AxiosError } from 'axios';

export default function SignIn(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  const navigate = useNavigate();
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  if (props.token) {
    console.log('SIGNIN');
    navigate('/dashboard');
  }
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const email = data.get('email') as string;
    const password = data.get('password') as string;
    console.log(email);
    console.log(password);
    if (email.length === 0 || password.length === 0) {
      alert('Fill out all required fields');
    } else {
      try {
        const response = await axios.post('http://localhost:5000/auth/login', {
          email,
          password,
        });

        if (response.status === 200) {
          props.setToken(response.data.token);
          localStorage.setItem('token', response.data.token);

          // Temporary Solution before backend TOKEN auth is done
          // REMOVE WHEN FEATURE IS ADDED
          localStorage.setItem('email', email);
          navigate('/dashboard');
        } else {
          setOpenError(true);
          setError(response.data.message);
        }
      } catch (error) {
        const err = error as AxiosError<{ message: string }>;
        if (err.response) {
          setOpenError(true);
          setError(err.response.data.message);
        } else if (error instanceof Error) {
          setOpenError(true);
          setError(error.message);
        }
      }
    }
  };

  return (
    <>
      <Container component='main' maxWidth='xs'>
        <CssBaseline />
        <Box
          sx={{
            marginTop: 20,
            padding: 5,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            border: 'solid 0.5px',
            borderRadius: 4,
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component='h1' variant='h5'>
            Sign In
          </Typography>
          <Box
            component='form'
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              margin='normal'
              required
              fullWidth
              id='email'
              label='Email'
              name='email'
              autoComplete='email'
              autoFocus
            />
            <TextField
              margin='normal'
              required
              fullWidth
              name='password'
              label='Password'
              type='password'
              id='password'
              autoComplete='current-password'
            />

            <Typography
              variant='subtitle1'
              sx={{ color: 'info.main', textDecoration: 'none' }}
              component={Link}
              to='/reset-pw'
              gutterBottom
            >
              Forgot password?
            </Typography>
            <Button type='submit' fullWidth variant='contained' sx={{ mt: 3 }}>
              Sign In
            </Button>

            <Button
              type='submit'
              fullWidth
              variant='contained'
              component={Link}
              to='/sign-up'
              sx={{ mt: 3, mb: 2 }}
              color='secondary'
            >
              Register here
            </Button>
          </Box>
        </Box>
      </Container>
      <Box sx={{ position: 'fixed', bottom: 20, left: 10, width: '40%' }}>
        {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
      </Box>
    </>
  );
}
