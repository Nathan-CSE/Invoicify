import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useLocation, useNavigate } from 'react-router-dom';
import FormControl from '@mui/material/FormControl';
import { SelectChangeEvent } from '@mui/material/Select';
import { DropzoneArea } from 'mui-file-dropzone';
import axios, { AxiosError } from 'axios';
import { TextField } from '@mui/material';
import MultipleSelect from '../../components/MultipleSelect';
import SendIcon from '@mui/icons-material/Send';
import LoadingDialog from '../../components/LoadingDialog';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';
import ErrorModal from '../../components/ErrorModal';

function InvoiceSending(props: { token: string }) {
  useAuth(props.token);
  const navigate = useNavigate();
  const [loading, setLoading] = React.useState(false);
  const [loadingMsg, setLoadingMsg] = React.useState<string>('');
  const [invoices, setInvoices] = React.useState<string[]>([]);
  const [files, setFiles] = React.useState<File[] | null>([]);
  const [availableInvoices, setAvailableInvoices] = React.useState<any[]>([]);

  // Error handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  const breadcrumbNav = {
    Dashboard: '/dashboard',
    'Invoice Sending': '/invoice-sending',
  };

  // How we preload data from another page
  const location = useLocation();
  React.useEffect(() => {
    // Checks if we have some props from another page otherwise it will be null
    if (location && location.state) {
      // Type cast id to string, since allInvoices contains a list of ID strings
      const id: string = location.state.cardID.toString();
      setInvoices([id]);
    }
  }, []);

  const handleChange = (event: SelectChangeEvent<string[]>) => {
    const { name, value } = event.target;

    setInvoices(typeof value === 'string' ? value.split(',') : value);

    if (event.target.value) {
      setFiles(null); // Clear file selection if an invoice is selected
    }
  };

  const handleFileChange = (loadedFiles: File[]) => {
    if (loadedFiles.length > 0) {
      setFiles(loadedFiles);
      setInvoices([]); // Clear invoice selection if a file is uploaded
    } else {
      setFiles(null);
    }
  };

  const handleSubmit = async (event: {
    preventDefault: () => void;
    currentTarget: HTMLFormElement | undefined;
  }) => {
    event.preventDefault();

    if (files === null && invoices.length === 0) {
      setOpenError(true);
      setError(
        'You must either upload a JSON/PDF file or select a UBL invoice to send.'
      );
      return;
    }

    const formData = new FormData(event.currentTarget);
    const recipientEmail = (formData.get('recipientEmail') as string) || '';

    if (!recipientEmail.includes('@')) {
      setOpenError(true);
      setError('Please provide a valid email address');
      return;
    }

    const requestData = new FormData();
    let invoiceNames: string[] = [];

    if (files) {
      files.forEach((item) => {
        requestData.append('files', item);
        invoiceNames.push(item.name);
      });
    } else {
      invoices.forEach((item) => {
        // This sends the name of the invoices across
        const specificInvoice = availableInvoices.find(
          (invoice) => invoice.invoiceId === Number(item)
        );
        invoiceNames.push(specificInvoice.name);
      });
    }
    requestData.append('target_email', recipientEmail);

    try {
      var response;

      setLoading(true);

      if (files) {
        setLoadingMsg('Sending file(s)...');
        response = await axios.post(
          `http://localhost:5000/invoice/send_ubl`,
          requestData,
          {
            headers: {
              Authorisation: `${props.token}`,
              'Content-Type': 'multipart/form-data',
            },
          }
        );
      } else {
        setLoadingMsg('Sending invoice(s)...');
        response = await axios.post(
          `http://localhost:5000/invoice/send_ubl?xml_id=${invoices}`,
          requestData,
          {
            headers: {
              Authorisation: `${props.token}`,
            },
          }
        );
      }

      setLoading(false);
      if (response.status === 200) {
        navigate('/invoice-sending-confirmation', {
          state: { invoiceNames: invoiceNames, recipientEmail: recipientEmail },
        });
      } else {
        setOpenError(true);
        setError('Unable to send invoice');
      }
    } catch (err) {
      setLoading(false);
      setOpenError(true);
      setError('Unable to send invoice');
    }
  };

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          'http://localhost:5000/invoice/history?is_ready=true',
          {
            headers: {
              Authorisation: `${props.token}`,
            },
          }
        );

        var allInvoices = [];

        if (response.status === 200) {
          for (let i = 0; i < response.data.length; i++) {
            var invoiceInfo = {
              name: response.data[i].name,
              invoiceId: response.data[i].id,
            };

            allInvoices.push(invoiceInfo);
          }

          setAvailableInvoices(allInvoices);
        } else {
          setOpenError(true);
          setError('Unable to retrieve valid invoices');
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

    fetchData();
  }, []);

  return (
    <>
      <LoadingDialog open={loading} message={loadingMsg} />
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <PageHeader
          HeaderTitle={'Invoice Sending'}
          BreadcrumbDict={breadcrumbNav}
        />

        <form onSubmit={handleSubmit}>
          <Box sx={{ my: 5 }}>
            <DropzoneArea
              acceptedFiles={['.json', '.pdf']}
              fileObjects={files}
              onChange={handleFileChange}
              dropzoneText={'Upload an Invoice: JSON, PDF'}
              filesLimit={10}
            />
          </Box>

          <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
            OR
          </Typography>

          <MultipleSelect
            invoices={invoices}
            availableInvoices={availableInvoices}
            file={files}
            handleChange={handleChange}
          />

          <Box sx={{ minWidth: 120, mb: 5 }}>
            <FormControl variant='standard' fullWidth>
              <TextField
                data-cy='send-email'
                margin='normal'
                required
                id='recipientEmail'
                label='Recipient Email'
                name='recipientEmail'
                variant='standard'
                sx={{ width: '100%' }}
              />
            </FormControl>
          </Box>

          <Box textAlign='center'>
            <Button
              data-cy='send-submit'
              type='submit'
              variant='contained'
              startIcon={<SendIcon style={{ marginTop: 2 }} />}
              sx={{
                padding: '15px',
              }}
            >
              Send Invoice(s)
            </Button>
          </Box>
        </form>
      </Container>
      {openError && (
        <ErrorModal open={openError} setOpen={setOpenError}>
          {error}
        </ErrorModal>
      )}
    </>
  );
}

export default InvoiceSending;
