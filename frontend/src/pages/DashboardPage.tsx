import React from 'react';
import { Routes, Route, useNavigate, Link } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import { ReactComponent as TickSvg } from '../assets/validate.svg';
import { ReactComponent as PenSvg } from '../assets/create.svg';
import { ReactComponent as SendSvg } from '../assets/send.svg';

import { ReactComponent as ManageSvg } from '../assets/manage.svg';
import { ReactComponent as CogSvg } from '../assets/settings.svg';
import { ReactComponent as DocSvg } from '../assets/documentation.svg';

// Current Idea -> For loop to create each grid item and card to make it so we dont have to repeat code
// Wow yeap
// - The svgs have the name corresponding to the options -> just make it lower
// - Assign a custom string based on the option value -> Switch case
// - Issue: Have to integrate cardaction and usenavigate here... so?? figure that out yeah

function DashboardPage(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  console.log(props.token);

  interface dashboardCardInfo {
    svg: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
    route: string;
  }

  interface dashboardDict {
    [key: string]: dashboardCardInfo;
  }

  // REPLACE your route to the page when implemented
  const options = {
    'Create/Upload an Invoice': { svg: PenSvg, route: '/invoice-creation' },
    'Validate an Invoice': { svg: TickSvg, route: '/invoice-validation' },
    'Send an Invoice': { svg: SendSvg, route: '/invoice-sending' },
    'Manage Invoices': { svg: ManageSvg, route: '/invoice-management' },
    'Account Settings': { svg: CogSvg, route: '/settings' },
    'Documentation Info': { svg: DocSvg, route: '/documentation' },
  };

  // Function to generate the dashboard card
  function generateOptions(options: dashboardDict): JSX.Element[] {
    return Object.entries(options).map(([name, items], index) => (
      <Grid key={index} item>
        <Card
          component={Link}
          to={items.route}
          sx={{
            border: 1,
            borderRadius: '16px',
            width: '20rem',
            height: '18rem',
            alignContent: 'center',
            textAlign: 'center',
            display: 'flex',
            textDecoration: 'none',
          }}
        >
          <CardActionArea>
            <CardContent>
              <items.svg />
              <Typography variant='h6' component='div'>
                {name}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid>
    ));
  }

  return (
    <>
      <Box sx={{ mt: 10 }}>
        <Grid
          container
          spacing={9}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          {generateOptions(options)}
        </Grid>
      </Box>
    </>
  );
}

export default DashboardPage;
