import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Link, useNavigate } from 'react-router-dom';
import { WindowSharp } from '@mui/icons-material';
import ErrorModal from '../components/ErrorModal';

export default function SignUp(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  const navigate = useNavigate();
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');
  if (props.token) {
    console.log('SIGNUP');
    navigate('/dashboard');
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const firstName = data.get('firstName') as string;
    const lastName = data.get('lastName') as string;
    const email = data.get('email') as string;
    const password = data.get('password') as string;
    const confirmPassword = data.get('confirmPassword') as string;

    if (
      firstName.length === 0 ||
      lastName.length === 0 ||
      email.length === 0 ||
      password.length === 0 ||
      confirmPassword.length === 0
    ) {
      alert('Fill out all required fields');
    } else {
      if (password === confirmPassword) {
        try {
          const response = await fetch('http://localhost:5000/auth/register', {
            method: 'POST',
            body: JSON.stringify({
              email,
              password,
            }),
            headers: {
              'Content-type': 'application/json',
            },
          });

          const data = await response.json();
          console.log(data);

          if (response.status === 400) {
            console.log('HERE');
            setOpenError(true);
            setError(data.message);
          } else {
            props.setToken(data.token);
            localStorage.setItem('token', data.token);

            // Temporary Solution before backend TOKEN auth is done
            // REMOVE WHEN FEATURE IS ADDED
            localStorage.setItem('email', email);
            navigate('/dashboard');
          }
        } catch (err) {
          // alert(err.response.data.error);
          if (err instanceof Error) {
            alert(err.message);
          }
        }
      } else {
        alert('Passwords do not match');
      }
    }
  };

  return (
    <>
      {/* <Navbar /> */}
      <Container component='main' maxWidth='xs'>
        <CssBaseline />
        <Box
          sx={{
            marginTop: 13,
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
            Sign up
          </Typography>
          <Box component='form' noValidate onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete='given-name'
                  name='firstName'
                  required
                  fullWidth
                  id='firstName'
                  label='First Name'
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id='lastName'
                  label='Last Name'
                  name='lastName'
                  autoComplete='family-name'
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name='email'
                  label='Email'
                  type='email'
                  id='email'
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name='password'
                  label='Password'
                  type='password'
                  id='password'
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name='confirmPassword'
                  label='Confirm Password'
                  type='password'
                  id='confirmPassword'
                />
              </Grid>
            </Grid>
            <Button type='submit' fullWidth variant='contained' sx={{ mt: 3 }}>
              Sign Up
            </Button>
            <Button
              type='submit'
              fullWidth
              variant='contained'
              component={Link}
              to='/sign-in'
              sx={{ mt: 3, mb: 2 }}
              color='secondary'
            >
              Back to Sign In
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
