import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { Link, useNavigate } from 'react-router-dom';
import LoadingDialog from '../../components/LoadingDialog';
import axios, { AxiosError } from 'axios';
import { DropzoneArea } from 'mui-file-dropzone';
import { BsPencilSquare } from 'react-icons/bs';
import { FaFileUpload } from 'react-icons/fa';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';
import ErrorModal from '../../components/ErrorModal';

function InvoiceCreation(props: { token: string }) {
  useAuth(props.token);
  const navigate = useNavigate();
  const [files, setFiles] = React.useState<File[]>([]);

  const [loading, setLoading] = React.useState(false);

  // Error handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

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
      setOpenError(true);
      setError('You must upload a valid file to create an invoice.');
      return;
    }

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
        navigate('/invoice-creation-confirmation', {
          state: {
            invoice: response.data,
            type: 'upload',
            invoiceId: response.data.data[0].invoiceId,
          },
        });
      } else {
        setOpenError(true);
        setError('Unable to create invoice');
      }
    } catch (error) {
      setLoading(false);
      const err = error as AxiosError<{ message: string }>;
      if (err.response) {
        setOpenError(true);
        setError(err.response.data.message);
      } else if (error instanceof Error) {
        setOpenError(true);
        setError(error.message);
      }
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
              setFiles(loadedFile);
            }}
            dropzoneText={'Upload an file: JSON, PDF'}
            filesLimit={10}
          />
        </Box>

        <Box textAlign='center'>
          <Button
            data-cy='generate-invoice'
            onClick={handleSubmit}
            variant='contained'
            startIcon={<FaFileUpload />}
            sx={{
              padding: '15px',
            }}
          >
            Generate Invoices from Uploaded Files
          </Button>
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
      {openError && (
        <ErrorModal open={openError} setOpen={setOpenError}>
          {error}
        </ErrorModal>
      )}
    </>
  );
}

export default InvoiceCreation;
