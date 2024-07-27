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
            Your file has been created
          </Typography>
        </Box>

        <Box
          sx={{
            my: 10,
            padding: 5,
            height: '25vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            border: 'solid 0.5px',
            borderRadius: 4
          }}
        >
          <Box sx={{ mt: 1 }}>
            <Typography textAlign='center'>
              {invoiceData["invoice"]["invoiceName"]}
            </Typography>
          </Box>

        </Box>

        <Grid container justifyContent="center" spacing={6}>
          <Grid item>
            <Button
              onClick={handleDownload}
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