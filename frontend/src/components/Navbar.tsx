import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import HomeIcon from '@mui/icons-material/Home';

import { Link, useLocation } from 'react-router-dom';
import TemporaryDrawer from './Drawer';

function Navbar(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  const location = useLocation();
  const currentPath = location.pathname;

  const logout = () => {
    localStorage.removeItem('token');
    props.setToken('');
    localStorage.removeItem('email');
  };

  // Creates the Login OR logout button dynamically
  const buttonCreation = () => {
    if (props.token) {
      return (
        <Button
          data-cy='logout'
          component={Link}
          to='/sign-in'
          startIcon={<LogoutIcon />}
          variant='contained'
          color='secondary'
          onClick={logout}
        >
          Logout
        </Button>
      );
    } else {
      if (currentPath == '/') {
        return (
          <Button
            data-cy='login'
            title='LoginButton'
            component={Link}
            to='/sign-in'
            startIcon={<LoginIcon />}
            variant='contained'
            color='secondary'
          >
            Login
          </Button>
        );
      } else {
        return (
          <Button
            component={Link}
            to='/'
            startIcon={<HomeIcon />}
            variant='contained'
            color='secondary'
          >
            Back to home page
          </Button>
        );
      }
    }
  };

  return (
    <Box
      sx={{
        flexGrow: 1,
        width: '100%',
        top: 0,
        position: 'fixed',
        zIndex: 'modal',
      }}
    >
      <AppBar>
        <Toolbar>
          {props.token ? (
            <>
              <TemporaryDrawer></TemporaryDrawer>
            </>
          ) : (
            <></>
          )}

          <Typography
            variant='h4'
            fontWeight={'bold'}
            component='div'
            sx={{ flexGrow: 1 }}
          >
            Invoicify
          </Typography>
          {buttonCreation()}
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Navbar;
