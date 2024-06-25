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
import vatRates from '../VATRates.json';
import ErrorModal from '../components/ErrorModal';

interface FileObject {
  file: File;
}

export default function CreationGUI() {
  const navigate = useNavigate();
  const countries = Object.keys(vatRates);

  // Form Information
  const [nextId, setNextId] = React.useState(2);
  const [selectedRowIds, setSelectedRowIds] = React.useState<number[]>([]);
  const [sellerCountry, setSellerCountry] = React.useState('');
  const [buyerCountry, setBuyerCountry] = React.useState('');
  const [vatRate, setVatRate] = React.useState(0);
  const [rows, setRows] = React.useState([
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
  ]);
  
  // Uploading additional documents
  const [openFileUpload, setOpenFileUpload] = React.useState(false);
  const [fileList, setFileList] = React.useState<FileObject[]>([]);

  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

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
      totalAmount: totalAmount
    };
  };

  const { totalGST, totalTaxable, totalAmount } = calculateTotals();

  // Changes the VAT rate based on the buyer's country
  const handleChange = (event: { target: { value: any; name: string; }; }) => {
    const selectedCountry = event.target.value as keyof typeof vatRates;
    
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

  // For adding invoice items
  const columns: GridColDef[] = [
    { field: 'quantity', headerName: 'Quantity', type: 'number', width: 75, editable: true },
    { field: 'unitCode', headerName: 'Unit Code', width: 100, editable: true },
    { field: 'item', headerName: 'Item', width: 120, editable: true },
    { field: 'description', headerName: 'Description', width: 180, editable: true },
    { field: 'unitPrice', headerName: 'Unit Price ($)', type: 'number', width: 120, editable: true },
    { field: 'GST', headerName: 'GST ($)', type: 'number', width: 80, editable: false },
    { field: 'totalPrice', headerName: 'Total Price ($)', type: 'number', width: 120, editable: false },
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

  const handleCellValueChange = (newRow: { id: any; quantity: any; unitCode?: string; item?: string; description?: string; unitPrice: any; GST: any; totalPrice: any; }) => {

    newRow.GST = (vatRate / 100) * newRow.unitPrice;
    newRow.totalPrice = newRow.quantity * (newRow.unitPrice + newRow.GST);

    const updatedRows = rows.map((row) =>
      row.id === newRow.id ? { ...row, ...newRow } : row
    );
    setRows(updatedRows);
  };
  
  // Form submission & sending to backend + error handling
  const handleSubmit = (event: { preventDefault: () => void; currentTarget: HTMLFormElement | undefined; }) => {
    event.preventDefault();
    
    let errorCheck = false;

    const formData = new FormData(event.currentTarget);
    const invoiceData = {
      invoiceName: formData.get('invoiceName'),
      invoiceNumber: formData.get('invoiceNumber'),
      invoiceIssueDate: formData.get('invoiceIssueDate'),
      seller: {
        ABN: formData.get('sellerABN'),
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
        ABN: formData.get('buyerABN'),
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
      vatRate: vatRate,
      additionalDocuments: fileList.map(file => ({
        fileName: file.file.name,
        fileSize: file.file.size,
        fileMimeType: file.file.type,
      })),
      extraComments: formData.get('extraComments'),
    };

    if (invoiceData.invoiceIssueDate === "") {
      setOpenError(true);
      setError("Please select an invoice issue date.");
      errorCheck = true;
    }

    
    for (let i = 0; i < rows.length; i++) {
      const unitCode = rows[i].unitCode;

      if (!unitCode.match(/^[A-Z]{3}$/)) {
        setOpenError(true);
        setError(`Invalid unit code '${unitCode}' for item ${rows[i].item}. Unit code must be a 3-letter alphanumeric combination in all uppercase.`);
        errorCheck = true;
        break;
      }
    }

    console.log('Formatted Invoice Data:', invoiceData);

    if (errorCheck) {
      return;
    } else {
      // SEND TO BACKEND HERE -> if successful, go to confirmation page
      navigate('/invoice-confirmation', { state: invoiceData });
      return;
    }

    

  };

  return (
    <>      
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
                required
                id="sellerABN"
                label="ABN"
                name="sellerABN"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                required
                id="sellerCompanyName"
                label="Company Name"
                name="sellerCompanyName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                required
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
                required
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
                required
                id="sellerCityName"
                label="City Name"
                name="sellerCityName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                required
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
                  required
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
                required
                id="buyerABN"
                label="ABN"
                name="buyerABN"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                required
                id="buyerCompanyName"
                label="Company Name"
                name="buyerCompanyName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                required
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
                required
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
                required
                id="buyerCityName"
                label="City Name"
                name="buyerCityName"
                sx={{ width: '100%' }}
              />

              <TextField
                margin="normal"
                required
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
                  required
                  name="buyerCountry"
                  value={buyerCountry}
                  onChange={handleChange}
                  label="Country"
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
          <Button variant="contained" color="primary" onClick={() => setOpenFileUpload(true)}>
            Upload Additional Documents
          </Button>
          <DropzoneDialogBase
            dialogTitle={"Upload file"}
            acceptedFiles={['image/*']}
            fileObjects={fileList.map(fileObj => ({ ...fileObj, data: null }))}
            cancelButtonText={"cancel"}
            submitButtonText={"submit"}
            maxFileSize={5000000}
            open={openFileUpload}
            onAdd={(newFileObjs: FileObject[]) => {
              console.log('onAdd', newFileObjs);
              setFileList(prevFileObjects => [...prevFileObjects, ...newFileObjs]);
            }}
            onDelete={deleteFileObj => {
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

        <Box sx={{ mb: 6 }}>
          {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
        </Box>
      </Container>
    </>
  );
}