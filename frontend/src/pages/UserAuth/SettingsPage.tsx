import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Button, Container, TextField, Snackbar, Alert } from '@mui/material';
import ErrorModal from '../../components/ErrorModal';
import SaveIcon from '@mui/icons-material/Save';
import axios, { AxiosError } from 'axios';
import LoadingDialog from '../../components/LoadingDialog';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';

function SettingsPage(props: { token: string }) {
  useAuth(props.token);
  const [loading, setLoading] = React.useState(false);

  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  const breadcrumbNav = {
    Dashboard: '/dashboard',
    'Account Settings': '/settings',
  };

  const [snackbarOpen, setSnackbarOpen] = React.useState(false);
  const [snackbarMessage, setSnackbarMessage] = React.useState('');

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const changeAccountDetails = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const email = localStorage.getItem('email');
    const password = data.get('oldPassword') as string;
    const updated_password = data.get('newPassword') as string;

    if (password.length === 0 || updated_password.length === 0) {
      setOpenError(true);
      setError('Password fields are empty');
      return;
    } else if (updated_password.length < 6) {
      setOpenError(true);
      setError('Passwords have a minimum length of 6');
    } else {
      try {
        setLoading(true);
        const response = await axios.patch(
          'http://localhost:5000/auth/change-pw',
          {
            email,
            password,
            updated_password,
          }
        );

        setLoading(false);

        if (response.status === 200) {
          setSnackbarMessage(response.data.message);
          setSnackbarOpen(true);
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
    }
  };
  return (
    <>
      <LoadingDialog open={loading} message='Changing password...' />
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <PageHeader
          HeaderTitle={'Account Settings'}
          BreadcrumbDict={breadcrumbNav}
        />

        <Box sx={{ mt: 4, width: '100%', mb: -2 }}>
          <Typography variant='h5'>Email</Typography>
          <TextField
            margin='normal'
            fullWidth
            id='outlined-read-only-input'
            defaultValue={localStorage.getItem('email')}
            InputProps={{
              readOnly: true,
              style: { pointerEvents: 'none' },
            }}
          />

          <Typography variant='h5' sx={{ mt: 3 }}>
            Change Password
          </Typography>
          <Box component='form' onSubmit={changeAccountDetails} noValidate>
            <Box sx={{ display: 'flex', flexDirection: 'row', gap: 3 }}>
              <TextField
                margin='normal'
                fullWidth
                name='oldPassword'
                label='Old Password'
                type='password'
                id='oldPassword'
                autoComplete='old-password'
              />
              <TextField
                margin='normal'
                fullWidth
                name='newPassword'
                label='New Password'
                type='password'
                id='newPassword'
                autoComplete='new-password'
              />
            </Box>
            <Box display='flex' justifyContent='center'>
              <Button
                type='submit'
                variant='contained'
                sx={{ mt: 3, height: '50px', padding: '25px' }}
                startIcon={<SaveIcon />}
              >
                Save Changes
              </Button>
            </Box>
          </Box>
        </Box>
      </Container>
      {openError && (
        <ErrorModal open={openError} setOpen={setOpenError}>
          {error}
        </ErrorModal>
      )}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
      >
        <Alert
          variant='filled'
          onClose={handleSnackbarClose}
          severity='success'
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
}

export default SettingsPage;
