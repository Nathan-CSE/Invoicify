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

export default function InvoiceValidation(props: { token: string; }) {
  console.log('user token: ', props.token);
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [invoice, setInvoice] = React.useState('');
  const [ruleSet, setRuleSet] = React.useState('');
  const [file, setFile] = React.useState<File>();

  const handleChange = (event: SelectChangeEvent) => {
    console.log('this is event.target: ', event.target);

    if (event.target.name === 'rule-set') {
      setRuleSet(event.target.value);
    } else {
      setInvoice(event.target.value);
    }

    setInvoice(event.target.value);
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    const formData = new FormData();

    if (file) {
      formData.append("files", file);
    }

    console.log('this is formData: ', formData);
    console.log('this is the rule set: ', ruleSet);

    try {
      // Placeholder until backend endpoint has been created
      const response = await axios.post(`http://localhost:5000/invoice/validate?rules=${ruleSet}`, formData, {
        headers: {
          'Authorisation': `${props.token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      if (response.status === 200) {
        console.log(response.data);
        // navigate('/invoice-validation-report-valid');
        navigate('/invoice-validation-report-invalid');

      } else if (response.status === 400) {
        console.log(response);
        alert("Invoice error");
      } else {
        console.log(response);
        alert("Unable to create invoice");
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

        <Box sx={{ my: 5 }}>
          <DropzoneArea
            acceptedFiles={['.xml']}
            fileObjects={file}
            onChange={(loadedFile) => {
              console.log('Currently loaded:', loadedFile)
              setFile(loadedFile[0]);
            }}
            dropzoneText={'Upload a UBL2.1 XML Invoice File'}
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
            >
              <MenuItem value={10}>Invoice 1</MenuItem>
              <MenuItem value={11}>Invoice 2</MenuItem>
              <MenuItem value={12}>Invoice 3</MenuItem>
            </Select>
          </FormControl>
        </Box>

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