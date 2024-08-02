import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import InvoiceFlavourImage from '../assets/stock_invoice.png';
import { ReactComponent as TickSvg } from '../assets/validate.svg';
import { ReactComponent as PenSvg } from '../assets/create.svg';
import { ReactComponent as SendSvg } from '../assets/send.svg';
import { Container } from '@mui/material';
import checkAuth from '../helpers/useAuth';

function HomePage(props: { token: string }) {
  const navigate = useNavigate();
  checkAuth(props.token);

  React.useEffect(() => {
    console.log('HOME');
    props.token === '' ? navigate('/') : navigate('/dashboard');
  }, [props.token]);

  return (
    <>
      {/* <Navbar /> */}
      <Container maxWidth='lg' sx={{ marginY: 10 }}>
        <Box sx={{ display: 'flex', flexDirection: 'row' }}>
          <Box>
            <Typography variant='h3' gutterBottom>
              About us
            </Typography>
            <Typography variant='body1' gutterBottom>
              Invoicify is an invoicing web service to streamline 
              the logistics of payments for vendors. Our solution is 
              targeted towards the SMEs who lack reliable modern solutions f
              or e-invoice creation, validation, and sending. 
              Invoicify is a one stop ecosystem, we will handle everything 
              a user can do with invoices, from creation from the seller’s extracted data, 
              to sending it to the recipient’s email address.
            </Typography>
          </Box>
          <Box>
            <img
              src={InvoiceFlavourImage}
              alt='invoice vector illustration'
            ></img>
          </Box>
        </Box>

        {/* Feature Icons */}
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

      </Container>
    </>
  );
}

export default HomePage;
