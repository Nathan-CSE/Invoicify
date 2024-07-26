import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Navbar from '../../components/Navbar';
import Divider from '@mui/material/Divider';
import { Link, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import FileUpload from '../../components/FileUpload';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import axios from 'axios';
import { DropzoneArea } from 'mui-file-dropzone';
import { BsPencilSquare } from "react-icons/bs";
import { FaFileUpload } from "react-icons/fa";

export default function InvoiceCreation(props: { token: string }) {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [files, setFiles] = React.useState<File[]>([]);

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    navigate('/invoice-creation-confirmation');
    setOpen(false);
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    const formData = new FormData();

    if (files) {
      files.forEach(item => {
        formData.append("files", item);
      });
    } else {
      alert('You must upload a valid file to create an invoice.');
      return;
    }

    // console.log('file to be sent: ', file);

    try {
      const response = await axios.post('http://localhost:5000/invoice/uploadCreate', formData, {
        headers: {
          Authorisation: `${props.token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        console.log(response.data);
        var str = JSON.stringify(response.data, null, 2);
        console.log(str);
        navigate('/invoice-creation-confirmation', {
          state: {
            invoice: response.data,
            type: 'upload',
            invoiceId: response.data.data[0].invoiceId,
          },
        });
      } else {
        console.log(response);
        alert('Unable to create invoice');
      }
    } catch (err) {
      alert(err);
    }
  };

  return (
    <>
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <Typography variant='h4'>Invoice Creation</Typography>

        <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />

        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize='small' />}
        >
          <Typography component={Link} to='/dashboard'>
            Dashboard
          </Typography>

          <Typography color='text.primary'>Invoice Creation</Typography>
        </Breadcrumbs>

        <Box sx={{ my: 5 }}>
          <DropzoneArea
            acceptedFiles={['.pdf', '.json']}
            fileObjects={files}
            onChange={(loadedFile) => {
              console.log('Currently loaded:', loadedFile);
              setFiles(loadedFile);
            }}
            filesLimit={5}
          />
        </Box>

        <Box textAlign='center'>
          <Button
            onClick={handleSubmit}
            variant='contained'
            startIcon={<FaFileUpload />}
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Generate Invoices from Uploaded Files
          </Button>
          {/* NOTE: Send to backend and create invoices */}
        </Box>

        <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
          OR
        </Typography>

        <Box textAlign='center'>
          <Button
            component={Link}
            to='/invoice-creation-GUI'
            variant='contained'
            startIcon={<BsPencilSquare style={{ marginRight: 2 }}/>}
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Create a New Invoice from a GUI Form
          </Button>
        </Box>
      </Container>
    </>
  );
}
