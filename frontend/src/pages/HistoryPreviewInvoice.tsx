import {
  Box,
  Breadcrumbs,
  Button,
  Divider,
  Grid,
  IconButton,
  Paper,
  Popover,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import * as React from 'react';
import { useLocation } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { Link, useNavigate } from 'react-router-dom';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';
import DownloadIcon from '@mui/icons-material/Download';
import ReplayIcon from '@mui/icons-material/Replay';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import LoadingDialog from '../components/LoadingDialog';
import { ReactComponent as ManageSvg } from '../assets/manage.svg';
import useAuth from './useAuth';

export default function HistoryPreviewInvoice(props: { token: string }) {
  useAuth(props.token);
  const location = useLocation();
  console.log("this is location: ", location);
  const name = location.state.name;

  // Popover Info
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const [invoiceId, setInvoiceId] = React.useState(0);

  const handleClickPopover = (
    event:
      | React.MouseEvent<HTMLButtonElement>
      | React.MouseEvent<HTMLAnchorElement>
  ) => {
    if (event.currentTarget instanceof Element) {
      setAnchorEl(event.currentTarget);
    }
  };

  const handleClosePopover = () => {
    setAnchorEl(null);
  };

  const openPopover = Boolean(anchorEl);
  const id = openPopover ? 'simple-popover' : undefined;
  console.log("this is invoice id: ", id);
  const [dataFields, setDataFields] = React.useState(location.state.fields);
  console.log(dataFields);
  const [invoiceType, setInvoiceType] = React.useState('JSON');
  React.useEffect(() => {
    console.log(location.state);
    setInvoiceId(location.state.invoiceId);
    if (location.state.status) {
      const data = location.state.fields;
      setDataFields(data);
      setInvoiceType('GUI');
    } else {
      // When validating theres a chance the JSON is double stringed so we
      // Have this check in place to parse it correctly
      if (typeof location.state.fields === 'string') {
        setDataFields(JSON.parse(JSON.parse(location.state.fields)));
      }
      setInvoiceType('JSON');
    }
  }, []);

  const handleDownload = async (event: any) => {    
    
    event.preventDefault();

    console.log("this is invoiceId, ", invoiceId);

    try {
      const response = await axios.post(`http://localhost:5000/invoice/download/${invoiceId}`, {
        headers: {
          'Authorisation': `${props.token}`,
        }
      });
      
      if (response.status === 200) {
        console.log(response.data)

        // Tried to change this to use saveAs lib, but ran into a bunch of issues trying to format the 
        // string into a file that was able to be saved
        const url = window.URL.createObjectURL(new Blob([response.data[0]["message"]]));
        const link = document.createElement('a');
        link.href = url;
        console.log(response.data[0]["message"])
        link.setAttribute('download', name);
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

  const formatJSON = (dataFields: any, indentLevel = 0) => {
    let formattedString = '';
    const indent = ' '.repeat(indentLevel * 2); // Use two spaces for each indent level
    console.log(dataFields);

    // Checks if its an object and has children to loop through so we recurse
    // Else we just display the value
    if (dataFields) {
      for (const [key, value] of Object.entries(dataFields)) {
        if (typeof value === 'object') {
          formattedString += `${indent}${key}:\n${formatJSON(
            value,
            indentLevel + 1
          )}`;
        } else {
          const val = value ? value : '';
          console.log(val);
          formattedString += `${indent}${key}: ${val}\n`;
        }
      }
    }
    return formattedString;
  };

  const formatGUI = (dataFields: any) => {
    console.log(dataFields);
    return (
      <>
        <Box>
          <Grid container justifyContent='center' spacing={5}>
            <Grid item xs={12}>
              <Typography
                margin='normal'
                component='div'
                id='invoiceName'
                sx={{ width: '100%' }}
              >
                Invoice Number: {dataFields.ID}
              </Typography>
            </Grid>

            <Grid item xs={12} sx={{ mt: -5 }}>
              <Typography
                margin='normal'
                component='div'
                id='invoiceName'
                sx={{ width: '100%' }}
              >
                Invoice Issue Date: {dataFields.IssueDate}
              </Typography>
            </Grid>
          </Grid>

          {/* BUYER/SELLER HEADER */}
          <Grid container justifyContent='center' spacing={4} sx={{ mb: 2 }}>
            <Grid item xs={5.8}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Seller Information
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                ABN:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PartyLegalEntity
                    .CompanyID['@value']
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Company:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PartyLegalEntity
                    .RegistrationName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                {/* Address: {sellerInfo.companyAddress} */}
              </Typography>

              <Typography variant='h6' sx={{ mt: 3 }}>
                Postal Address
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Street Name:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PostalAddress
                    .StreetName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Additional Street Name:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PostalAddress
                    .additionalStreetName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                City Name:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PostalAddress
                    .CityName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Postal Code:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PostalAddress
                    .PostalZone
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Country:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PostalAddress.Country
                    .IdentificationCode
                }
              </Typography>
            </Grid>

            <Grid item xs={0}>
              <Divider orientation='vertical' sx={{ height: '90%', mt: 6 }} />
            </Grid>

            <Grid item xs={5.8}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Buyer Information
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                ABN:{' '}
                {
                  dataFields.AccountingCustomerParty.Party.PartyLegalEntity
                    .CompanyID['@value']
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Company:{' '}
                {
                  dataFields.AccountingCustomerParty.Party.PartyLegalEntity
                    .RegistrationName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                {/* Address: {buyerInfo.companyAddress} */}
              </Typography>

              <Typography variant='h6' sx={{ mt: 3 }}>
                Postal Address
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Street Name:{' '}
                {
                  dataFields.AccountingCustomerParty.Party.PostalAddress
                    .StreetName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Additional Street Name:{' '}
                {
                  dataFields.AccountingCustomerParty.Party.PostalAddress
                    .AdditionalStreetName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                City Name:{' '}
                {
                  dataFields.AccountingCustomerParty.Party.PostalAddress
                    .CityName
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Postal Code:{' '}
                {
                  dataFields.AccountingCustomerParty.Party.PostalAddress
                    .PostalZone
                }
              </Typography>

              <Typography
                margin='normal'
                component='div'
                sx={{ width: '100%' }}
              >
                Country:{' '}
                {
                  dataFields.AccountingSupplierParty.Party.PostalAddress.Country
                    .IdentificationCode
                }
              </Typography>
            </Grid>
            {/* INVOICE ITEMS */}
            <Grid item xs={12}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Invoice Items
              </Typography>
            </Grid>

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
                  {Array.isArray(dataFields.InvoiceLine) ? (
                    dataFields.InvoiceLine.map((item: any, index: number) => {
                      return (
                        <TableRow key={index}>
                          <TableCell>
                            {item.InvoicedQuantity['@value']}
                          </TableCell>
                          <TableCell>
                            {item.InvoicedQuantity.unitCode}
                          </TableCell>
                          <TableCell>{item?.Item.Name || ''}</TableCell>
                          <TableCell>{item?.Item.Description || ''}</TableCell>
                          <TableCell>
                            {item.Price.PriceAmount['@value']}
                          </TableCell>
                          <TableCell>
                            {(Number(item.Price.PriceAmount['@value']) *
                              Number(
                                dataFields.TaxTotal.TaxSubtotal.TaxCategory
                                  .Percent
                              )) /
                              100}
                          </TableCell>
                          <TableCell>
                            {item.LineExtensionAmount['@value']}
                          </TableCell>
                        </TableRow>
                      );
                    })
                  ) : (
                    <>
                      <TableRow key={dataFields.InvoiceLine.index}>
                        <TableCell>
                          {dataFields.InvoiceLine.InvoicedQuantity['@value']}
                        </TableCell>
                        <TableCell>
                          {dataFields.InvoiceLine.InvoicedQuantity.unitCode}
                        </TableCell>
                        <TableCell>
                          {dataFields?.InvoiceLine.Item.Name || ''}
                        </TableCell>
                        <TableCell>
                          {dataFields?.InvoiceLine.Item.Description || ''}
                        </TableCell>
                        <TableCell>
                          {dataFields.InvoiceLine.Price.PriceAmount['@value']}
                        </TableCell>
                        <TableCell>
                          {(Number(
                            dataFields.InvoiceLine.Price.PriceAmount['@value']
                          ) *
                            Number(
                              dataFields.TaxTotal.TaxSubtotal.TaxCategory
                                .Percent
                            )) /
                            100}
                        </TableCell>
                        <TableCell>
                          {dataFields.InvoiceLine.LineExtensionAmount['@value']}
                        </TableCell>
                      </TableRow>
                    </>
                  )}
                </TableBody>
              </Table>
            </TableContainer>

            {/* MONETARY TOTALS */}
            <Grid item xs={12}>
              <Stack direction='row' spacing={1} sx={{ mt: 4 }}>
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
                <Typography sx={{ p: 2 }}>
                  GST is determined by the buyer's country.
                </Typography>
              </Popover>

              <TableContainer
                component={Paper}
                sx={{ maxWidth: '25vw', my: 2 }}
              >
                <Table aria-label='simple table'>
                  <TableBody>
                    <TableRow>
                      <TableCell>
                        Total GST (
                        {dataFields.TaxTotal.TaxSubtotal.TaxCategory.Percent}%):{' '}
                      </TableCell>
                      <TableCell align='right'>
                        $
                        {
                          dataFields.TaxTotal.TaxSubtotal.TaxableAmount[
                            '@value'
                          ]
                        }
                      </TableCell>
                    </TableRow>

                    <TableRow>
                      <TableCell>Total Taxable Amount: </TableCell>
                      <TableCell align='right'>
                        $
                        {
                          dataFields.LegalMonetaryTotal.TaxExclusiveAmount[
                            '@value'
                          ]
                        }
                      </TableCell>
                    </TableRow>

                    <TableRow>
                      <TableCell>Total Amount: </TableCell>
                      <TableCell align='right'>
                        $
                        {
                          dataFields.LegalMonetaryTotal.TaxInclusiveAmount[
                            '@value'
                          ]
                        }
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>
          </Grid>
        </Box>
      </>
    );
  };

  return (
    <>
      <Box sx={{ mt: 10, ml: 10 }}>
        <Typography variant='h5' sx={{ mt: 4 }}>
          Previeving: {name}
        </Typography>
        <Divider sx={{ borderColor: 'black', width: '100%' }} />
        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize='small' />}
          sx={{ mt: 1 }}
        >
          <Typography component={Link} to='/dashboard'>
            Dashboard
          </Typography>

          <Typography component={Link} to='/invoice-management'>
            Invoice Management
          </Typography>
          <Typography color='text.primary'>Invoice Preview</Typography>
        </Breadcrumbs>
        <Box sx={{ mt: 5 }}>
          {invoiceType === 'JSON' ? (
            <pre style={{ whiteSpace: 'pre-wrap' }}>
              <Typography>{formatJSON(dataFields)}</Typography>
            </pre>
          ) : (
            formatGUI(dataFields)
          )}
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

          <Grid item>
            <Button
              component={Link}
              to='/invoice-management'
              startIcon={<ManageSvg style={{ width: '24px', height: '24px', fill: '#ffffff' }}/>}
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Back to Invoice Management
            </Button>
          </Grid>
        </Grid>

      </Box>
    </>
  );
}
