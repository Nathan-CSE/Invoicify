import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Box, Stack, Typography } from '@mui/material';
import { ReactComponent as InvoiceSettings } from '../assets/settings_mini.svg';
import axios, { AxiosError } from 'axios';
import ErrorModal from './ErrorModal';
import { useLocation, useNavigate } from 'react-router-dom';

export default function SettingsMenu(props: { id: number; token: string }) {
  // Error checking
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  // Open state for the menu
  const [anchorEl, setAnchorEl] = React.useState<null | SVGElement>(null);
  const open = Boolean(anchorEl);

  // Handle the mouse events of the menu
  const handleClick = (event: React.MouseEvent<SVGElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const navigate = useNavigate();

  // Three functions to handle the settings option
  const handleEdit = () => {
    console.log('1');
  };

  const handleSend = () => {
    console.log(props.id);
    navigate('/invoice-sending', {
      state: { cardID: props.id },
    });
  };

  const handleDelete = async () => {
    try {
      const response = await axios.delete(
        `http://localhost:5000/invoice/delete/${props.id}`,
        {
          headers: {
            Authorisation: `${props.token}`,
          },
        }
      );

      if (response.status === 200) {
        alert('Delete confirmed');
        window.location.reload();
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
  };

  return (
    <div>
      <Box
        sx={{
          position: 'absolute',
          zIndex: 1000,
          cursor: 'pointer',
          pl: 1,
          pt: 1,
        }}
      >
        <InvoiceSettings onClick={handleClick}></InvoiceSettings>
      </Box>
      <Menu
        id='basic-menu'
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
        sx={{
          textAlign: 'center',
        }}
      >
        <Typography variant='h6' component='div' sx={{ width: '9rem' }}>
          Settings
        </Typography>
        <Stack spacing={2} sx={{ mt: 1 }}>
          <Box onClick={handleClose}>
            <Button
              onClick={handleEdit}
              variant='contained'
              sx={{ minWidth: '6rem' }}
            >
              EDIT
            </Button>
          </Box>
          <Box onClick={handleClose}>
            <Button
              onClick={handleSend}
              variant='contained'
              sx={{ minWidth: '6rem' }}
            >
              SEND
            </Button>
          </Box>
          <Box onClick={handleClose}>
            <Button
              onClick={handleDelete}
              variant='contained'
              color='error'
              sx={{ minWidth: '6rem' }}
            >
              DELETE
            </Button>
          </Box>
        </Stack>
      </Menu>
      <Box sx={{ position: 'fixed', bottom: 20, left: 10, width: '40%' }}>
        {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
      </Box>
    </div>
  );
}
