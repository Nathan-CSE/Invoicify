// PrintableInvoice.tsx
import React, { forwardRef } from 'react';
import {
  Typography,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Paper,
  IconButton,
  Popover,
  Grid,
  Stack,
  TableHead,
  ListItem,
  List,
  ListItemText,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';


export const PrintableInvoice = (
  { invoiceInfo, sellerInfo, buyerInfo, invoiceItems, invoiceDocuments }: 
  { invoiceInfo: any, sellerInfo: any, buyerInfo: any, invoiceItems: any, invoiceDocuments: any }, ref: any) => {
  
    // Popover Info
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);

  const handleClickPopover = (event: React.MouseEvent<HTMLButtonElement> | React.MouseEvent<HTMLAnchorElement>) => {
    if (event.currentTarget instanceof Element) {
      setAnchorEl(event.currentTarget);
    }
  };

  const handleClosePopover = () => {
    setAnchorEl(null);
  };

  const openPopover = Boolean(anchorEl);
  const id = openPopover ? 'simple-popover' : undefined;


  return (
    <>
      {/* INVOICE HEADER */}
      <div ref={ref}>
        <Typography variant='h5' sx={{ mt: 4 }}>
          {invoiceInfo.invoiceName}
        </Typography>

        <Grid container justifyContent="center" spacing={5}>

          <Grid item xs={12}>
            <Typography
              margin="normal"
              component="div"
              id="invoiceName"
              sx={{ width: '100%' }}
            >
              Invoice Number: {invoiceInfo.invoiceNumber}
            </Typography>
          </Grid>

          <Grid item xs={12} sx={{ mt: -5 }}>
            <Typography
              margin="normal"
              component="div"
              id="invoiceName"
              sx={{ width: '100%' }}
            >
              Invoice Issue Date: {invoiceInfo.invoiceIssueDate}
            </Typography>
          </Grid>

        </Grid>

        {/* BUYER/SELLER HEADER */}
        <Grid container justifyContent="center" spacing={4} sx={{ mb: 2 }}>
          <Grid item xs={5.8}> 
            <Typography variant='h5' sx={{ mt: 4 }}>
              Seller Information
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              ABN: {sellerInfo.ABN}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Company: {sellerInfo.companyName}
            </Typography>
          

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Address: {sellerInfo.companyAddress}
            </Typography>

            <Typography variant='h6' sx={{ mt: 3 }}>
              Postal Address
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Street Name: {sellerInfo.address.streetName}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Additional Street Name: {sellerInfo.address.additionalStreetName}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              City Name: {sellerInfo.address.cityName}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Postal Code: {sellerInfo.address.postalCode}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Country: {sellerInfo.address.country}
            </Typography>

          </Grid>

          <Grid item xs={0}>
            <Divider orientation="vertical" sx={{ height: '90%', mt: 6 }} />
          </Grid>

          <Grid item xs={5.8}> 
            <Typography variant='h5' sx={{ mt: 4 }}>
              Buyer Information
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              ABN: {buyerInfo.ABN}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Company: {buyerInfo.companyName}
            </Typography>
          

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Address: {buyerInfo.companyAddress}
            </Typography>

            <Typography variant='h6' sx={{ mt: 3 }}>
              Postal Address
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Street Name: {buyerInfo.address.streetName}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Additional Street Name: {buyerInfo.address.additionalStreetName}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              City Name: {buyerInfo.address.cityName}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Postal Code: {buyerInfo.address.postalCode}
            </Typography>

            <Typography
              margin="normal"
              component="div"
              sx={{ width: '100%' }}
            >
              Country: {buyerInfo.address.country}
            </Typography>

          </Grid>

        </Grid>

        {/* INVOICE ITEMS */}
        <Typography variant='h5' sx={{ mt: 4 }}>
          Invoice Items
        </Typography>

        <TableContainer component={Paper} sx={{ mt: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Quantity</TableCell>
                <TableCell>Unit Code</TableCell>
                <TableCell>Item</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Unit Price ($)</TableCell>
                <TableCell>GST ($)</TableCell>
                <TableCell>Total Price ($)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {invoiceItems.map((item: any, index: number) => (
                <TableRow key={index}>
                  <TableCell>{item.quantity}</TableCell>
                  <TableCell>{item.unitCode}</TableCell>
                  <TableCell>{item.item}</TableCell>
                  <TableCell>{item.description}</TableCell>
                  <TableCell>{item.unitPrice}</TableCell>
                  <TableCell>{item.GST}</TableCell>
                  <TableCell>{item.totalPrice}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        {/* MONETARY TOTALS */}
        <Stack direction="row" spacing={1} sx={{ mt: 4 }}>
          <Typography variant='h5'>Monetary Totals</Typography>
          <IconButton onClick={handleClickPopover}>
            <InfoIcon sx={{ mt: -0.25 }} />
          </IconButton>
        </Stack>
        <Popover
          id={id}
          open={openPopover}
          anchorEl={anchorEl}
          onClose={handleClosePopover}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
        >
          <Typography sx={{ p: 2 }}>GST is determined by the buyer's country.</Typography>
        </Popover>

        <TableContainer component={Paper} sx={{ maxWidth: '25vw', my: 2 }}>
          <Table aria-label="simple table">
            <TableBody>
              <TableRow>
                <TableCell>Total GST ({invoiceInfo.vatRate}%): </TableCell>
                <TableCell align="right">${invoiceInfo.totalGST.toLocaleString()}</TableCell>
              </TableRow>

              <TableRow>
                <TableCell>Total Taxable Amount: </TableCell>
                <TableCell align="right">${invoiceInfo.totalTaxable.toLocaleString()}</TableCell>
              </TableRow>
          
              <TableRow>
                <TableCell>Total Amount: </TableCell>
                <TableCell align="right">${invoiceInfo.totalAmount.toLocaleString()}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>

        <Typography variant='h5' sx={{ mt: 4, mb: 0 }}>Additional Documents</Typography>
        <List>
          {invoiceDocuments.map((document: any, index: number) => (
            <ListItem key={index}>
              <ListItemText primary={document.fileName} secondary={`Size: ${document.fileSize} | Type: ${document.fileMimeType}`} />
            </ListItem>
          ))}
        </List>

        <Typography variant='h6' sx={{ mt: 4 }}>Extra Comments</Typography>
        <Typography
          margin="normal"
          component="div"
          sx={{ width: '100%' }}
        >
          {invoiceInfo.extraComments}
        </Typography>
      </div>
    </>
  );
};

export default forwardRef(PrintableInvoice);