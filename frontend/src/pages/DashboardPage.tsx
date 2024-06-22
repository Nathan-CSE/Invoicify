import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
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

  interface SVGDict {
    [key: string]: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  }

  const options = {
    'Create/Upload an Invoice': PenSvg,
    'Validate an Invoice': TickSvg,
    'Send an Invoice': SendSvg,
    'Manage Invoices': ManageSvg,
    'Account Settings': CogSvg,
    'Documentation Info': DocSvg,
  };

  function generateOptions(options: SVGDict): JSX.Element[] {
    return Object.entries(options).map(([name, SVG], index) => (
      <Grid key={index} item>
        <Card
          sx={{
            border: 1,
            borderRadius: '16px',
            width: '20rem',
            height: '18rem',
            alignContent: 'center',
            textAlign: 'center',
            display: 'flex',
          }}
        >
          <CardActionArea>
            <CardContent>
              <SVG />
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
      {/* <Navbar></Navbar> */}
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
