import React from 'react';
import Navbar from '../components/Navbar';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
// import InvoiceFlavourImage from '../images/invoice.png';
import InvoiceFlavourImage from '../assets/stock_invoice.png';
import { ReactComponent as TickSvg } from '../assets/tick.svg';
import { ReactComponent as PenSvg } from '../assets/pen.svg';
import { ReactComponent as SendSvg } from '../assets/send.svg';
function HomePage() {
  return (
    <>
      <Navbar></Navbar>
      <Box sx={{ display: 'flex', flexDirection: 'row', mt: 10 }}>
        <Box>
          <Typography variant='h2' gutterBottom>
            Placeholder
          </Typography>
          <Typography variant='body1' gutterBottom>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quos
            blanditiis tenetur unde suscipit, quam beatae rerum inventore
            consectetur, neque doloribus, cupiditate numquam dignissimos laborum
            fugiat deleniti? Eum quasi quidem quibusdam. Lorem ipsum dolor sit
            amet, consectetur adipisicing elit. Quos blanditiis tenetur unde
            suscipit, quam beatae rerum inventore consectetur, neque doloribus,
            cupiditate numquam dignissimos laborum fugiat deleniti? Eum quasi
            quidem quibusdam.
          </Typography>
        </Box>
        <Box>
          <img
            src={InvoiceFlavourImage}
            alt='invoice vector illustration'
          ></img>
        </Box>
      </Box>

      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          gap: 8,
          mt: 8,
          justifyContent: 'center',
        }}
      >
        <Box sx={{ alignContent: 'center', textAlign: 'center' }}>
          <Box
            sx={{
              border: 6,
              borderRadius: '50%',
              borderColor: '#2196F3',
              width: 150,
              height: 150,
              alignContent: 'center',
              textAlign: 'center',
            }}
          >
            <TickSvg />
          </Box>
          <Typography
            variant='subtitle1'
            sx={{ fontWeight: 'bold' }}
            gutterBottom
          >
            INVOICE VALIDATION
          </Typography>
        </Box>

        <Box sx={{ alignContent: 'center', textAlign: 'center' }}>
          <Box
            sx={{
              border: 6,
              borderRadius: '50%',
              borderColor: '#2196F3',
              width: 150,
              height: 150,
              alignContent: 'center',
              textAlign: 'center',
            }}
          >
            <PenSvg />
          </Box>
          <Typography
            variant='subtitle1'
            sx={{ fontWeight: 'bold' }}
            gutterBottom
          >
            INVOICE CREATION
          </Typography>
        </Box>

        <Box sx={{ alignContent: 'center', textAlign: 'center' }}>
          <Box
            sx={{
              border: 6,
              borderRadius: '50%',
              borderColor: '#2196F3',
              width: 150,
              height: 150,
              alignContent: 'center',
              textAlign: 'center',
            }}
          >
            <SendSvg />
          </Box>
          <Typography
            variant='subtitle1'
            sx={{ fontWeight: 'bold' }}
            gutterBottom
          >
            INVOICE SENDING
          </Typography>
        </Box>
      </Box>
    </>
  );
}

export default HomePage;
