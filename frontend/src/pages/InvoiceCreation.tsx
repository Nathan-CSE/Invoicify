import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
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
import axios from 'axios';
import { DropzoneArea } from "mui-file-dropzone";

export default function InvoiceCreation(props: { token: string; }) {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [file, setFile] = React.useState<File[]>([]);

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    navigate('/invoice-confirmation');
    setOpen(false);
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    handleOpen();

    console.log('file to be sent: ', file);

    try {
      // Placeholder until backend endpoint has been created
      const response = await axios.post('http://localhost:5000/invoice/create', file, {
        headers: {
          'Authorization': `Bearer ${props.token}`
        }
      });
      
      if (response.status === 201) {
        navigate('/invoice-confirmation');

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
          Invoice Creation
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

          <Typography color='text.primary'>
            Invoice Creation
          </Typography>
        </Breadcrumbs>

        <Box sx={{ my: 5 }}>
          <DropzoneArea
            acceptedFiles={['.pdf', '.json']}
            fileObjects={file}
            onChange={(loadedFile) => {
              console.log('Currently loaded:', loadedFile)
              setFile(loadedFile);
            }}
            filesLimit={1}
          />
        </Box>

        <Box textAlign='center'>
          <Button
            onClick={handleSubmit}
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Generate Invoices
          </Button>
          {/* NOTE: Send to backend and create invoices */}
        </Box>

        <Dialog
          open={open}
          onClose={handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {"Your invoice has been created and saved to your account."}
          </DialogTitle>
          <DialogActions>
            <Button onClick={handleClose} autoFocus>
              Confirm
            </Button>
          </DialogActions>
        </Dialog>

        <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
          OR
        </Typography>

        <Box textAlign='center'>
          <Button
            component={Link}
            to='/invoice-creation-GUI'
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
      
    </>
  );
}