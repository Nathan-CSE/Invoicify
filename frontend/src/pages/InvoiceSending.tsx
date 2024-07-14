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

export default function InvoiceSending(props: { token: string; }) {
  console.log('user token: ', props.token);
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [invoice, setInvoice] = React.useState('');
  const [file, setFile] = React.useState<File | null>(null);
  const [email, setEmail] = React.useState('');
  const [showOverlay, setShowOverlay] = React.useState(false);

  const handleChange = (event: SelectChangeEvent) => {
    console.log('this is event.target: ', event.target);

    setInvoice(event.target.value);

    if (event.target.value) {
      setFile(null); // Clear file selection if an invoice is selected

    } else {
      setShowOverlay(false);
    }

  };

  const handleFileChange = (loadedFiles: File[]) => {
    console.log('Currently loaded:', loadedFiles);
    if (loadedFiles.length > 0) {
      setFile(loadedFiles[0]);
      setInvoice(''); // Clear invoice selection if a file is uploaded
      setShowOverlay(false);
    } else {
      setFile(null);
    }
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    const formData = new FormData();

    if (file) {
      formData.append("files", file);
    }

    if (invoice) {
      formData.append("invoice", invoice);
    }

    formData.append("email", email);

    console.log('this is formData: ', formData);

    try {
      // Placeholder until sending endpoint has been created
      const response = await axios.post(`http://localhost:5000/invoice/uploadValidate`, formData, {
        headers: {
          'Authorisation': `${props.token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      if (response.status === 200) {
        console.log(response.data);
        // navigate('/invoice-validation-report-valid', { state: { fileName: file?.name, ruleSet: ruleSet } });
        
      } else {
        console.log(response.data);
        // navigate('/invoice-validation-report-invalid', { state: { response: response.data, ruleSet: ruleSet } });
        // alert("Unable to create invoice");
      }
    } catch (err) {
      // console.log(err);
      alert(err);
    }

  };

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

        <Box sx={{ my: 5 }}>
          <DropzoneArea
            acceptedFiles={['.json', '.pdf']}
            fileObjects={file}
            onChange={handleFileChange}
            dropzoneText={'Upload an Invoice: JSON, PDF'}
            filesLimit={1}
          />
        </Box>

        <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
          OR
        </Typography>

        <Box sx={{ minWidth: 120 }}>
          <FormControl variant="standard" fullWidth>
            <InputLabel id="select-invoice-label">Select Invoice</InputLabel>
            <Select
              labelId="select-invoice-label"
              id="select-invoice"
              name='select-invoice'
              value={invoice}
              label="Select Invoice"
              onChange={handleChange}
              disabled={Boolean(file)}
            >
              <MenuItem value={10}>Invoice 1</MenuItem>
              <MenuItem value={11}>Invoice 2</MenuItem>
              <MenuItem value={12}>Invoice 3</MenuItem>
            </Select>
          </FormControl>
        </Box>

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
              onChange={(e) => setEmail(e.target.value)}
            />
          </FormControl>
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
            Continue
          </Button>
        </Box>
      </Container>
      
    </>
  );
}