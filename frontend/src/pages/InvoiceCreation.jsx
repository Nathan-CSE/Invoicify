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
import { Link } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import FileUpload from '../components/FileUpload';

const theme = createTheme({
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});


export default function SignIn() {
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

      <Typography variant='h4' sx={{ marginTop: 10 }}>
        Invoice Creation
      </Typography>

      <Divider sx={{ borderBottomWidth: 1.5 }} />

      <Breadcrumbs aria-label='breadcrumb'>
        <Link
          underline='hover'
          color='inherit'
          href='/material-ui/getting-started/installation/'
        >
          Dashboard
        </Link>
        <Typography color='text.primary'>
          Invoice Creation
        </Typography>
      </Breadcrumbs>

      <Box sx={{ mt: 5 }}>
        <FileUpload />
        <Typography textAlign='center' sx={{ mt: -15 }}>
          Supported formats: CSV, Excel, SQL, PDF
        </Typography>
      </Box>

      <Container component='main' maxWidth='xs'>
        <Box
          sx={{
            marginTop: 10,
            padding: 5,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            border: 'solid 0.5px',
            borderRadius: 4
          }}
        >
          <Box component='form' onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <Typography textAlign='center'>
              Upload Invoice
            </Typography>
            <Typography>
              Supported formats: CSV, Excel, SQL, PDF
            </Typography>
          </Box>
        </Box>

        <Typography textAlign='center' sx={{ my: 2 }}>
          OR
        </Typography>

        <Box textAlign='center'>
          <Button component={Link} to='/sign-in' variant='contained'>
            Create a New Invoice
          </Button>
        </Box>

      </Container>

      </ThemeProvider>
    </>
  );
}