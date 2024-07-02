import React from 'react';
import { Link } from 'react-router-dom';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Button, Divider, TextField } from '@mui/material';
import ErrorModal from '../components/ErrorModal';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import axios, { AxiosError } from 'axios';

function SettingsPage(props: { token: string }) {
  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  const changeAccountDetails = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const email = localStorage.getItem('email');
    const password = data.get('oldPassword') as string;
    const updated_password = data.get('newPassword') as string;

    if (password.length === 0 || updated_password.length === 0) {
      alert('Password fields are empty');
    } else {
      try {
        console.log(password, updated_password);
        const response = await axios.patch(
          'http://localhost:5000/auth/change-pw',
          {
            email,
            password,
            updated_password,
          }
        );
        if (response.status === 200) {
          alert(response.data.message);
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
      <Box
        sx={{
          mt: 15,
          mx: 5,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          width: '90%',
        }}
      >
        <Typography variant='h4'>Account Settings</Typography>
        <Divider sx={{ borderColor: 'black', width: '100%' }} />
        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize='small' />}
          sx={{ mt: 1 }}
        >
          <Typography component={Link} to='/dashboard'>
            Dashboard
          </Typography>

          <Typography color='text.primary'>Account Settings</Typography>
        </Breadcrumbs>

        <Box sx={{ mt: 5, width: '100%' }}>
          <Typography variant='subtitle1' gutterBottom>
            Email
          </Typography>
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

          <Typography variant='subtitle1' gutterBottom sx={{ mt: 5 }}>
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
            <Button type='submit' fullWidth variant='contained' sx={{ mt: 3 }}>
              Save Changes
            </Button>
          </Box>
        </Box>
        <Box sx={{ mt: 10 }}>
          {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
        </Box>
      </Box>
    </>
  );
}

export default SettingsPage;