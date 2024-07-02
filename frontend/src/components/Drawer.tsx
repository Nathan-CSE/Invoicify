import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

import { IconButton, Typography } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { ReactComponent as TickSvg } from '../assets/validate.svg';
import { ReactComponent as PenSvg } from '../assets/create.svg';
import { ReactComponent as SendSvg } from '../assets/send.svg';
import { ReactComponent as ManageSvg } from '../assets/manage.svg';
import { ReactComponent as CogSvg } from '../assets/settings.svg';
import { ReactComponent as DocSvg } from '../assets/documentation.svg';
import { ReactComponent as HomeSvg } from '../assets/home.svg';
import { useNavigate } from 'react-router-dom';

export default function TemporaryDrawer() {
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();
  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  };

  interface dashboardCardInfo {
    svg: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
    route: string;
  }

  interface dashboardDict {
    [key: string]: dashboardCardInfo;
  }

  // REPLACE your route to the page when implemented
  const options = {
    'Home Page': { svg: HomeSvg, route: '/dashboard' },
    'Create/Upload an Invoice': { svg: PenSvg, route: '/invoice-creation' },
    'Validate an Invoice': { svg: TickSvg, route: '/' },
    'Send an Invoice': { svg: SendSvg, route: '/' },
    'Manage Invoices': { svg: ManageSvg, route: '/' },
    'Account Settings': { svg: CogSvg, route: '/settings' },
    'Documentation Info': { svg: DocSvg, route: '/' },
  };

  const DrawerList = (
    <Box sx={{ width: 250 }} role='presentation' onClick={toggleDrawer(false)}>
      <List>
        <Typography variant='h6' component='div' sx={{ textAlign: 'center' }}>
          E-Invoice Manager
        </Typography>
        <Divider />
        {Object.entries(options).map(([name, items], index) => (
          <ListItem
            key={index}
            disablePadding
            onClick={() => {
              navigate(items.route);
            }}
          >
            <ListItemButton>
              <ListItemIcon>
                <items.svg style={{ width: '24px', height: '24px' }} />
              </ListItemIcon>
              <ListItemText primary={name} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <div>
      <IconButton
        size='large'
        edge='start'
        color='inherit'
        aria-label='menu'
        sx={{ mr: 2 }}
        onClick={toggleDrawer(true)}
      >
        <MenuIcon />
      </IconButton>
      <Drawer
        sx={{ zIndex: 'tooltip' }}
        open={open}
        onClose={toggleDrawer(false)}
      >
        {DrawerList}
      </Drawer>
    </div>
  );
}