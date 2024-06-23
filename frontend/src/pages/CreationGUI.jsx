import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Navbar from '../components/Navbar';
import Divider from '@mui/material/Divider';
import { Link, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import FileUpload from '../components/FileUpload';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import FormControl from '@mui/material/FormControl';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Grid from '@mui/material/Grid';
import { DataGrid } from '@mui/x-data-grid';
import Stack from '@mui/material/Stack';
import vatRates from '../VATRates.json';
import { InputLabel, Select, MenuItem } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { DropzoneDialogBase } from 'mui-file-dropzone';
import Popover from '@mui/material/Popover';
import InfoIcon from '@mui/icons-material/Info';

const theme = createTheme({
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

const countries = Object.keys(vatRates);

const initialRows = [
  { 
    id: 1,
    quantity: 0,
    unitCode: '',
    item: '',
    description: '',
    unitPrice: 0,
    GST: 0,
    totalPrice: 0 
  },
];


export default function CreationGUI() {
  const navigate = useNavigate();

  const [rows, setRows] = React.useState(initialRows);
  const [nextId, setNextId] = React.useState(2);
  const [selectedRowIds, setSelectedRowIds] = React.useState([]);
  const [sellerCountry, setSellerCountry] = React.useState('');
  const [buyerCountry, setBuyerCountry] = React.useState('');
  const [vatRate, setVatRate] = React.useState(0);
  
  const [open, setOpen] = React.useState(false);
  const [fileObjects, setFileObjects] = React.useState([]);

  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const openPopover = Boolean(anchorEl);
  const id = openPopover ? 'simple-popover' : undefined;

  const dialogTitle = () => (
    <>
      <span>Upload file</span>
      <IconButton
        style={{right: '12px', top: '8px', position: 'absolute'}}
        onClick={() => setOpen(false)}>
        <CloseIcon />
      </IconButton>
    </>
  );

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
      totalAmount: totalAmount
    };
  };

  const { totalGST, totalTaxable, totalAmount } = calculateTotals();

  const handleChange = (event) => {
    const selectedCountry = event.target.value;
    
    console.log(event.target);

    if (event.target.name == "buyerCountry") {
      setBuyerCountry(selectedCountry);
      setVatRate(vatRates[selectedCountry]);

      rows.forEach((row) => {
        handleCellValueChange(row);
      })
    } else {
      setSellerCountry(selectedCountry);
    }
  };

  const addRow = () => {
    const newRow = { 
      id: nextId,
      quantity: 0,
      unitCode: '',
      item: '',
      description: '',
      unitPrice: 0,
      GST: 0,
      totalPrice: 0 
    };
    setRows([...rows, newRow]);
    setNextId(nextId + 1);
  };

  const removeRow = () => {
    let updatedRows = rows.filter((row) => !selectedRowIds.includes(row.id));
    setRows(updatedRows);
    setSelectedRowIds([]);
  };

  const handleCellValueChange = (newRow) => {

    newRow.GST = (vatRate / 100) * newRow.unitPrice;
    newRow.totalPrice = newRow.quantity * (newRow.unitPrice + newRow.GST);

    const updatedRows = rows.map((row) =>
      row.id === newRow.id ? { ...row, ...newRow } : row
    );
    setRows(updatedRows);
  };
  
  const columns = [
    { field: 'quantity', headerName: 'Quantity', type: 'number', width: 75, editable: true },
    { field: 'unitCode', headerName: 'Unit Code', width: 100, editable: true },
    { field: 'item', headerName: 'Item', width: 120, editable: true },
    { field: 'description', headerName: 'Description', width: 180, editable: true },
    { field: 'unitPrice', headerName: 'Unit Price ($)', type: 'number', width: 120, editable: true },
    { field: 'GST', headerName: 'GST ($)', type: 'number', width: 80, editable: false },
    { field: 'totalPrice', headerName: 'Total Price ($)', type: 'number', width: 120, editable: false },
  ];
  
  const handleSubmit = (event) => {
    event.preventDefault();
    
    const formData = new FormData(event.currentTarget);
    const invoiceData = {
      invoiceName: formData.get('invoiceName'),
      invoiceNumber: formData.get('invoiceNumber'),
      invoiceIssueDate: formData.get('invoiceIssueDate'),
      seller: {
        ABN: formData.get('sellerABN'),
        companyName: formData.get('sellerCompanyName'),
        address: {
          streetName: formData.get('sellerStreetName'),
          additionalStreetName: formData.get('sellerAdditionalStreetName'),
          cityName: formData.get('sellerCityName'),
          postalCode: formData.get('sellerPostalCode'),
          country: sellerCountry,
        },
      },
      buyer: {
        ABN: formData.get('buyerABN'),
        companyName: formData.get('buyerCompanyName'),
        address: {
          streetName: formData.get('buyerStreetName'),
          additionalStreetName: formData.get('buyerAdditionalStreetName'),
          cityName: formData.get('buyerCityName'),
          postalCode: formData.get('buyerPostalCode'),
          country: buyerCountry,
        },
      },
      invoiceItems: rows.map(row => ({
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
      additionalDocuments: fileObjects.map(file => ({
        fileName: file.file.name,
        fileSize: file.file.size,
        fileMimeType: file.file.type,
      })),
      extraComments: formData.get('extraComments'),
    };

    console.log('Formatted Invoice Data:', invoiceData);
    
    // SEND TO BACKEND HERE

  };

  return (
    <>
      <ThemeProvider theme={theme}>

      <Navbar />
      
      <Container maxWidth="lg" sx={{ marginTop: 11 }}>
        <Typography variant='h4'>
          Invoice Creation - GUI
        </Typography>

        <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />

        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize="small" />}
        >
          <Typography
            component={Link}
            to='/sign-in'
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
            Invoice Creation - GUI
          </Typography>
        </Breadcrumbs>

        <form onSubmit={handleSubmit}>
          {/* INVOICE HEADER */}
          <Typography variant='h5' sx={{ mt: 4 }}>
            Invoice Header
          </Typography>

          <Grid container justifyContent="center" spacing={5} sx={{ mb: 2 }}>
            <Grid item xs={6}>
              <TextField
                margin="normal"
                required
                id="invoiceName"
                label="Invoice Name"
                name="invoiceName"
                autoFocus
                sx={{ width: '100%' }}
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                margin="normal"
                required
                id="invoiceNumber"
                label="Invoice Number"
                name="invoiceNumber"
                autoFocus
                sx={{ width: '100%' }}
              />
            </Grid>

            <Grid item xs={12} sx={{ mt: -5 }}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker 
                    label="Invoice Issue Date"
                    name='invoiceIssueDate'
                    format="dd/MM/yyyy"
                    sx={{ width: '100%' }}
                  />
                </DemoContainer>
              </LocalizationProvider>
            </Grid>

          </Grid>

          {/* BUYER/SELLER HEADER */}
          <Grid container justifyContent="center" spacing={4} sx={{ mb: 2 }}>
            <Grid item xs={5.8}> 
              <Typography variant='h5' sx={{ mt: 4 }}>
                Seller Information
              </Typography>

              <TextField
                margin="normal"
                id="sellerABN"
                label="ABN"
                name="sellerABN"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerCompanyName"
                label="Company Name"
                name="sellerCompanyName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerAddress"
                label="Address"
                name="sellerAddress"
                sx={{ width: '100%' }}
              />

              <Typography variant='h6' sx={{ mt: 1 }}>
                Postal Address
              </Typography>


              <TextField
                margin="normal"
                id="sellerStreetName"
                label="Street Name"
                name="sellerStreetName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerAdditionalStreetName"
                label="Additional Street Name"
                name="sellerAdditionalStreetName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerCityName"
                label="City Name"
                name="sellerCityName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerPostalCode"
                label="Postal Code"
                name="sellerPostalCode"
                sx={{ width: '100%' }}
              />

              <FormControl sx={{ mt: 2, width: '100%' }}>
                <InputLabel id="country-label">Country</InputLabel>
                <Select
                  labelId="country-label"
                  id="country"
                  name="sellerCountry"
                  value={sellerCountry}
                  onChange={handleChange}
                  label="Country"
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
              <Divider orientation="vertical" sx={{ height: '90%', mt: 10 }} />
            </Grid>

            <Grid item xs={5.8}> 
              <Typography variant='h5' sx={{ mt: 4 }}>
                Buyer Information
              </Typography>

              <TextField
                margin="normal"
                id="buyerABN"
                label="ABN"
                name="buyerABN"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="buyerCompanyName"
                label="Company Name"
                name="buyerCompanyName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="buyerAddress"
                label="Address"
                name="buyerAddress"
                sx={{ width: '100%' }}
              />

              <Typography variant='h6' sx={{ mt: 1 }}>
                Postal Address
              </Typography>


              <TextField
                margin="normal"
                id="buyerStreetName"
                label="Street Name"
                name="buyerStreetName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="buyerAdditionalStreetName"
                label="Additional Street Name"
                name="buyerAdditionalStreetName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="buyerCityName"
                label="City Name"
                name="buyerCityName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="buyerPostalCode"
                label="Postal Code"
                name="buyerPostalCode"
                sx={{ width: '100%' }}
              />

              <FormControl sx={{ mt: 2, width: '100%' }}>
                <InputLabel id="country-label">Country</InputLabel>
                <Select
                  labelId="country-label"
                  id="country"
                  name="buyerCountry"
                  value={buyerCountry}
                  onChange={handleChange}
                  label="Country"
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

          </Grid>

          {/* INVOICE ITEMS */}
          <Typography variant='h5' sx={{ mt: 4 }}>
            Invoice Items
          </Typography>

          <Box sx={{ width: '100%' }}>
            <Stack direction="row" spacing={1} sx={{ my: 1.5 }}>
              <Button size="small" onClick={addRow} variant='contained'>
                Add a Row
              </Button>
              {selectedRowIds.length > 0 && (
                <Button
                  size="small"
                  onClick={removeRow}
                  variant='contained'
                >
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
                selectionModel={selectedRowIds}
                onRowSelectionModelChange={(rowIds) => {
                  setSelectedRowIds(rowIds);
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

          <Stack direction="row" spacing={1} sx={{ mt: 4 }}>
            <Typography variant='h5'>Monetary Totals</Typography>
            <IconButton onClick={handleClick}>
              <InfoIcon sx={{ mt: -0.25 }} />
            </IconButton>
          </Stack>
          <Popover
            id={id}
            open={openPopover}
            anchorEl={anchorEl}
            onClose={handleClose}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left',
            }}
          >
            <Typography sx={{ p: 2 }}>GST is determined by the buyer's country.</Typography>
          </Popover>

          {/* MONETARY TOTALS */}
          <TableContainer component={Paper} sx={{ maxWidth: '25vw', my: 2 }}>
            <Table aria-label="simple table">
              <TableBody>
                <TableRow>
                  <TableCell>Total GST ({vatRate}%): </TableCell>
                  <TableCell align="right">${totalGST.toLocaleString()}</TableCell>
                </TableRow>

                <TableRow>
                  <TableCell>Total Taxable Amount: </TableCell>
                  <TableCell align="right">${totalTaxable.toLocaleString()}</TableCell>
                </TableRow>
            
                <TableRow>
                  <TableCell>Total Amount: </TableCell>
                  <TableCell align="right">${totalAmount.toLocaleString()}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          {/* ADDITIONAL OPTIONS */}
          <Typography variant='h5' sx={{ mt: 4, mb: 2 }}>Additional Options</Typography>
          <Button variant="contained" color="primary" onClick={() => setOpen(true)}>
            Upload Additional Documents
          </Button>
          <DropzoneDialogBase
            dialogTitle={dialogTitle()}
            acceptedFiles={['image/*']}
            fileObjects={fileObjects}
            cancelButtonText={"cancel"}
            submitButtonText={"submit"}
            maxFileSize={5000000}
            open={open}
            onAdd={newFileObjs => {
              console.log('onAdd', newFileObjs);
              setFileObjects([].concat(fileObjects, newFileObjs));
            }}
            onDelete={deleteFileObj => {
              console.log('onDelete', deleteFileObj);
            }}
            onClose={() => setOpen(false)}
            onSave={() => {
              console.log('onSave', fileObjects);
              setOpen(false);
            }}
            showPreviews={true}
            showFileNamesInPreview={true}
          />

          <Typography variant='h6' sx={{ mt: 4 }}>Extra Comments</Typography>
          <TextField
            multiline
            rows={5}
            name='extraComments'
            sx={{ width: '100%' }}
          />

          <Box textAlign='center'>
            <Button
              type="submit"
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
                my: 6
              }}
            >
              Finish & Save Invoice
            </Button>
          </Box>
        
        </form>
      </Container>

      </ThemeProvider>
    </>
  );
}