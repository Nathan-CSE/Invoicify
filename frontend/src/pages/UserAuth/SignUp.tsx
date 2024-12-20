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
import ErrorModal from '../../components/ErrorModal';
import axios, { AxiosError } from 'axios';
import HowToRegIcon from '@mui/icons-material/HowToReg';
import LoginIcon from '@mui/icons-material/Login';
import LoadingDialog from '../../components/LoadingDialog';

function SignUp(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  const navigate = useNavigate();
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  if (props.token) {
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
      setOpenError(true);
      setError('Fill out all required fields');
    } else if (!email.includes('@')) {
      setOpenError(true);
      setError('Please provide a valid email address');
    } else if (password !== confirmPassword) {
      setOpenError(true);
      setError('Passwords do not match');
    } else if (password.length < 6) {
      setOpenError(true);
      setError('Passwords have a minimum length of 6');
    } else {
      if (password === confirmPassword) {
        try {
          setLoading(true);
          const response = await axios.post(
            'http://localhost:5000/auth/register',
            {
              email,
              password,
            }
          );

          setLoading(false);
          if (response.status === 201) {
            props.setToken(response.data.token);
            localStorage.setItem('token', response.data.token);

            localStorage.setItem('email', email);
            navigate('/dashboard');
          } else {
            setOpenError(true);
            setError(response.data.message);
          }
        } catch (error) {
          setLoading(false);
          const err = error as AxiosError<{ message: string }>;
          if (err.response) {
            setOpenError(true);
            setError(err.response.data.message);
          } else if (error instanceof Error) {
            setOpenError(true);
            setError(error.message);
          }
        }
      } else {
        setOpenError(true);
        setError('Passwords do not match');
      }
    }
  };

  return (
    <>
      <LoadingDialog open={loading} message='Signing up...' />
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
          <Typography component='h1' variant='h5' sx={{ mb: 4 }}>
            Sign up
          </Typography>
          <Box component='form' noValidate onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  data-cy='register-firstName'
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
                  data-cy='register-lastName'
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
                  data-cy='register-email'
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
                  data-cy='register-password'
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
                  data-cy='register-confirmPassword'
                  required
                  fullWidth
                  name='confirmPassword'
                  label='Confirm Password'
                  type='password'
                  id='confirmPassword'
                />
              </Grid>
            </Grid>
            <Button
              data-cy='register-signUp'
              type='submit'
              fullWidth
              variant='contained'
              sx={{ mt: 3 }}
              startIcon={<HowToRegIcon />}
            >
              Sign Up
            </Button>
            <Button
              type='submit'
              fullWidth
              variant='contained'
              component={Link}
              to='/sign-in'
              sx={{ mt: 3, mb: 2 }}
              startIcon={<LoginIcon />}
              color='secondary'
            >
              Back to Sign In
            </Button>
          </Box>
        </Box>
      </Container>
      {openError && (
        <ErrorModal open={openError} setOpen={setOpenError}>
          {error}
        </ErrorModal>
      )}
    </>
  );
}

export default SignUp;
