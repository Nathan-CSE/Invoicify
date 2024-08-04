import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
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

function TemporaryDrawer() {
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();
  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  };

  interface dashboardCardInfo {
    svg: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
    route: string;
    cy: string;
  }

  interface dashboardDict {
    [key: string]: dashboardCardInfo;
  }

  const options = {
    Dashboard: { svg: HomeSvg, route: '/dashboard', cy: 'drawer-dashboard' },
    'Create/Upload an Invoice': {
      svg: PenSvg,
      route: '/invoice-creation',
      cy: 'drawer-creation',
    },
    'Validate an Invoice': {
      svg: TickSvg,
      route: '/invoice-validation',
      cy: 'drawer-validation',
    },
    'Send an Invoice': {
      svg: SendSvg,
      route: '/invoice-sending',
      cy: 'drawer-sending',
    },
    'Manage Invoices': {
      svg: ManageSvg,
      route: '/invoice-management',
      cy: 'drawer-management',
    },
    'Account Settings': {
      svg: CogSvg,
      route: '/settings',
      cy: 'drawer-settings',
    },
    'Documentation Info': {
      svg: DocSvg,
      route: '/documentation',
      cy: 'drawer-documentation',
    },
  };

  const DrawerList = (
    <Box sx={{ width: 250 }} role='presentation' onClick={toggleDrawer(false)}>
      <List>
        <Typography
          variant='h5'
          fontWeight={'bold'}
          component='div'
          sx={{ textAlign: 'center', my: 1 }}
        >
          Invoicify
        </Typography>
        <Divider sx={{ mb: 1 }} />
        {Object.entries(options).map(([name, items], index) => (
          <ListItem
            data-cy={items.cy}
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
        data-cy='toggle-drawer'
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

export default TemporaryDrawer;
