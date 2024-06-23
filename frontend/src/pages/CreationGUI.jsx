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

const theme = createTheme({
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

const initialRows = [
  { id: 1, item: '', quantity: 0, unitPrice: 0, totalPrice: 0 },
];

export default function CreationGUI() {
  const navigate = useNavigate();

  const [rows, setRows] = React.useState(initialRows);
  const [nextId, setNextId] = React.useState(2); // To track the next available ID for new rows
  const [selectedRowIds, setSelectedRowIds] = React.useState([]);

  const addRow = () => {
    const newRow = { id: nextId, item: '', quantity: 0, unitPrice: 0, totalPrice: 0 };
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

    const updatedRows = rows.map((row) =>
      row.id === newRow.id ? { ...row, ...newRow } : row
    );
    setRows(updatedRows);
    console.log('these are the updated rows: ', updatedRows);
  };
  
  const columns = [
    { field: 'item', headerName: 'Item', width: 200, editable: true },
    { field: 'quantity', headerName: 'Quantity', type: 'number', width: 150, editable: true },
    { field: 'unitPrice', headerName: 'Unit Price ($)', type: 'number', width: 150, editable: true },
    { field: 'totalPrice', headerName: 'Total Price ($)', type: 'number', width: 150, editable: false },
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

            <Grid item xs={6} sx={{ mt: -4 }}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker 
                    label="Invoice Issue Date"
                    sx={{ width: '100%' }}
                  />
                </DemoContainer>
              </LocalizationProvider>
            </Grid>

            <Grid item xs={6} sx={{ mt: -4 }}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker 
                    label="Invoice Due Date"
                    sx={{ width: '100%' }}
                  />
                </DemoContainer>
              </LocalizationProvider>
            </Grid>
          </Grid>

          {/* =========================================================== */}

          <Grid container justifyContent="center" spacing={5} sx={{ mb: 2 }}>
            <Grid item xs={6}> 
              <Typography variant='h5' sx={{ mt: 4 }}>
                Seller Information
              </Typography>

              <TextField
                margin="normal"
                id="sellerFirstName"
                label="First name"
                name="sellerFirstName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerLastName"
                label="Last name"
                name="sellerLastName"
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

              <TextField
                margin="normal"
                id="sellerEmailAddress"
                label="Email Address"
                name="sellerEmailAddress"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerPhoneNumber"
                label="Phone Number"
                name="sellerPhoneNumber"
                sx={{ width: '100%' }}
              />

            </Grid>

            <Grid item xs={6}> 
              <Typography variant='h5' sx={{ mt: 4 }}>
                Buyer Information
              </Typography>

              <TextField
                margin="normal"
                id="sellerFirstName"
                label="First name"
                name="sellerFirstName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerLastName"
                label="Last name"
                name="sellerLastName"
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

              <TextField
                margin="normal"
                id="sellerEmailAddress"
                label="Email Address"
                name="sellerEmailAddress"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                id="sellerPhoneNumber"
                label="Phone Number"
                name="sellerPhoneNumber"
                sx={{ width: '100%' }}
              />
            </Grid>


              
          </Grid>

        </form>

        <Typography variant='h5' sx={{ mt: 4 }}>
          Invoice Items
        </Typography>

        <Box sx={{ width: '100%' }}>
          <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
            <Button size="small" onClick={removeRow}>
              Remove a row
            </Button>
            <Button size="small" onClick={addRow}>
              Add a row
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
                newRow.totalPrice = newRow.quantity * newRow.unitPrice;
                handleCellValueChange(newRow);
                return newRow;
              }}
              onProcessRowUpdateError={(error) => {
                console.error('Row update error:', error);
              }}
            />
          </Box>
        </Box>


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