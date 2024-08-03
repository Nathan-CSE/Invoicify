import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useLocation, useNavigate } from 'react-router-dom';
import FormControl from '@mui/material/FormControl';
import { SelectChangeEvent } from '@mui/material/Select';
import { DropzoneArea } from 'mui-file-dropzone';
import axios from 'axios';
import { TextField } from '@mui/material';
import MultipleSelect from '../../components/MultipleSelect';
import SendIcon from '@mui/icons-material/Send';
import LoadingDialog from '../../components/LoadingDialog';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';
import ErrorModal from '../../components/ErrorModal';

export default function InvoiceSending(props: { token: string }) {
  // console.log('user token: ', props.token);
  useAuth(props.token);
  const navigate = useNavigate();
  const [loading, setLoading] = React.useState(false);
  const [loadingMsg, setLoadingMsg] = React.useState<string>('');
  const [invoices, setInvoices] = React.useState<string[]>([]);
  const [files, setFiles] = React.useState<File[] | null>([]);
  const [availableInvoices, setAvailableInvoices] = React.useState<any[]>([]);
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  const breadcrumbNav = {
    'Dashboard': '/dashboard',
    'Invoice Sending': '/invoice-sending'
  }

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
    console.log('this is event.target: ', event.target);

    const { name, value } = event.target;

    setInvoices( typeof value === 'string' ? value.split(',') : value);

    console.log("this is invoices: ", invoices);

    if (event.target.value) {
      setFiles(null); // Clear file selection if an invoice is selected

    }
  };

  const handleFileChange = (loadedFiles: File[]) => {
    console.log('Currently loaded:', loadedFiles);
    if (loadedFiles.length > 0) {
      console.log("these are the files that have currently been loaded: ", loadedFiles);
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
      setError('You must either upload a JSON/PDF file or select a UBL invoice to send.');
      return;
    }

    const formData = new FormData(event.currentTarget);
    const recipientEmail = formData.get('recipientEmail') as string || '';

    if (!recipientEmail.includes('@')) {
      setOpenError(true);
      setError('Please provide a valid email address');
      return;
    }

    console.log('recipient email: ', recipientEmail);
    // console.log('invoice id: ', invoiceId);

    const requestData = new FormData();
    let invoiceNames: string[] = [];

    if (files) {
      files.forEach(item => {
        requestData.append("files", item);
        invoiceNames.push(item.name);
      });
    } else {
      invoices.forEach(item => {
        // requestData.append("id", item);

        // console.log("available invoices: ", availableInvoices);
        // This sends the name of the invoices across
        const specificInvoice = availableInvoices.find(invoice => invoice.invoiceId === Number(item));
        invoiceNames.push(specificInvoice.name);
        
      })
    }
    requestData.append("target_email", recipientEmail);

    console.log("These are the invoice names2: ", invoiceNames);

    console.log('this is requestData: ', requestData);

    // navigate('/invoice-sending-confirmation', { state: { invoiceNames: invoiceNames, recipientEmail: recipientEmail } });

    // FIXME: Commented this out until the endpoint supports multiple send
    try {
      // Placeholder until sending endpoint has been created
      var response;
      
      setLoading(true);

      if (files) {
        // Placeholder until json/pdf send endpoint has been created
        setLoadingMsg('Sending file(s)...');
        response = await axios.post(`http://localhost:5000/invoice/send_ubl`, requestData, {
          headers: {
            Authorisation: `${props.token}`,
            'Content-Type': 'multipart/form-data',
          },
        });
      } else {
        setLoadingMsg('Sending invoice(s)...');
        response = await axios.post(`http://localhost:5000/invoice/send_ubl?xml_id=${invoices}`, requestData, {
          headers: {
            Authorisation: `${props.token}`,
          },
        });
      }

      setLoading(false);
      if (response.status === 200) {
        console.log(response.data);
        navigate('/invoice-sending-confirmation', { state: { invoiceNames: invoiceNames, recipientEmail: recipientEmail } });
      } else {
        // console.log(response.data);
        // navigate('/invoice-sending-confirmation', { state: { invoiceNames: invoiceNames } });
        setOpenError(true);
        setError('Unable to send invoice');
      }
    } catch (err) {
      setLoading(false);
      // FIXME:
      // Here temporarily until endpoint has been created for bulk sending
      setOpenError(true);
      setError('Unable to send invoice');

    }
  };

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        // placeholder until everything else is merged
        // const response = await axios.get('http://localhost:5000/invoice/history?is_ready=true', {
        //   headers: {
        //     'Authorisation': `${props.token}`,
        //   }
        // });
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
          // console.log(response.data);
          setAvailableInvoices(allInvoices);
          // console.log("all invoices: ", allInvoices);
          // navigate('/invoice-creation-confirmation', { state: invoiceData });
        } else {
          console.log(response);
          alert('Unable to retrieve valid invoices');
        }
      } catch (err) {
        
        alert(err);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <LoadingDialog open={loading} message={loadingMsg} />
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>

        <PageHeader HeaderTitle={'Invoice Sending'} BreadcrumbDict={breadcrumbNav} />

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

          <MultipleSelect invoices={invoices} availableInvoices={availableInvoices} file={files} handleChange={handleChange} />

          <Box sx={{ minWidth: 120, mb: 5 }}>
            <FormControl variant='standard' fullWidth>
              <TextField
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
