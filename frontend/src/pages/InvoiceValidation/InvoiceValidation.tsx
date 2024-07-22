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
import { Checkbox } from '@mui/material';
import Chip from '@mui/material/Chip';
import MultipleSelect from '../../components/MultipleSelect';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

export default function InvoiceValidation(props: { token: string; }) {
  console.log('user token: ', props.token);
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  // const [invoice, setInvoice] = React.useState('');
  const [invoices, setInvoices] = React.useState<string[]>([]);
  const [ruleSet, setRuleSet] = React.useState<string[]>([]);
  const [files, setFiles] = React.useState<File[] | null>([]);
  const [availableInvoices, setAvailableInvoices] = React.useState<{ invoiceId: number; name: string; }[]>([]);

  const handleChange = (event: SelectChangeEvent<string[]>) => {
    console.log('this is event.target: ', event.target);
    const { name, value } = event.target;

    if (name === 'rule-set') {
      setRuleSet(value as string[]);
    } else {
      setInvoices( typeof value === 'string' ? value.split(',') : value);
    }

  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    if (files === null && invoices.length === 0) {
      alert("You must either upload or select an xml file to create an invoice.");
      return;
    }

    const formData = new FormData();

    if (files) {
      files.forEach(item => {
        formData.append("files", item);
      });
    }

    console.log('this is formData: ', formData);
    console.log('this is the rule set: ', ruleSet);
    console.log('this is invoiceId: ', invoices);

    try {
      // Placeholder until backend endpoint has been created
      var response;

      if (files) {
        response = await axios.post(`http://localhost:5000/invoice/uploadValidate?rules=${ruleSet}`, formData, {
          headers: {
            'Authorisation': `${props.token}`,
            'Content-Type': 'multipart/form-data'
          }
        });
      } else {
        response = await axios.get(`http://localhost:5000/invoice/validate/${invoices}?rules=${ruleSet}`, {
          headers: {
            'Authorisation': `${props.token}`,
          }
        });

      }

      
      if (response.status === 200) {
        console.log(response.data);
        // navigate('/invoice-validation-report-valid', { state: { fileName: files?.name, ruleSet: ruleSet } });
        
      } else {
        console.log(response.data);
        navigate('/invoice-validation-report-invalid', { state: { response: response.data, ruleSet: ruleSet } });
      }
    } catch (err) {
      console.error(err);
      alert("Unable to validate invoice. Make sure the XML file itself is complete and has no syntactic errors.");
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

  React.useEffect(() => {
    const fetchData = async () => {
      try {

        const response = await axios.get('http://localhost:5000/invoice/history?is_ready=false', {
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
          Invoice Validation
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
            Invoice Validation
          </Typography>
        </Breadcrumbs>

        <form onSubmit={handleSubmit}>
          <Box sx={{ my: 5 }}>
            <DropzoneArea
              acceptedFiles={['.xml']}
              fileObjects={files}
              onChange={handleFileChange}
              dropzoneText={'Upload a UBL2.1 XML Invoice File'}
              filesLimit={5}
            />
          </Box>

          <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
            OR
          </Typography>

          <MultipleSelect invoices={invoices} availableInvoices={availableInvoices} file={files} handleChange={handleChange} />

          <Box sx={{ minWidth: 120, my: 3 }}>
            <FormControl variant="standard" fullWidth>
              <InputLabel id="select-rule-set">Rule Set</InputLabel>
              <Select
                labelId="select-rule-set"
                id="rule-set"
                name='rule-set'
                value={ruleSet}
                label="Rule Set"
                onChange={handleChange}
                required
              >
                <MenuItem value={'AUNZ_PEPPOL_1_0_10'}>AU-NZ PEPPOL-1.0.10</MenuItem>
                <MenuItem value={'AUNZ_PEPPOL_SB_1_0_10'}>AU-NZ PEPPOL-SB-1.0.10</MenuItem>
                <MenuItem value={'AUNZ_UBL_1_0_10'}>AU-NZ UBL-1.0.10</MenuItem>
                <MenuItem value={'FR_EN16931_CII_1_3_11'}>FR-EN16931-CII-1.3.11</MenuItem>
                <MenuItem value={'FR_EN16931_UBL_1_3_11'}>FR-EN16931-UBL-1.3.11</MenuItem>
                <MenuItem value={'FR_EN16931_UBL_1_3_11'}>FR-EN16931-UBL-1.3.11</MenuItem>
                <MenuItem value={'RO_RO16931_UBL_1_0_8_EN16931'}>RO-RO16931-UBL-1.0.8-EN16931</MenuItem>
                <MenuItem value={'RO_RO16931_UBL_1_0_8_CIUS_RO'}>RO-RO16931-UBL-1.0.8-CIUS-RO</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Box textAlign='center'>
            <Button
              type='submit'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
              endIcon={<ArrowForwardIcon />}
            >
              Continue
            </Button>
          </Box>
        </form>
      </Container>
      
    </>
  );
}