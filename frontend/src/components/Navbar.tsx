import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { Link, useNavigate } from 'react-router-dom';

function Navbar(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  const navigate = useNavigate();

  React.useEffect(() => {
    if (props.token) {
      console.log('HELLO?');
      navigate('/');
    }
  }, [props.token]);

  // Replace with API call later
  function logout() {
    localStorage.removeItem('token');
    props.setToken('');
    // Temporary Solution before backend TOKEN auth is done
    // REMOVE WHEN FEATURE IS ADDED
    localStorage.removeItem('email');
  }
  // Creates the Login OR logout button dynamically
  function buttonCreation() {
    if (props.token) {
      return (
        <Button
          component={Link}
          to='/'
          variant='contained'
          color='secondary'
          onClick={logout}
        >
          Logout
        </Button>
      );
    } else {
      return (
        <Button
          component={Link}
          to='/sign-in'
          variant='contained'
          color='secondary'
        >
          Login
        </Button>
      );
    }
  }

  return (
    <Box sx={{ flexGrow: 1, width: '100%', top: 0, position: 'fixed' }}>
      <AppBar>
        <Toolbar>
          <IconButton
            size='large'
            edge='start'
            color='inherit'
            aria-label='menu'
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant='h6' component='div' sx={{ flexGrow: 1 }}>
            E-Invoice Manager
          </Typography>
          {buttonCreation()}
          {/* <Button
            component={Link}
            to='/sign-in'
            variant='contained'
            color='secondary'
          >
            Login
          </Button> */}
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;
