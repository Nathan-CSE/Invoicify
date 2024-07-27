import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useLocation } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import ReplayIcon from '@mui/icons-material/Replay';
import DownloadReport from '../../components/DownloadReport';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import { Paper, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

interface AssertionError {
  id: string;
  text: string;
  location: string;
}


export default function ValidationReport() {
  const location = useLocation();
  const { response, ruleSet } = location.state;

  const [currentReportIndex, setCurrentReportIndex] = React.useState(0);
  const validationReports = response.validationOutcome;

  const currentReport = validationReports[currentReportIndex];
  const isValid = currentReport.validated;
  const errorData = !isValid ? currentReport.data : null;
  const fileName = !isValid ? currentReport.data.filename : currentReport.data;

  const handlePrevious = () => {
    if (currentReportIndex > 0) {
      setCurrentReportIndex(currentReportIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentReportIndex < validationReports.length - 1) {
      setCurrentReportIndex(currentReportIndex + 1);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ marginTop: 11 }}>
      <Typography variant='h4'>Invoice Validation Report</Typography>
      <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />
      <Breadcrumbs aria-label='breadcrumb' separator={<NavigateNextIcon fontSize="small" />}>
        <Typography component={Link} to='/dashboard'>Dashboard</Typography>
        <Typography component={Link} to='/invoice-validation'>Invoice Validation</Typography>
        <Typography color='text.primary'>Invoice Validation Report</Typography>
      </Breadcrumbs>
      <Typography variant='h5' fontWeight='bold' textAlign='center' sx={{ my: 2 }}>
        {ruleSet} Validation Report(s)
      </Typography>

      {isValid ? (
        <Box display="flex" alignItems="center" justifyContent="center" sx={{ maxWidth: '40vh', border: 'solid 0.5px', borderRadius: 4, paddingX: 2, margin: '0 auto' }}>
          <Stack direction="row" spacing={2} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
            <CheckCircleIcon sx={{ color: 'green', fontSize: '3rem' }} />
            <Typography>The file {fileName} is valid.</Typography>
          </Stack>
        </Box>
      ) : (
        <>
          <Box display="flex" alignItems="center" justifyContent="center" sx={{ maxWidth: '40vh', border: 'solid 0.5px', borderRadius: 4, paddingX: 2, margin: '0 auto' }}>
            <Stack direction="row" spacing={2} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
              <CancelIcon sx={{ color: 'red', fontSize: '3rem' }} />
              <Typography>The file {fileName} is invalid. It contains {errorData.reports.firedAssertionErrorsCount} failed assertion(s), check individual reports for details.</Typography>
            </Stack>
          </Box>
          <Typography variant='h5' sx={{ mt: 4 }}>Errors</Typography>
          <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Assertion Rule</TableCell>
                  <TableCell>Error Message</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {errorData.reports.firedAssertionErrors.map((item: AssertionError, index: React.Key) => {
                  const errorText = `${item.text}\n\nLocation: ${item.location}`;
                  return (
                    <TableRow key={index}>
                      <TableCell>{item.id}</TableCell>
                      <TableCell style={{ whiteSpace: 'pre-wrap' }}>{errorText}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}

      <Stack direction="row" spacing={2} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
        <Button onClick={handlePrevious} disabled={currentReportIndex === 0} startIcon={<KeyboardArrowLeftIcon />}>Previous</Button>
        <Button onClick={handleNext} disabled={currentReportIndex === validationReports.length - 1} endIcon={<KeyboardArrowRightIcon />}>Next</Button>
      </Stack>

      <Stack direction="row" spacing={4} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
        {!isValid && <DownloadReport invoiceName={fileName} />}
        <Button component={Link} to='/invoice-validation' startIcon={<ReplayIcon />} variant='contained' sx={{ height: '50px', padding: '25px' }}>
          Validate Another Report
        </Button>
      </Stack>
    </Container>
  );
}
