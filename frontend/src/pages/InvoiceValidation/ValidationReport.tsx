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
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import DownloadReport from '../../components/DownloadReport';
import { Paper, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

interface AssertionError {
  id: string;
  text: string;
  location: string;
}

export default function ValidationReport() {
  const stateData = useLocation().state;

  var isValid = true;
  var fileName = '';
  var ruleSet = '';
  var errorData;

  // Check if state contains a response, indicating an invalid invoice
  if (stateData && stateData.response) {
    isValid = false;
    // Extract data for invalid invoice
    errorData = stateData.response;
    fileName = errorData.filename;
    ruleSet = stateData.ruleSet;
    console.log("this is ruleSet: ", ruleSet);
  } else if (stateData) {
    // Extract data for valid invoice
    fileName = stateData.fileName;
    ruleSet = stateData.ruleSet;
  }

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

        {isValid ? (
          <>
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
          </>
        ) : (
          <>
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
                <CancelIcon sx={{ color: 'red', fontSize: '3rem' }} />
                <Typography>
                  The file {fileName} is invalid. It contains {errorData.reports.firedAssertionErrorsCount} failed assertion(s),
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

        <Stack direction="row" spacing={4} sx={{ my: 4, justifyContent: 'center', alignItems: 'center' }}>
          {!isValid ? (
            <DownloadReport invoiceName={fileName} />
          ) : null}
          <Button
            component={Link}
            to='/invoice-validation'
            startIcon={<RestartAltIcon />}
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
