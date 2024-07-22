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
import SettingsMenu from '../../components/SettingsMenu';
import { ReactComponent as InvoiceSvg } from '../../assets/invoice.svg';
import DownloadIcon from '@mui/icons-material/Download';

export default function InvoiceCreationConfirmation(props: { token: string; }) {
  const navigate = useNavigate();
  const invoiceData = useLocation().state;
  const invoiceType = invoiceData.type;
  console.log('this is the invoice data: ', invoiceData);

  const handlePreview = () => {
    navigate('/invoice-preview', { state: invoiceData.invoice });
  }

  const handleDownload = async (event: any) => {
    
    
    event.preventDefault();
  
    const invoiceInt = invoiceData.invoiceInt;
    console.log('this is invoice int ', invoiceInt);
    const data = {
      "article_id": invoiceInt
    }

    try {
      // Placeholder until backend endpoint has been created
      const response = await axios.post(`http://localhost:5000/invoice/download`, data, {
        headers: {
          'Authorisation': `${props.token}`,
        }
      });
      
      if (response.status === 200) {
        // navigate('/invoice-confirmation');
        console.log(response);

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


        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            my: 5,
          }}
        >
          <Card
            sx={{
              border: 1,
              borderRadius: '16px',
              width: '20rem',
              height: '24rem',
              alignContent: 'center',
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              textDecoration: 'none',
              position: 'relative',
            }}
          >
            <CardContent
              sx={{
                mt: 2,
                height: '24rem',
              }}
            >
              <InvoiceSvg />
              <Typography variant='h6' component='div'>
                INVOICE NAME
              </Typography>

            </CardContent>
          </Card>
        </Box>

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

          {/* Conditionally show preview only if invoice created via gui */}
          {
            invoiceType !== 'upload' &&
            <Grid item>
              <Button
                onClick={handlePreview}
                variant='contained'
                sx={{
                  height: '50px',
                  padding: '25px',
                }}
              >
                Preview Invoice
              </Button>
            </Grid>
          }

          <Grid item>
            <Button
              component={Link}
              to='/invoice-creation'
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