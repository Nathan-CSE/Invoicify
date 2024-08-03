import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Link, useNavigate } from 'react-router-dom';
import LoadingDialog from '../../components/LoadingDialog';
import axios from 'axios';
import { DropzoneArea } from 'mui-file-dropzone';
import { BsPencilSquare } from 'react-icons/bs';
import { FaFileUpload } from 'react-icons/fa';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';

export default function InvoiceCreation(props: { token: string }) {
  useAuth(props.token);
  const navigate = useNavigate();
  const [files, setFiles] = React.useState<File[]>([]);

  const [loading, setLoading] = React.useState(false);

  const breadcrumbNav = {
    Dashboard: '/dashboard',
    'Invoice Creation': '/invoice-creation',
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    const formData = new FormData();

    if (files.length > 0) {
      files.forEach((item) => {
        formData.append('files', item);
      });
    } else {
      alert('You must upload a valid file to create an invoice.');
      return;
    }

    // console.log('file to be sent: ', file);
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:5000/invoice/uploadCreate',
        formData,
        {
          headers: {
            Authorisation: `${props.token}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setLoading(false);
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
      setLoading(false);
      alert(err);
    }
  };

  return (
    <>
      <LoadingDialog open={loading} message='Creating invoice(s)...' />
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <PageHeader
          HeaderTitle={'Invoice Creation'}
          BreadcrumbDict={breadcrumbNav}
        />

        <Box sx={{ my: 5 }}>
          <DropzoneArea
            acceptedFiles={['.pdf', '.json']}
            fileObjects={files}
            onChange={(loadedFile) => {
              console.log('Currently loaded:', loadedFile);
              setFiles(loadedFile);
            }}
            dropzoneText={'Upload an file: JSON, PDF'}
            filesLimit={10}
          />
        </Box>

        <Box textAlign='center'>
          <Button
            onClick={handleSubmit}
            variant='contained'
            startIcon={<FaFileUpload />}
            sx={{
              padding: '15px',
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
            data-cy='create-gui'
            component={Link}
            to='/invoice-creation-GUI'
            variant='contained'
            startIcon={<BsPencilSquare style={{ marginRight: 2 }} />}
            sx={{
              padding: '15px',
            }}
          >
            Create a New Invoice from a GUI Form
          </Button>
        </Box>
      </Container>
    </>
  );
}
