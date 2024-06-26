import React from 'react';
import {
  Button,
  Box,
  Typography,
  Container,
  Divider,
  Breadcrumbs,
  Stack,
} from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import PrintableInvoice from '../components/PrintableInvoice';
import { useReactToPrint } from 'react-to-print';

export default function PreviewInvoice() {

  const componentRef = React.useRef<HTMLDivElement>(null);
  const handlePrint = useReactToPrint({
    content: () => componentRef.current || null,
  });

  const location = useLocation();

  const invoiceInfo = location.state.state;
  const sellerInfo = invoiceInfo.seller;
  const buyerInfo = invoiceInfo.buyer;
  const invoiceItems = invoiceInfo.invoiceItems;
  const invoiceDocuments = invoiceInfo.additionalDocuments;
  
  return (
    <>      
      <Container maxWidth="lg" sx={{ marginTop: 11 }}>
        <Typography variant='h4'>
          Invoice Preview
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
            Invoice Preview
          </Typography>
        </Breadcrumbs>

        <PrintableInvoice
          ref={componentRef}
          invoiceInfo={invoiceInfo}
          sellerInfo={sellerInfo}
          buyerInfo={buyerInfo}
          invoiceItems={invoiceItems}
          invoiceDocuments={invoiceDocuments}
        />


        <Stack direction="row" spacing={5} sx={{ my: 4, justifyContent: 'center' }}>
          <Button 
            onClick={handlePrint}
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
              my: 6
            }} 
          >
            Print/Save Invoice 
          </Button>

          <Button
            component={Link}
            to='/invoice-creation'
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
              my: 6
            }}
          >
            Create another Invoice
          </Button>
        </Stack>

        <Box textAlign='center'>
        </Box>
      </Container>
    </>
  );
}