import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import FileUpload from '../../components/FileUpload';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { Paper, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

export default function InvoiceValidationReport() {
  const navigate = useNavigate();
  const fileName = useLocation().state.fileName;
  const ruleSet = useLocation().state.ruleSet;

  return (
    <>
     
      <Container maxWidth="lg" sx={{ marginTop: 11 }}>
        <Typography variant='h4'>
          Invoice Validation Report
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

          <Typography
            component={Link}
            to='/invoice-validation'
          >
            Invoice Validation
          </Typography>

          <Typography color='text.primary'>
            Invoice Validation Report
          </Typography>
        </Breadcrumbs>

        <Typography variant='h5' fontWeight='bold' textAlign='center' sx={{ my: 2 }}>
          {ruleSet} Validation Report
        </Typography>

        <Box
          display="flex"
          alignItems="center"
          justifyContent="center" 
          sx={{ 
            maxWidth: '40vh',
            border: 'solid 0.5px',
            borderRadius: 4, 
            paddingX: 2,
            margin: '0 auto'
          }}
        >
          <Stack direction="row" spacing={2} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
            <CheckCircleIcon sx={{ color: 'green', fontSize: '3rem' }} />
            <Typography>
              The file {fileName} is valid.
            </Typography>
          </Stack>
        </Box>
       
        <Stack direction="row" spacing={4} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
          <Button
            component={Link}
            to='/invoice-validation-report'
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Download Report
          </Button>

          <Button
            component={Link}
            to='/invoice-validation'
            variant='contained'
            sx={{
              height: '50px',
              padding: '25px',
            }}
          >
            Validate Another Report
          </Button>
        </Stack>

      </Container>
      
    </>
  );
}