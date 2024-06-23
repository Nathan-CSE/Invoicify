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
  const [vatRate, setVatRate] = React.useState(null);
  
  const [open, setOpen] = React.useState(false);
  const [fileObjects, setFileObjects] = React.useState([]);

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

    if (event.target.name == "sellerCountry") {
      setSellerCountry(selectedCountry);
      setVatRate(vatRates[selectedCountry]);

      rows.forEach((row) => {

        handleCellValueChange(row);
      })
    } else {
      setBuyerCountry(selectedCountry)
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

  const handleSelectionChange = (newSelection) => {
    setSelectedRowIds(newSelection.selectionModel);
  };

  const handleCellValueChange = (newRow) => {

    newRow.GST = (vatRate / 100) * newRow.unitPrice;
    newRow.totalPrice = newRow.quantity * (newRow.unitPrice + newRow.GST);

    const updatedRows = rows.map((row) =>
      row.id === newRow.id ? { ...row, ...newRow } : row
    );
    setRows(updatedRows);
    // console.log('these are the updated rows: ', updatedRows);
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
    const data = new FormData(event.currentTarget);

    const username = data.get('username');
    const password = data.get('password');
    
    if (username.length === 0 || password === 0) {
      alert('Fill out all required fields');
    } else {
      try {
        // send to backend
      } catch (err) {
        alert(err.response.data.error);
      }
    }

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

        {/* <Box sx={{ my: 5 }}>
          <FileUpload />
        </Box> */}


        <form onSubmit={handleSubmit}>
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
                    sx={{ width: '100%' }}
                  />
                </DemoContainer>
              </LocalizationProvider>
            </Grid>

          </Grid>

          {/* =========================================================== */}

          <Grid container justifyContent="center" spacing={10} sx={{ mb: 2 }}>
            <Grid item xs={6}> 
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

            <Grid item xs={6}> 
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

        </form>

        <Typography variant='h5' sx={{ mt: 4 }}>
          Invoice Items
        </Typography>

        <Box sx={{ width: '100%' }}>
          <Stack direction="row" spacing={1} sx={{ my: 1.5 }}>
            <Button size="small" onClick={removeRow} variant='contained'>
              Remove Selected Rows
            </Button>
            <Button size="small" onClick={addRow} variant='contained'>
              Add a Row
            </Button>
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

        <Typography variant='h5' sx={{ mt: 4 }}>Monetary Totals</Typography>
        <TableContainer component={Paper} sx={{ maxWidth: '25vw', my: 2 }}>
          <Table aria-label="simple table">
            <TableBody>
              <TableRow>
                <TableCell>Total GST: </TableCell>
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

        <Typography variant='h5' sx={{ mt: 4 }}>Additional Options</Typography>
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


        <Box textAlign='center'>
          <Button
            component={Link}
            to='/sign-in'
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Create a New Invoice
          </Button>
        </Box>
      </Container>

      </ThemeProvider>
    </>
  );
}