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
import { Card, CardActionArea, CardContent } from '@mui/material';
import { ReactComponent as InvoiceSvg } from '../../assets/invoice.svg';
import DownloadIcon from '@mui/icons-material/Download';
import ReplayIcon from '@mui/icons-material/Replay';
import IconButton from '@mui/material/IconButton';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';

export default function InvoiceCreationConfirmation(props: { token: string; }) {
  const invoiceData = useLocation().state;
  console.log('invoice data: ', invoiceData);
  const { data: invoices, type } = invoiceData.invoice;
  // const invoiceType = invoiceData.type;
  const [currentIndex, setCurrentIndex] = React.useState(0);

  console.log('this is the invoice data: ', invoiceData);
  
  const handlePrevious = () => {
    setCurrentIndex((prevIndex) => Math.max(prevIndex - 1, 0));
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => Math.min(prevIndex + 1, invoices.length - 1));
  };


  const handleDownload = async (event: any) => {    
    
    event.preventDefault();
    
    const invoiceInt = invoiceData.invoiceId.data[0]["invoiceId"];
    console.log('this is invoice int ', invoiceInt);
    const data = {
      "article_id": invoiceInt
    }

    try {
      // Placeholder until backend endpoint has been created
      const response = await axios.post(`http://localhost:5000/invoice/download/` + invoiceInt, {
        headers: {
          'Authorisation': `${props.token}`,
        }
      });
      
      if (response.status === 200) {
        console.log(response.data)
        const url = window.URL.createObjectURL(new Blob([response.data[0]["message"]]));
        const link = document.createElement('a');
        link.href = url;
        console.log(response.data[0]["message"])
        link.setAttribute('download', invoiceData["invoiceId"].data[0]["filename"]);
        document.body.appendChild(link);
        link.click();
        link.remove();

      } else {
        console.log(response);
        alert("Unable to create invoice");
      }
    } catch (err) {
      alert(err)
    }

  };

  return (
    <>
      
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
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 4, mb: 8 }}>
            <IconButton
              aria-label="check"
              onClick={handlePrevious} 
              disabled={currentIndex === 0} 
              sx={{ mr: 2 }}
            >
              <KeyboardArrowLeftIcon sx={{ fontSize: 60 }} />
            </IconButton>

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

            <IconButton
              aria-label="check"
              onClick={handleNext} 
              disabled={currentIndex === invoices.length - 1} 
              sx={{ ml: 2 }}
            >
              <KeyboardArrowRightIcon sx={{ fontSize: 60 }} />
            </IconButton>

          </Box>
        )}

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

