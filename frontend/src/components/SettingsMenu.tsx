import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Box, Stack, Typography } from '@mui/material';
import { ReactComponent as InvoiceSettings } from '../assets/settings_mini.svg';

export default function SettingsMenu() {
  const [anchorEl, setAnchorEl] = React.useState<null | SVGElement>(null);
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<SVGElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    console.log('1');
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
              onClick={handleEdit}
              variant='contained'
              sx={{ minWidth: '6rem' }}
            >
              SEND
            </Button>
          </Box>
          <Box onClick={handleClose}>
            <Button
              onClick={handleEdit}
              variant='contained'
              color='error'
              sx={{ minWidth: '6rem' }}
            >
              DELETE
            </Button>
          </Box>
        </Stack>
      </Menu>
    </div>
  );
}
