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
      <Navbar />
      <Typography component="h1" variant="header3" sx={{ marginTop: 10 }}>
        Invoice Creation
      </Typography>
      <Divider sx={{ borderBottomWidth: 2 }} />
      <Breadcrumbs aria-label="breadcrumb">
        <Link
          underline="hover"
          color="inherit"
          href="/material-ui/getting-started/installation/"
        >
          Dashboard
        </Link>
        <Typography color="text.primary">
          Invoice Creation
        </Typography>
      </Breadcrumbs>
      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 20,
            padding: 5,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            border: 'solid 0.5px',
            borderRadius: 4
          }}
        >
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            Upload Invoice
          </Box>
        </Box>
      </Container>
    </>
  );
}