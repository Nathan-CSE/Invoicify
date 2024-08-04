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
import LoadingDialog from '../../components/LoadingDialog';
import { Dialog, DialogActions, DialogTitle } from '@mui/material';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import LoginIcon from '@mui/icons-material/Login';

function ResetPassword(props: { token: string }) {
  const navigate = useNavigate();

  // Error handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  // To differentiate between the stage of resetting
  // Stage 1: Only entering the email
  // Stage 2: Entering the token sent by the web app and the password
  const [resetState, setResetState] = React.useState(false);

  // Loading dialog handling
  const [loading, setLoading] = React.useState(false);
  const handleOpenLoadingDialog = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 3000);
  };

  // To prevent submitting multiple times in a row that causes a spam of requests
  const [submissionState, setSubmission] = React.useState(false);

  // Dialog Confirmation handling
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    navigate('/sign-in');
    setOpen(false);
  };

  if (props.token) {
    navigate('/dashboard');
  }
  React.useEffect(() => {
    setResetState(false);
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const email = data.get('email') as string;
    const reset_code = data.get('token') as string;
    const updated_password = data.get('newpassword') as string;

    // Checks if a form has been submitted
    // If so prevent further submits till completion
    if (submissionState) {
      return;
    }
    setSubmission(true);

    // First case:
    // - User has already submitted their email
    // - User is now inputting the reset token and their new password
    //
    // Second case:
    // - User is inputting their email
    if (resetState) {
      if (reset_code && updated_password) {
        if (reset_code.length === 0) {
          setOpenError(true);
          setError('Please enter a valid token');
        } else if (updated_password.length < 0) {
          setOpenError(true);
          setError('Passwords have a minimum length of 6');
        } else {
          try {
            const response = await axios.patch(
              'http://localhost:5000/auth/reset-pw',
              {
                email,
                reset_code,
                updated_password,
              }
            );

            if (response.status === 204) {
              handleOpen();
              setResetState(true);
              setOpenError(false);
              setError('');
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
          } finally {
            setSubmission(false);
          }
        }
      } else {
        setOpenError(true);
        setError('Please fill in all fields');
      }
    } else if (email) {
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
          setLoading(false);
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
    }
  };

  return (
    <>
      <Container component='main' maxWidth='xs'>
        <CssBaseline />
        <LoadingDialog open={loading} message='Checking Request...' />
        <Dialog
          open={open}
          onClose={handleClose}
          aria-labelledby='alert-dialog-title'
          aria-describedby='alert-dialog-description'
        >
          <DialogTitle id='alert-dialog-title'>
            {'Your password has been changed'}
          </DialogTitle>
          <DialogActions>
            <Button onClick={handleClose} autoFocus>
              Confirm
            </Button>
          </DialogActions>
        </Dialog>
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
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component='h1' variant='h5'>
            Reset Password
          </Typography>
          {resetState ? (
            <>
              <Typography variant='subtitle1' sx={{ mt: 3 }} gutterBottom>
                An email should be sent to you shortly. Please input the token
                given when received
              </Typography>
              <Box
                component='form'
                onSubmit={handleSubmit}
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
                  InputProps={{
                    readOnly: true,
                    style: { pointerEvents: 'none' },
                  }}
                />
                <TextField
                  margin='normal'
                  fullWidth
                  id='token'
                  label='Token'
                  name='token'
                  autoComplete='token'
                  autoFocus
                />
                <TextField
                  margin='normal'
                  fullWidth
                  id='newpassword'
                  label='New Password'
                  name='newpassword'
                  autoComplete='newpassword'
                  type='password'
                  autoFocus
                />
                <Button
                  type='submit'
                  fullWidth
                  variant='contained'
                  sx={{ mt: 3 }}
                  startIcon={<KeyboardArrowRightIcon />}
                >
                  Submit
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
            </>
          ) : (
            <>
              <Typography variant='subtitle1' sx={{ mt: 3 }} gutterBottom>
                Enter your email to begin
              </Typography>
              <Box
                component='form'
                onSubmit={handleSubmit}
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
                  startIcon={<KeyboardArrowRightIcon />}
                >
                  Submit
                </Button>
              </Box>
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
            </>
          )}
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

export default ResetPassword;
