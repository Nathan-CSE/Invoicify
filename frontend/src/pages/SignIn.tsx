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
import ErrorModal from '../components/ErrorModal';
import axios, { AxiosError } from 'axios';

export default function SignIn(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  const navigate = useNavigate();
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');
  // React.useEffect(() => {
  //   if (props.token) {
  //     navigate('/dashboard');
  //   }
  // }, [props.token]);
  if (props.token) {
    console.log('SIGNIN');
    navigate('/dashboard');
  }
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const email = data.get('email') as string;
    const password = data.get('password') as string;

    if (email.length === 0 || password.length === 0) {
      alert('Fill out all required fields');
    } else {
      try {
        const response = await axios.post('http://localhost:5000/auth/login', {
          email,
          password,
        });
        // const response = await fetch('http://localhost:5000/auth/login', {
        //   method: 'POST',
        //   body: JSON.stringify({
        //     email,
        //     password,
        //   }),
        //   headers: {
        //     'Content-type': 'application/json',
        //   },
        // });

        // const data = await response.json();
        // console.log(data);
        if (response.status === 200) {
          props.setToken(response.data.token);
          localStorage.setItem('token', response.data.token);

          // Temporary Solution before backend TOKEN auth is done
          // REMOVE WHEN FEATURE IS ADDED
          localStorage.setItem('email', email);
          navigate('/dashboard');
        }

        // if (response.status === 400) {
        //   console.log('HERE');
        //   setOpenError(true);
        //   setError(data.message);
        // } else {
        //   props.setToken(data.token);
        //   localStorage.setItem('token', data.token);

        //   // Temporary Solution before backend TOKEN auth is done
        //   // REMOVE WHEN FEATURE IS ADDED
        //   localStorage.setItem('email', email);
        //   navigate('/dashboard');
        // }
      } catch (error) {
        const err = error as AxiosError<{ message: string }>;
        if (err.response) {
          setOpenError(true);
          setError(err.response.data.message);
        } else {
          alert(err.message);
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
