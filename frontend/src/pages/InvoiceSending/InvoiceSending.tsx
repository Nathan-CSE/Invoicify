import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DropzoneArea } from "mui-file-dropzone";
import axios from 'axios';
import { TextField } from '@mui/material';
import { request } from 'http';
import MultipleSelect from '../../components/MultipleSelect';

export default function InvoiceSending(props: { token: string; }) {
  // console.log('user token: ', props.token);
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [invoices, setInvoices] = React.useState<string[]>([]);
  const [files, setFiles] = React.useState<File[] | null>([]);
  const [availableInvoices, setAvailableInvoices] = React.useState<any[]>([]);


  const handleChange = (event: SelectChangeEvent<string[]>) => {
    console.log('this is event.target: ', event.target);

    const { name, value } = event.target;

    setInvoices( typeof value === 'string' ? value.split(',') : value);

    if (event.target.value) {
      setFiles(null); // Clear file selection if an invoice is selected

    }

  };

  const handleFileChange = (loadedFiles: File[]) => {
    console.log('Currently loaded:', loadedFiles);
    if (loadedFiles.length > 0) {
      setFiles(loadedFiles);
      setInvoices([]); // Clear invoice selection if a file is uploaded
    } else {
      setFiles(null);
    }
  };

  const handleSubmit = async (event: { preventDefault: () => void; currentTarget: HTMLFormElement | undefined; }) => {
    event.preventDefault();

    if (files === null && invoices.length === 0) {
      alert("You must either upload a JSON/PDF file or select a UBL invoice to send.");
      return;
    }

    const formData = new FormData(event.currentTarget);
    const recipientEmail = formData.get("recipientEmail") || '';
    const invoiceId = formData.get("select-invoice") || '';

    console.log("recipient email: ", recipientEmail);
    console.log("invoice id: ", invoiceId);

    const requestData = new FormData();

    if (files) {
      files.forEach(item => {
        requestData.append("files", item);
      });
    } else {
      // requestData.append("target_email", recipientEmail);
      requestData.append("id", invoiceId);
    }
    
    requestData.append("target_email", recipientEmail);

    console.log('this is requestData: ', requestData);
    navigate('/invoice-sending-confirmation');

    try {
      // Placeholder until sending endpoint has been created
      var response;

      if (files) {
        // Placeholder until json/pdf send endpoint has been created
        response = await axios.post(`http://localhost:5000/invoice/uploadValidate`, requestData, {
          headers: {
            'Authorisation': `${props.token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
      } else {
        // console.log(`http://localhost:5000/invoice/send_ubl/${invoiceId}?target_email=${recipientEmail}`);
        // response = await axios.post(`http://localhost:5000/invoice/send_ubl/${invoiceId}?target_email=${recipientEmail}`, {
        //   headers: {
        //     'Authorisation': `${props.token}`,
        //   }
        // });

        response = await axios.post(`http://localhost:5000/invoice/send_ubl/${invoiceId}`, requestData, {
          headers: {
            'Authorisation': `${props.token}`,
          }
        });

      }
      
      if (response.status === 200) {
        console.log(response.data);
        navigate('/invoice-sending-confirmation');
        
      } else {
        console.log(response.data);
        navigate('/invoice-sending-confirmation');
        // alert("Unable to send invoice");
      }
    } catch (err) {
      // console.log(err);
      alert(err);
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
        const response = await axios.get('http://localhost:5000/invoice/history?is_ready=true', {
          headers: {
            'Authorisation': `${props.token}`,
          }
        });
        
        var allInvoices = [];
        
        if (response.status === 200) {
          for (let i = 0; i < response.data.length; i++) {
            var invoiceInfo = {
              name: response.data[i].name,
              invoiceId: response.data[i].id
            }
           
            allInvoices.push(invoiceInfo);
          } 
          console.log(response.data);
          setAvailableInvoices(allInvoices);
          // console.log("all invoices: ", allInvoices);
          // navigate('/invoice-creation-confirmation', { state: invoiceData });
        } else {
          console.log(response);
          alert("Unable to retrieve valid invoices");
        }
      } catch (err) {
        alert(err);
      }
    };
  
    fetchData();
  }, []);


  return (
    <>
     
      <Container maxWidth="lg" sx={{ marginTop: 11 }}>
        <Typography variant='h4'>
          Invoice Sending
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
            Invoice Sending
          </Typography>
        </Breadcrumbs>

        <form onSubmit={handleSubmit}>

          <Box sx={{ my: 5 }}>
            <DropzoneArea
              acceptedFiles={['.json', '.pdf']}
              fileObjects={files}
              onChange={handleFileChange}
              dropzoneText={'Upload an Invoice: JSON, PDF'}
              filesLimit={3}
            />
          </Box>

          <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
            OR
          </Typography>

          <MultipleSelect invoices={invoices} availableInvoices={availableInvoices} file={files} handleChange={handleChange} />

          <Box sx={{ minWidth: 120, mb: 5 }}>
            <FormControl variant="standard" fullWidth>
              <TextField
                margin="normal"
                required
                id="recipientEmail"
                label="Recipient Email"
                name="recipientEmail"
                variant="standard"
                sx={{ width: '100%' }}
              />
            </FormControl>
          </Box>

          <Box textAlign='center'>
            <Button
              type="submit"
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Continue
            </Button>
          </Box>
        </form>
      </Container>
      
    </>
  );
}