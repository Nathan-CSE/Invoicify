import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Box, Stack, Typography } from '@mui/material';
import { ReactComponent as InvoiceSettings } from '../assets/settings_mini.svg';
import axios, { AxiosError } from 'axios';
import ErrorModal from './ErrorModal';
import { useLocation, useNavigate } from 'react-router-dom';
import CreateIcon from '@mui/icons-material/Create';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';
import LoadingDialog from './LoadingDialog';

export default function SettingsMenu(props: { token: string; details: any }) {
  // Error checking
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');
  const [loading, setLoading] = React.useState(false);

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
    navigate('/invoice-edit', {
      state: { details: props.details },
    });
  };

  const handleSend = () => {
    navigate('/invoice-sending', {
      state: { cardID: props.details.id },
    });
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      const response = await axios.delete(
        `http://localhost:5000/invoice/delete/${props.details.id}`,
        {
          headers: {
            Authorisation: `${props.token}`,
          },
        }
      );

      setLoading(false);

      if (response.status === 200) {
        alert('Delete confirmed');
        window.location.reload();
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
  };

  return (
    <div>
      <LoadingDialog open={loading} message='Deleting invoice...' />
      <Box
        sx={{
          position: 'absolute',
          zIndex: 1000,
          cursor: 'pointer',
          right: 0,
          top: 0,
          pr: 1.5,
          pt: 1.5,
        }}
      >
        <InvoiceSettings onClick={handleClick}></InvoiceSettings>
      </Box>
      <Menu
        id='basic-menu'
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
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
          {props.details.is_gui ? (
            <Box onClick={handleClose}>
              <Button
                onClick={handleEdit}
                startIcon={<CreateIcon />}
                variant='contained'
                sx={{ minWidth: '6rem', maxWidth: '6rem' }}
              >
                EDIT
              </Button>
            </Box>
          ) : (
            <></>
          )}
          {props.details.is_ready ? (
            <Box onClick={handleClose}>
              <Button
                onClick={handleSend}
                startIcon={<SendIcon />}
                variant='contained'
                sx={{ minWidth: '6rem', maxWidth: '6rem' }}
              >
                SEND
              </Button>
            </Box>
          ) : (
            <></>
          )}

          <Box onClick={handleClose}>
            <Button
              onClick={handleDelete}
              startIcon={<DeleteIcon sx={{ mr: -0.75 }} />}
              variant='contained'
              color='error'
              sx={{ minWidth: '6rem', maxWidth: '6rem' }}
            >
              DELETE
            </Button>
          </Box>
        </Stack>
      </Menu>
      {/* <Box sx={{ position: 'fixed', bottom: 20, left: 10, width: '40%' }}>
        {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
      </Box> */}
    </div>
  );
}
