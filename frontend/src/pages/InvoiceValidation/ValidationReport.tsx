import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useLocation } from 'react-router-dom';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import ReplayIcon from '@mui/icons-material/Replay';
import DownloadReport from '../../components/DownloadReport';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import {
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';

interface AssertionError {
  id: string;
  text: string;
  location: string;
}

function ValidationReport(props: { token: string }) {
  useAuth(props.token);

  const location = useLocation();
  const { response, ruleSet } = location.state;

  const [currentReportIndex, setCurrentReportIndex] = React.useState(0);
  const validationReports = response.validationOutcome;

  const currentReport = validationReports[currentReportIndex];
  const isValid = currentReport.validated;
  const errorData = !isValid ? currentReport.data : null;
  const fileName = currentReport.invoiceName;

  const breadcrumbNav = {
    Dashboard: '/dashboard',
    'Invoice Validation': '/invoice-validation',
    'Invoice Validation Report': '/invoice-validation-report',
  };

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
    <Container maxWidth='lg' sx={{ marginTop: 11 }}>
      <PageHeader
        HeaderTitle={'Invoice Validation Report'}
        BreadcrumbDict={breadcrumbNav}
      />

      <div id='report-content'>
        <Typography
          variant='h5'
          fontWeight='bold'
          textAlign='center'
          sx={{ my: 2 }}
        >
          {ruleSet} Validation Report
        </Typography>
        {isValid ? (
          <Box
            display='flex'
            alignItems='center'
            justifyContent='center'
            sx={{
              maxWidth: '40vh',
              border: 'solid 0.5px',
              borderRadius: 4,
              paddingX: 2,
              margin: '0 auto',
            }}
          >
            <Stack
              direction='row'
              spacing={2}
              sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}
            >
              <CheckCircleIcon sx={{ color: 'green', fontSize: '3rem' }} />
              <Typography data-cy='validation-valid'>
                The file {fileName} is valid.
              </Typography>
            </Stack>
          </Box>
        ) : (
          <>
            <Box
              display='flex'
              alignItems='center'
              justifyContent='center'
              sx={{
                maxWidth: '40vh',
                border: 'solid 0.5px',
                borderRadius: 4,
                paddingX: 2,
                margin: '0 auto',
              }}
            >
              <Stack
                direction='row'
                spacing={2}
                sx={{
                  my: 4,
                  justifyContent: 'center',
                  alignItems: 'center',
                }}
              >
                <CancelIcon sx={{ color: 'red', fontSize: '3rem' }} />
                <Typography
                  data-cy='validation-invalid'
                  sx={{
                    maxWidth: 'calc(100% - 4rem)',
                    overflowWrap: 'break-word',
                    wordBreak: 'break-word',
                  }}
                >
                  The file <b>{fileName}</b> is invalid. It contains{' '}
                  {errorData.firedAssertionErrorsCount} failed assertion(s),
                  check individual reports for details.
                </Typography>
              </Stack>
            </Box>
            <Typography variant='h5' sx={{ mt: 4 }}>
              Errors
            </Typography>
            <TableContainer component={Paper} sx={{ mt: 2 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Assertion Rule</TableCell>
                    <TableCell>Error Message</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {errorData.firedAssertionErrors.map(
                    (item: AssertionError, index: React.Key) => {
                      const errorText = `${item.text}\n\nLocation: ${item.location}`;
                      return (
                        <TableRow key={index}>
                          <TableCell>{item.id}</TableCell>
                          <TableCell style={{ whiteSpace: 'pre-wrap' }}>
                            {errorText}
                          </TableCell>
                        </TableRow>
                      );
                    }
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </>
        )}
      </div>

      <Stack
        direction='row'
        spacing={2}
        sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}
      >
        <Button
          onClick={handlePrevious}
          disabled={currentReportIndex === 0}
          startIcon={<KeyboardArrowLeftIcon />}
        >
          Previous
        </Button>
        <Typography>
          {currentReportIndex + 1} / {validationReports.length}
        </Typography>
        <Button
          onClick={handleNext}
          disabled={currentReportIndex === validationReports.length - 1}
          endIcon={<KeyboardArrowRightIcon />}
        >
          Next
        </Button>
      </Stack>

      <Divider
        sx={{
          my: 5,
          borderBottomWidth: 2,
        }}
      />

      <Stack
        direction='row'
        spacing={4}
        sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}
      >
        {!isValid && (
          <DownloadReport
            invoiceName={fileName}
            currentReport={currentReport}
            inputDiv={document.getElementById('report-content')}
          />
        )}
        <Button
          component={Link}
          to='/invoice-validation'
          startIcon={<ReplayIcon />}
          variant='contained'
          sx={{ padding: '15px' }}
        >
          Validate Another Report
        </Button>
      </Stack>
    </Container>
  );
}

export default ValidationReport;
