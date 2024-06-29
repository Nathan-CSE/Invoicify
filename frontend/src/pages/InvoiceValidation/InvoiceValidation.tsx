import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import FileUpload from '../../components/FileUpload';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

export default function InvoiceValidation() {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const [invoice, setInvoice] = React.useState('');
  const [ruleSet, setRuleSet] = React.useState('');


  const handleChange = (event: SelectChangeEvent) => {
    console.log('this is event.target: ', event.target);

    if (event.target.name === 'rule-set') {
      setRuleSet(event.target.value);
    } else {
      setInvoice(event.target.value);
    }

    setInvoice(event.target.value);
  };


  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    const username = data.get('username') as string;
    const password = data.get('password') as string;
    
    if (username.length === 0 || password.length === 0) {
      alert('Fill out all required fields');
    } else {
      try {
        // send to backend
      } catch (err) {
        if (err instanceof Error) {
          alert(err.message);
        }
      }
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
          <FileUpload />
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
              <MenuItem value={10}>ANZ-Invoice</MenuItem>
              <MenuItem value={10}>ANZ-Invoice</MenuItem>
              <MenuItem value={10}>ANZ-Invoice</MenuItem>
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
              <MenuItem value={10}>AU-NZ PEPPOL 1.0.10</MenuItem>
            </Select>
          </FormControl>
        </Box>

        <Box textAlign='center'>
          <Button
            component={Link}
            to='/invoice-validation-report'
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