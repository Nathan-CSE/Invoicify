import React from 'react';
import {
  Button,
  TextField,
  Box,
  Typography,
  Container,
  Divider,
  Breadcrumbs,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
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
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InfoIcon from '@mui/icons-material/Info';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { DropzoneDialogBase } from 'mui-file-dropzone';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import vatRates from '../../VATRates.json';
import ErrorModal from '../../components/ErrorModal';
import axios from 'axios';

interface FileObject {
  file: File;
}

// Edit flag to determine if we are editing
// Data passed in to preload it if we are editing
export default function CreationGUI(props: {
  token: string;
  editFlag: boolean;
  data: any;
  id: number;
}) {
  const navigate = useNavigate();
  const countries = Object.keys(vatRates);
  console.log(props.id);
  const [fields, setFields] = React.useState<any>(null);
  // Preloading the saved data

  React.useEffect(() => {
    if (props.editFlag && props.data) {
      console.log('Hey guys');
      setFields(props.data.fields);
    }
  }, []);

  console.log(fields);

  // Invoice Name State
  const [invName, setInvName] = React.useState<string>('');
  const [invNum, setInvNum] = React.useState<string>('');
  const [date, setDate] = React.useState<Date>(new Date());
  const [sellerABN, setSellerABN] = React.useState<string>('');
  const [sellerName, setSellerName] = React.useState<string>('');
  // const [sellerAddr, setSellerAddr] = React.useState<string>('');
  const [sellerStreetName, setSellerStreetName] = React.useState<string>('');
  const [sellerAddStreetName, setSellerAddStreetName] =
    React.useState<string>('');
  const [sellerCityName, setSellerCityName] = React.useState<string>('');
  const [sellerCode, setSellerCode] = React.useState<string>('');

  const [buyerABN, setBuyerABN] = React.useState<string>('');
  const [buyerName, setBuyerName] = React.useState<string>('');
  const [buyerStreetName, setBuyerStreetName] = React.useState<string>('');
  const [buyerAddStreetName, setBuyerAddStreetName] =
    React.useState<string>('');
  const [buyerCityName, setBuyerCityName] = React.useState<string>('');
  const [buyerCode, setBuyerCode] = React.useState<string>('');

  // Form Information
  const [nextId, setNextId] = React.useState(2);
  const [selectedRowIds, setSelectedRowIds] = React.useState<number[]>([]);
  const [sellerCountry, setSellerCountry] = React.useState('');
  const [buyerCountry, setBuyerCountry] = React.useState('');
  const [vatRate, setVatRate] = React.useState<number>(0);
  const [rows, setRows] = React.useState([
    {
      id: 1,
      quantity: 0,
      unitCode: '',
      item: '',
      description: '',
      unitPrice: 0,
      GST: 0,
      totalPrice: 0,
    },
  ]);
  const handleDateChange = (newDate: any) => {
    setDate(newDate);
  };

  React.useEffect(() => {
    const dateString = fields?.IssueDate || '';
    const [day, month, year] = dateString.split('/');
    const newDate = `${year}-${month}-${day}`;
    setDate(new Date(newDate));
    setInvName(fields?.BuyerReference || '');
    setInvNum(fields?.ID || '');
    setSellerABN(
      fields?.AccountingSupplierParty.Party.PartyLegalEntity.CompanyID[
        '@value'
      ] || ''
    );
    setSellerName(
      fields?.AccountingSupplierParty.Party.PartyLegalEntity.RegistrationName ||
        ''
    );
    setSellerStreetName(
      fields?.AccountingSupplierParty.Party.PostalAddress.StreetName || ''
    );
    setSellerAddStreetName(
      fields?.AccountingSupplierParty.Party.PostalAddress
        .AdditionalStreetName || ''
    );
    setSellerCityName(
      fields?.AccountingSupplierParty.Party.PostalAddress.CityName || ''
    );
    setSellerCode(
      fields?.AccountingSupplierParty.Party.PostalAddress.PostalZone || ''
    );

    setBuyerABN(
      fields?.AccountingCustomerParty.Party.PartyLegalEntity.CompanyID[
        '@value'
      ] || ''
    );
    setBuyerName(
      fields?.AccountingCustomerParty.Party.PartyLegalEntity.RegistrationName ||
        ''
    );
    setBuyerStreetName(
      fields?.AccountingCustomerParty.Party.PostalAddress.StreetName || ''
    );
    setBuyerAddStreetName(
      fields?.AccountingCustomerParty.Party.PostalAddress
        .AdditionalStreetName || ''
    );
    setBuyerCityName(
      fields?.AccountingCustomerParty.Party.PostalAddress.CityName || ''
    );
    setBuyerCode(
      fields?.AccountingCustomerParty.Party.PostalAddress.PostalZone || ''
    );

    if (Array.isArray(fields?.InvoiceLine)) {
      // console.log(rows);
      let tempRows = rows;
      let firstFlag = true;
      fields?.InvoiceLine.forEach((item: any) => {
        if (firstFlag) {
          const newRow = {
            id: 1,
            quantity: parseInt(item?.InvoicedQuantity['@value'], 10),
            unitCode: item?.InvoicedQuantity.unitCode,
            item: item?.Item.Name || '',
            description: item?.Item.Description || '',
            unitPrice: parseInt(item?.Price.PriceAmount['@value'], 10),
            GST: 0,
            totalPrice: 0,
          };
          firstFlag = false;
          // setRows([...rows, newRow]);
          tempRows = [newRow];
          console.log(tempRows);
          // console.log(rows);
        } else {
          const newRow = {
            id: nextId,
            quantity: parseInt(item?.InvoicedQuantity['@value'], 10),
            unitCode: item?.InvoicedQuantity.unitCode,
            item: item?.Item.Name || '',
            description: item?.Item.Description || '',
            unitPrice: parseInt(item?.Price.PriceAmount['@value'], 10),
            GST: 0,
            totalPrice: 0,
          };
          tempRows.push(newRow);
          // setRows([...rows, newRow]);
          setNextId(nextId + 1);
        }
      });
      setRows(tempRows);
    } else {
      if (fields?.InvoiceLine) {
        const newRow = {
          id: 1,
          quantity: parseInt(
            fields?.InvoiceLine.InvoicedQuantity['@value'],
            10
          ),
          unitCode: fields?.InvoiceLine.InvoicedQuantity.unitCode,
          item: fields?.InvoiceLine.Item.Name || '',
          description: fields?.InvoiceLine.Item.Description || '',
          unitPrice: parseInt(
            fields?.InvoiceLine.Price.PriceAmount['@value'],
            10
          ),
          GST: 0,
          totalPrice: 0,
        };
        setRows([newRow]);
        // setNextId(nextId + 1);
      }
    }
  }, [fields]);
  // Uploading additional documents
  const [openFileUpload, setOpenFileUpload] = React.useState(false);
  const [fileList, setFileList] = React.useState<FileObject[]>([]);

  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  // Popover Info
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);

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

  // Function for monetary totals
  const calculateTotals = () => {
    let totalGST = 0;
    let totalTaxable = 0;
    let totalAmount = 0;

    rows.forEach((row) => {
      totalGST += row.GST;
      totalTaxable += row.totalPrice - row.GST;
      totalAmount += row.totalPrice;
    });

    return {
      totalGST: totalGST,
      totalTaxable: totalTaxable,
      totalAmount: totalAmount,
    };
  };

  const { totalGST, totalTaxable, totalAmount } = calculateTotals();

  // Changes the VAT rate based on the buyer's country
  const handleChange = (event: { target: { value: any; name: string } }) => {
    const selectedCountry = event.target.value as keyof typeof vatRates;
    console.log(buyerCountry);
    if (event.target.name == 'buyerCountry') {
      setBuyerCountry(selectedCountry);
      setVatRate(vatRates[selectedCountry]);

      rows.forEach((row) => {
        handleCellValueChange(row);
      });
    } else {
      setSellerCountry(selectedCountry);
    }
  };

  // For adding invoice items
  const columns: GridColDef[] = [
    {
      field: 'quantity',
      headerName: 'Quantity',
      type: 'number',
      width: 75,
      editable: true,
    },
    { field: 'unitCode', headerName: 'Unit Code', width: 100, editable: true },
    { field: 'item', headerName: 'Item', width: 120, editable: true },
    {
      field: 'description',
      headerName: 'Description',
      width: 180,
      editable: true,
    },
    {
      field: 'unitPrice',
      headerName: 'Unit Price ($)',
      type: 'number',
      width: 120,
      editable: true,
    },
    {
      field: 'GST',
      headerName: 'GST ($)',
      type: 'number',
      width: 80,
      editable: false,
    },
    {
      field: 'totalPrice',
      headerName: 'Total Price ($)',
      type: 'number',
      width: 120,
      editable: false,
    },
  ];

  const addRow = () => {
    const newRow = {
      id: nextId,
      quantity: 0,
      unitCode: '',
      item: '',
      description: '',
      unitPrice: 0,
      GST: 0,
      totalPrice: 0,
    };
    setRows([...rows, newRow]);
    setNextId(nextId + 1);
  };

  const removeRow = () => {
    let updatedRows = rows.filter((row) => !selectedRowIds.includes(row.id));
    setRows(updatedRows);
    setSelectedRowIds([]);
  };

  const handleCellValueChange = (newRow: {
    id: any;
    quantity: any;
    unitCode?: string;
    item?: string;
    description?: string;
    unitPrice: any;
    GST: any;
    totalPrice: any;
  }) => {
    newRow.GST = (vatRate / 100) * newRow.unitPrice;
    newRow.totalPrice = newRow.quantity * (newRow.unitPrice + newRow.GST);

    const updatedRows = rows.map((row) =>
      row.id === newRow.id ? { ...row, ...newRow } : row
    );

    setRows(updatedRows);
  };

  // Form submission & sending to backend + error handling
  const handleSubmit = async (event: {
    preventDefault: () => void;
    currentTarget: HTMLFormElement | undefined;
  }) => {
    event.preventDefault();

    let errorCheck = false;

    const formData = new FormData(event.currentTarget);
    const invoiceData: any = {
      invoiceName: formData.get('invoiceName'),
      invoiceNumber: Number(formData.get('invoiceNumber')),
      invoiceIssueDate: formData.get('invoiceIssueDate'),
      seller: {
        ABN: Number(formData.get('sellerABN')),
        companyName: formData.get('sellerCompanyName'),
        companyAddress: formData.get('sellerAddress'),
        address: {
          streetName: formData.get('sellerStreetName'),
          additionalStreetName: formData.get('sellerAdditionalStreetName'),
          cityName: formData.get('sellerCityName'),
          postalCode: formData.get('sellerPostalCode'),
          country: sellerCountry,
        },
      },
      buyer: {
        ABN: Number(formData.get('buyerABN')),
        companyName: formData.get('buyerCompanyName'),
        companyAddress: formData.get('buyerAddress'),
        address: {
          streetName: formData.get('buyerStreetName'),
          additionalStreetName: formData.get('buyerAdditionalStreetName'),
          cityName: formData.get('buyerCityName'),
          postalCode: formData.get('buyerPostalCode'),
          country: buyerCountry,
        },
      },
      invoiceItems: rows.map((row) => ({
        quantity: row.quantity,
        unitCode: row.unitCode,
        item: row.item,
        description: row.description,
        unitPrice: row.unitPrice,
        GST: row.GST,
        totalPrice: row.totalPrice,
      })),
      totalGST: totalGST,
      totalTaxable: totalTaxable,
      totalAmount: totalAmount,
      buyerVatRate: vatRate,
      additionalDocuments: fileList.map((file) => ({
        fileName: file.file.name,
        fileSize: file.file.size,
        fileMimeType: file.file.type,
      })),
      extraComments: formData.get('extraComments'),
    };

    if (invoiceData.invoiceIssueDate === '') {
      setOpenError(true);
      setError('Please select an invoice issue date.');
      errorCheck = true;
    }

    for (let i = 0; i < rows.length; i++) {
      const unitCode = rows[i].unitCode;

      if (!unitCode.match(/^[A-Z]{3}$/)) {
        setOpenError(true);
        setError(
          `Invalid unit code '${unitCode}' for item ${rows[i].item}. Unit code must be a 3-letter alphanumeric combination in all uppercase.`
        );
        errorCheck = true;
        break;
      }
    }

    const {
      buyerVatRate,
      additionalDocuments,
      extraComments,
      ...filteredInvoiceData
    } = invoiceData;
    var str = JSON.stringify(filteredInvoiceData, null, 2);
    console.log('filtered: ', str);

    if (errorCheck) {
      return;
    } else {
      if (props.editFlag) {
        console.log(filteredInvoiceData);
        const response = await axios.put(
          `http://localhost:5000/invoice/edit/${props.id}`,
          {
            name: formData.get('invoiceName'),
            fields: filteredInvoiceData,
            rule: 'AUNZ_PEPPOL_1_0_10',
          },

          {
            headers: {
              Authorisation: `${props.token}`,
            },
          }
        );

        if (response.status === 204) {
          alert('Edit Successful');
        } else {
          console.log(response);
          alert('Unable to edit invoice');
        }

        navigate('/invoice-management');
      } else {
        try {
          const response = await axios.post(
            'http://localhost:5000/invoice/create',
            filteredInvoiceData,
            {
              headers: {
                Authorisation: `${props.token}`,
              },
            }
          );

          if (response.status === 201) {
            // This is the one that should be working, but the api backend does not work
            // navigate('/invoice-confirmation', { state: { invoice: invoiceData, type: 'GUI' } });

            // This is to make the response object consistent betwee invoices create via GUI and upload
            console.log('this is reponse data: ', response.data);
            console.log('this is reponse data.data: ', response.data.data);
            const customResponse = {
              invoice: {
                data: [
                  {
                    // NOTE: This method chaining fucking sucks -> wtf is this
                    filename: response.data.data[0].filename,
                    invoiceId: response.data.data[0].invoiceId,
                  },
                ],
              },
              type: 'GUI',
              // This doesn't seem right... but it's how the invoicecreation gui via bulk upload returns
              invoiceId: response.data.data[0].invoiceId,
            };

            navigate('/invoice-creation-confirmation', {
              state: customResponse,
            });
          } else {
            console.log(response);
            alert('Unable to create invoice');
          }
        } catch (err) {
          console.error(err);
          alert(err);
        }
        // SEND TO BACKEND HERE -> if successful, go to confirmation page
        return;
      }
    }
  };

  return (
    <>
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        {props.editFlag ? (
          <>
            <Typography variant='h4'>Invoice Edit</Typography>
            <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />
            <Breadcrumbs
              aria-label='breadcrumb'
              separator={<NavigateNextIcon fontSize='small' />}
            >
              <Typography component={Link} to='/dashboard'>
                Dashboard
              </Typography>

              <Typography component={Link} to='/invoice-management'>
                Invoice Management
              </Typography>

              <Typography color='text.primary'>Invoice Edit</Typography>
            </Breadcrumbs>
          </>
        ) : (
          <>
            <Typography variant='h4'>Invoice Creation - GUI</Typography>
            <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />
            <Breadcrumbs
              aria-label='breadcrumb'
              separator={<NavigateNextIcon fontSize='small' />}
            >
              <Typography component={Link} to='/dashboard'>
                Dashboard
              </Typography>

              <Typography component={Link} to='/invoice-creation'>
                Invoice Creation
              </Typography>

              <Typography color='text.primary'>
                Invoice Creation - GUI
              </Typography>
            </Breadcrumbs>
          </>
        )}

        <form onSubmit={handleSubmit}>
          {/* INVOICE HEADER */}
          <Typography variant='h5' sx={{ mt: 4 }}>
            Invoice Header
          </Typography>

          <Grid container justifyContent='center' spacing={5} sx={{ mb: 2 }}>
            <Grid item xs={6}>
              <TextField
                margin='normal'
                required
                id='invoiceName'
                label='Invoice Name'
                name='invoiceName'
                autoFocus
                sx={{ width: '100%' }}
                value={invName}
                onChange={(e) => setInvName(e.target.value)}
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                margin='normal'
                required
                id='invoiceNumber'
                label='Invoice Number'
                name='invoiceNumber'
                autoFocus
                sx={{ width: '100%' }}
                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                value={invNum}
                onChange={(e) => setInvNum(e.target.value)}
              />
            </Grid>

            <Grid item xs={12} sx={{ mt: -5 }}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker
                    label='Invoice Issue Date'
                    name='invoiceIssueDate'
                    format='dd/MM/yyyy'
                    sx={{ width: '100%' }}
                    value={date}
                    onChange={handleDateChange}
                  />
                </DemoContainer>
              </LocalizationProvider>
            </Grid>
          </Grid>

          {/* BUYER/SELLER HEADER */}
          <Grid container justifyContent='center' spacing={4} sx={{ mb: 2 }}>
            <Grid item xs={5.8}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Seller Information
              </Typography>

              <TextField
                margin='normal'
                required
                id='sellerABN'
                label='Seller ABN'
                name='sellerABN'
                sx={{ width: '100%' }}
                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                value={sellerABN}
                onChange={(e) => setSellerABN(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='sellerCompanyName'
                label='Company Name'
                name='sellerCompanyName'
                sx={{ width: '100%' }}
                value={sellerName}
                onChange={(e) => setSellerName(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='sellerAddress'
                label='Address'
                name='sellerAddress'
                sx={{ width: '100%' }}
              />

              <Typography variant='h6' sx={{ mt: 1 }}>
                Postal Address
              </Typography>

              <TextField
                margin='normal'
                required
                id='sellerStreetName'
                label='Street Name'
                name='sellerStreetName'
                sx={{ width: '100%' }}
                value={sellerStreetName}
                onChange={(e) => setSellerStreetName(e.target.value)}
              />

              <TextField
                margin='normal'
                id='sellerAdditionalStreetName'
                label='Additional Street Name'
                name='sellerAdditionalStreetName'
                sx={{ width: '100%' }}
                value={sellerAddStreetName}
                onChange={(e) => setSellerAddStreetName(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='sellerCityName'
                label='City Name'
                name='sellerCityName'
                sx={{ width: '100%' }}
                value={sellerCityName}
                onChange={(e) => setSellerCityName(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='sellerPostalCode'
                label='Postal Code'
                name='sellerPostalCode'
                sx={{ width: '100%' }}
                value={sellerCode}
                onChange={(e) => setSellerCode(e.target.value)}
              />

              <FormControl sx={{ mt: 2, width: '100%' }}>
                <InputLabel id='country-label'>Country</InputLabel>
                <Select
                  labelId='country-label'
                  id='country'
                  required
                  name='sellerCountry'
                  value={sellerCountry}
                  onChange={handleChange}
                  label='Country'
                  // placeholder='Country'
                  sx={{ width: '100%' }}
                >
                  {countries.map((country, index) => (
                    <MenuItem key={index} value={country}>
                      {country}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={0}>
              <Divider orientation='vertical' sx={{ height: '90%', mt: 10 }} />
            </Grid>

            <Grid item xs={5.8}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Buyer Information
              </Typography>

              <TextField
                margin='normal'
                required
                id='buyerABN'
                label='Buyer ABN'
                name='buyerABN'
                sx={{ width: '100%' }}
                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                value={buyerABN}
                onChange={(e) => setBuyerABN(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='buyerCompanyName'
                label='Company Name'
                name='buyerCompanyName'
                sx={{ width: '100%' }}
                value={buyerName}
                onChange={(e) => setBuyerName(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='buyerAddress'
                label='Address'
                name='buyerAddress'
                sx={{ width: '100%' }}
              />

              <Typography variant='h6' sx={{ mt: 1 }}>
                Postal Address
              </Typography>

              <TextField
                margin='normal'
                required
                id='buyerStreetName'
                label='Street Name'
                name='buyerStreetName'
                sx={{ width: '100%' }}
                value={buyerStreetName}
                onChange={(e) => setBuyerStreetName(e.target.value)}
              />

              <TextField
                margin='normal'
                id='buyerAdditionalStreetName'
                label='Additional Street Name'
                name='buyerAdditionalStreetName'
                sx={{ width: '100%' }}
                value={buyerAddStreetName}
                onChange={(e) => setBuyerAddStreetName(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='buyerCityName'
                label='City Name'
                name='buyerCityName'
                sx={{ width: '100%' }}
                value={buyerCityName}
                onChange={(e) => setBuyerCityName(e.target.value)}
              />

              <TextField
                margin='normal'
                required
                id='buyerPostalCode'
                label='Postal Code'
                name='buyerPostalCode'
                sx={{ width: '100%' }}
                value={buyerCode}
                onChange={(e) => setBuyerCode(e.target.value)}
              />

              <FormControl sx={{ mt: 2, width: '100%' }}>
                <InputLabel id='country-label'>Country</InputLabel>
                <Select
                  labelId='country-label'
                  id='country'
                  required
                  name='buyerCountry'
                  value={buyerCountry}
                  onChange={handleChange}
                  label='Country'
                  sx={{ width: '100%' }}
                >
                  {countries.map((country, index) => (
                    <MenuItem key={index} value={country}>
                      {country}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          {/* INVOICE ITEMS */}
          <Typography variant='h5' sx={{ mt: 4 }}>
            Invoice Items
          </Typography>

          <Box sx={{ width: '100%' }}>
            <Stack direction='row' spacing={1} sx={{ my: 1.5 }}>
              <Button size='small' onClick={addRow} variant='contained'>
                Add a Row
              </Button>
              {selectedRowIds.length > 0 && (
                <Button size='small' onClick={removeRow} variant='contained'>
                  Remove Selected Rows
                </Button>
              )}
            </Stack>
            <Box sx={{ height: 400, width: '100%' }}>
              <DataGrid
                rows={rows}
                columns={columns}
                checkboxSelection
                disableRowSelectionOnClick
                autoPageSize
                disableColumnMenu
                rowSelectionModel={selectedRowIds}
                onRowSelectionModelChange={(rowIds) => {
                  // console.log("this is rowIds: ", rowIds);
                  setSelectedRowIds(rowIds.map((id) => Number(id)));
                }}
                processRowUpdate={(newRow) => {
                  handleCellValueChange(newRow);
                  return newRow;
                }}
                onProcessRowUpdateError={(error) => {
                  console.error('Row update error:', error);
                }}
              />
            </Box>
          </Box>

          {/* MONETARY TOTALS */}
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

          <TableContainer component={Paper} sx={{ maxWidth: '25vw', my: 2 }}>
            <Table aria-label='simple table'>
              <TableBody>
                <TableRow>
                  <TableCell>Total GST ({vatRate}%): </TableCell>
                  <TableCell align='right'>
                    ${totalGST.toLocaleString()}
                  </TableCell>
                </TableRow>

                <TableRow>
                  <TableCell>Total Taxable Amount: </TableCell>
                  <TableCell align='right'>
                    ${totalTaxable.toLocaleString()}
                  </TableCell>
                </TableRow>

                <TableRow>
                  <TableCell>Total Amount: </TableCell>
                  <TableCell align='right'>
                    ${totalAmount.toLocaleString()}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          {/* ADDITIONAL OPTIONS */}
          <Typography variant='h5' sx={{ mt: 4, mb: 2 }}>
            Additional Options
          </Typography>
          <Button
            variant='contained'
            color='primary'
            onClick={() => setOpenFileUpload(true)}
          >
            Upload Additional Documents
          </Button>
          <DropzoneDialogBase
            dialogTitle={'Upload file'}
            acceptedFiles={['image/*']}
            fileObjects={fileList.map((fileObj) => ({
              ...fileObj,
              data: null,
            }))}
            cancelButtonText={'cancel'}
            submitButtonText={'submit'}
            maxFileSize={5000000}
            open={openFileUpload}
            onAdd={(newFileObjs: FileObject[]) => {
              console.log('onAdd', newFileObjs);
              setFileList((prevFileObjects) => [
                ...prevFileObjects,
                ...newFileObjs,
              ]);
            }}
            onDelete={(deleteFileObj) => {
              console.log('onDelete', deleteFileObj);
            }}
            onClose={() => setOpenFileUpload(false)}
            onSave={() => {
              console.log('onSave', fileList);
              setOpenFileUpload(false);
            }}
            showPreviews={true}
            showFileNamesInPreview={true}
          />

          <Typography variant='h6' sx={{ mt: 4 }}>
            Extra Comments
          </Typography>
          <TextField
            multiline
            rows={5}
            name='extraComments'
            sx={{ width: '100%' }}
          />

          <Box textAlign='center'>
            <Button
              type='submit'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
                my: 6,
              }}
            >
              Finish & Save Invoice
            </Button>
          </Box>
        </form>

        {openError && (
          <ErrorModal open={openError} setOpen={setOpenError}>
            {error}
          </ErrorModal>
        )}
      </Container>
    </>
  );
}
