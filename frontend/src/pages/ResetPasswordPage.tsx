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

import { ReactComponent as DocSvg } from '../assets/documentation.svg';
import { ReactComponent as BackSvg } from '../assets/backarrow.svg';
import { relative } from 'path';
import LoadingDialog from '../components/LoadingDialog';

export default function ResetPassword(props: { token: string }) {
  const navigate = useNavigate();
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');
  const [resetState, setResetState] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [submissionState, setSubmission] = React.useState(false);

  if (props.token) {
    console.log('SIGNIN');
    navigate('/dashboard');
  }
  React.useEffect(() => {
    setResetState(false);
  }, []);

  const handleOpenLoadingDialog = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 3000);
  };

  const handleSubmitEmail = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const email = data.get('email') as string;
    if (submissionState) {
      console.log('STOP');
      return;
    }
    setSubmission(true);
    if (email.length === 0) {
      setOpenError(true);
      setError('Please enter a valid email');
    } else {
      handleOpenLoadingDialog();
      try {
        const response = await axios.patch(
          'http://localhost:5000/auth/reset-code',
          {
            email,
          }
        );

        if (response.status === 200) {
          setResetState(true);
          setOpenError(false);
          setError('');
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
      } finally {
        setSubmission(false);
      }
    }
  };

  return (
    <>
      <Container component='main' maxWidth='xs'>
        <CssBaseline />
        <LoadingDialog open={loading} message='Checking Request...' />
        <Box
          sx={{
            marginTop: 20,
            padding: 5,
            position: 'relative',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            border: 'solid 0.5px',
            borderRadius: 4,
          }}
        >
          <Box
            component={Link}
            to='/sign-in'
            sx={{
              position: 'absolute',
              right: 10,
              top: 5,
              display: 'flex',
              flexDirection: 'row',
              color: 'primary.main',
              textDecoration: 'none',
            }}
          >
            <BackSvg></BackSvg>
            <Typography variant='subtitle2' gutterBottom>
              Back
            </Typography>
          </Box>
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component='h1' variant='h5'>
            Reset Password
          </Typography>
          {resetState ? (
            <></>
          ) : (
            <>
              <Typography variant='subtitle1' sx={{ mt: 3 }} gutterBottom>
                Enter your email to begin
              </Typography>
              <Box
                component='form'
                onSubmit={handleSubmitEmail}
                noValidate
                sx={{ mt: 1 }}
              >
                <TextField
                  margin='normal'
                  fullWidth
                  id='email'
                  label='Email'
                  name='email'
                  autoComplete='email'
                  autoFocus
                />
                <Button
                  type='submit'
                  fullWidth
                  variant='contained'
                  sx={{ mt: 3 }}
                >
                  Submit
                </Button>
              </Box>
            </>
          )}
        </Box>
      </Container>
      <Box sx={{ position: 'fixed', bottom: 20, left: 10, width: '40%' }}>
        {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
      </Box>
    </>
  );
}
