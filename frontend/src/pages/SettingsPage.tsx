import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import {
  Button,
  Container,
  CssBaseline,
  Stack,
  Divider,
  TextField,
} from '@mui/material';
import ErrorModal from '../components/ErrorModal';

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
        const response = await fetch('http://localhost:5000/auth/change-pw', {
          method: 'PATCH',
          body: JSON.stringify({
            email,
            password,
            updated_password,
          }),
          headers: {
            'Content-type': 'application/json',
          },
        });

        const data = await response.json();

        if (response.status === 400) {
          console.log('HERE');
          setOpenError(true);
          setError(data.message);
        } else {
          alert(data.message);
        }
      } catch (err) {
        if (err instanceof Error) {
          alert(err.message);
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
