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

const options = [
  'CREATE',
  'VALIDATE',
  'SEND',
  'MANAGE',
  'SETTINGS',
  'DOCUMENTATION',
];

// Current Idea -> For loop to create each grid item and card to make it so we dont have to repeat code
// Wow yeap
// - The svgs have the name corresponding to the options -> just make it lower
// - Assign a custom string based on the option value -> Switch case
// - Issue: Have to integrate cardaction and usenavigate here... so?? figure that out yeah

const bull = (
  <Box
    component='span'
    sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
  >
    •
  </Box>
);

const card = (
  <React.Fragment>
    <CardContent>
      <Typography sx={{ fontSize: 14 }} color='text.secondary' gutterBottom>
        Word of the Day
      </Typography>
      <Typography variant='h5' component='div'>
        be{bull}nev{bull}o{bull}lent
      </Typography>
      <Typography sx={{ mb: 1.5 }} color='text.secondary'>
        adjective
      </Typography>
      <Typography variant='body2'>
        well meaning and kindly.
        <br />
        {'"a benevolent smile"'}
      </Typography>
    </CardContent>
    <CardActions>
      <Button size='small'>Learn More</Button>
    </CardActions>
  </React.Fragment>
);

function DashboardPage() {
  return (
    <>
      <Navbar></Navbar>
      <Box sx={{ mt: 10 }}>
        <Grid container spacing={3}>
          <Grid item xs={4}>
            <Card variant='outlined'>{card}</Card>
          </Grid>
          <Grid item xs={4}>
            hello
          </Grid>
          <Grid item xs={4}>
            hello
          </Grid>
        </Grid>
      </Box>
    </>
  );
}

export default DashboardPage;
