import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, Navigate, useNavigate, useLocation } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Grid from '@mui/material/Grid';
import axios from 'axios';
import { Card, CardActionArea, CardContent, Stack } from '@mui/material';
import { ReactComponent as InvoiceSvg } from '../../assets/invoice.svg';
import DownloadIcon from '@mui/icons-material/Download';
import ReplayIcon from '@mui/icons-material/Replay';
import IconButton from '@mui/material/IconButton';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import LoadingDialog from '../../components/LoadingDialog';
import useAuth from '../useAuth';

export default function InvoiceCreationConfirmation(props: { token: string; }) {
  useAuth(props.token);
  const invoiceData = useLocation().state;
  console.log('invoice data: ', invoiceData);
  const { data: invoices } = invoiceData.invoice;
  const invoiceId = invoiceData.invoiceId;
  const [currentIndex, setCurrentIndex] = React.useState(0);
  const [loading, setLoading] = React.useState(false);

  console.log('this is the invoice data: ', invoiceData);
  
  const handlePrevious = () => {
    setCurrentIndex((prevIndex) => Math.max(prevIndex - 1, 0));
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => Math.min(prevIndex + 1, invoices.length - 1));
  };


  const handleDownload = async (event: any) => {    
    
    event.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`http://localhost:5000/invoice/download/${invoiceId}`, {
        headers: {
          'Authorisation': `${props.token}`,
        }
      });
      
      setLoading(false);
      if (response.status === 200) {
        console.log(response.data)

        // Tried to change this to use saveAs lib, but ran into a bunch of issues trying to format the 
        // string into a file that was able to be saved
        const url = window.URL.createObjectURL(new Blob([response.data[0]["message"]]));
        const link = document.createElement('a');
        link.href = url;
        console.log(response.data[0]["message"])
        link.setAttribute('download', invoices[currentIndex].filename);
        document.body.appendChild(link);
        link.click();
        link.remove();

      } else {
        console.log(response);
        alert("Unable to create invoice");
      }
    } catch (err) {
      console.error(err);
      alert(err)
    }

  };

  return (
    <>
      <LoadingDialog open={loading} message='Downloading invoice...' />
      <Container maxWidth="lg" sx={{ marginTop: 11 }}>
        <Typography variant='h4'>
          Invoice Creation Result
        </Typography>

        <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />

        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize="small" />}
        >
          <Typography
            component={Link}
            to='/dashboard'
          >
            Dashboard
          </Typography>

          <Typography
            component={Link}
            to='/invoice-creation'
          >
            Invoice Creation
          </Typography>

          <Typography color='text.primary'>
            Invoice Creation Result
          </Typography>
        </Breadcrumbs>

        <Box textAlign='center' sx={{ mt: 5 }}>
          <Typography variant='h4'>
            Your file(s) have been created
          </Typography>
        </Box>

        {invoices.length > 0 && (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 4, mb: 4 }}>

            <Card
              sx={{
                border: 1,
                borderRadius: '16px',
                width: '20rem',
                height: '24rem',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              <CardContent>
                <InvoiceSvg style={{ width: 175, height: 175, marginBottom: 65, marginTop: 25 }} />
                <Typography variant='h6' component='div'>
                  {invoices[currentIndex].filename}
                </Typography>
              </CardContent>
            </Card>

          </Box>
        )}

        <Stack direction="row" spacing={2} sx={{ mb: 2, justifyContent: 'center', alignItems: 'center' }}>
          <Button onClick={handlePrevious} disabled={currentIndex === 0} startIcon={<KeyboardArrowLeftIcon />}>Previous</Button>
          <Typography>
            {currentIndex + 1} / {invoices.length}
          </Typography>
          <Button onClick={handleNext} disabled={currentIndex === invoices.length - 1} endIcon={<KeyboardArrowRightIcon />}>Next</Button>
        </Stack>

        <Divider 
          sx={{ 
            my: 5,
            borderBottomWidth: 2,
          }}
        />

        <Grid container justifyContent="center" spacing={6}>
          <Grid item>
            <Button
              onClick={handleDownload}
              startIcon={<DownloadIcon />}
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Download Invoice
            </Button>
          </Grid>

          <Grid item>
            <Button
              component={Link}
              to='/invoice-creation'
              startIcon={<ReplayIcon />}
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Create another Invoice
            </Button>
          </Grid>
        </Grid>


      </Container>

    </>
  );
}

