import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Navbar from '../components/Navbar';
import Divider from '@mui/material/Divider';
import { Link, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import FileUpload from '../components/FileUpload';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';


const theme = createTheme({
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

export default function SignIn() {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    navigate('/invoice-confirmation');
    setOpen(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const username = data.get('username');
    const password = data.get('password');
    
    if (username.length === 0 || password === 0) {
      alert('Fill out all required fields');
    } else {
      try {
        // send to backend
      } catch (err) {
        alert(err.response.data.error);
      }
    }

  };

  return (
    <>
      <ThemeProvider theme={theme}>

      <Navbar />
      
      <Container maxWidth="lg" sx={{ marginTop: 11 }}>
        <Typography variant='h4'>
          Invoice Creation
        </Typography>

        <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />

        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize="small" />}
        >
          <Typography
            component={Link}
            to='/sign-in'
          >
            Dashboard
          </Typography>

          <Typography color='text.primary'>
            Invoice Creation
          </Typography>
        </Breadcrumbs>

        <Box sx={{ my: 5 }}>
          <FileUpload />
        </Box>

        <Box textAlign='center'>
          <Button
            onClick={handleOpen}
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Generate Invoices
          </Button>
          {/* NOTE: Send to backend and create invoices */}
        </Box>

        <Dialog
          open={open}
          onClose={handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {"Your invoice has been created and saved to your account."}
          </DialogTitle>
          <DialogActions>
            <Button onClick={handleClose} autoFocus>
              Confirm
            </Button>
          </DialogActions>
        </Dialog>

        <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
          OR
        </Typography>

        <Box textAlign='center'>
          <Button
            component={Link}
            to='/invoice-creation-GUI'
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Create a New Invoice
          </Button>
        </Box>
      </Container>

      </ThemeProvider>
    </>
  );
}