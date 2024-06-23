import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Navbar from '../components/Navbar';
import Divider from '@mui/material/Divider';
import { Link, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Grid from '@mui/material/Grid';

const theme = createTheme({
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

export default function InvoiceCreationConfirmation() {
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

        <Box textAlign='center' sx={{ mt: 5 }}>
          <Typography variant='h4'>
            Your file has been created
          </Typography>
        </Box>

        <Box
          sx={{
            my: 10,
            padding: 5,
            height: '25vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            border: 'solid 0.5px',
            borderRadius: 4
          }}
        >
          <Box sx={{ mt: 1 }}>
            <Typography textAlign='center'>
              ANZ-Invoice.xml
            </Typography>
          </Box>

        </Box>

        <Grid container justifyContent="center" spacing={6}>
          <Grid item>
            <Button
              component={Link}
              to='/sign-in'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Download Invoice
            </Button>
          </Grid>

          <Grid item>
            <Button
              component={Link}
              to='/sign-in'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Preview Invoice
            </Button>
          </Grid>

          <Grid item>
            <Button
              component={Link}
              to='/invoice-creation'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Create another Invoice
            </Button>
          </Grid>
        </Grid>
      </Container>

      </ThemeProvider>
    </>
  );
}