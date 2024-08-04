import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useLocation } from 'react-router-dom';
import { Card, CardContent, Grid } from '@mui/material';
import { ReactComponent as InvoiceSvg } from '../../assets/invoice.svg';
import ReplayIcon from '@mui/icons-material/Replay';
import SendIcon from '@mui/icons-material/Send';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';

function InvoiceSending(props: { token: string }) {
  useAuth(props.token);
  const breadcrumbNav = {
    Dashboard: '/dashboard',
    'Invoice Sending': '/invoice-sending',
    'Invoice Sending Confirmation': '/invoice-sending-confirmation',
  };

  const { invoiceNames, recipientEmail } = useLocation().state;

  return (
    <>
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <PageHeader
          HeaderTitle={'Invoice Sending Confirmation'}
          BreadcrumbDict={breadcrumbNav}
        />

        <Box textAlign='center' sx={{ mt: 5 }}>
          <Typography data-cy='send-confirmation' variant='h4' sx={{ mb: 1 }}>
            Your file(s) have been sent!
          </Typography>
          <Typography variant='h6'>
            <SendIcon style={{ marginBottom: -5, marginRight: 10 }} />
            {recipientEmail}
          </Typography>
        </Box>

        <Grid
          container
          spacing={4}
          sx={{ mt: 1, mb: 5 }}
          justifyContent='center'
        >
          {invoiceNames.map((invoice: string, index: number) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                sx={{
                  border: 1,
                  borderRadius: '16px',
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                }}
              >
                <CardContent>
                  <InvoiceSvg
                    style={{
                      width: '100px',
                      height: '100px',
                      marginBottom: '16px',
                    }}
                  />
                  <Typography variant='h6' component='div'>
                    {invoice}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Divider
          sx={{
            mt: 6,
            mb: 4,
            borderBottomWidth: 2,
          }}
        />

        <Grid container justifyContent='center' spacing={6}>
          <Grid item>
            <Button
              component={Link}
              to='/invoice-sending'
              startIcon={<ReplayIcon />}
              variant='contained'
              sx={{
                padding: '15px',
              }}
            >
              Send another Invoice
            </Button>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}

export default InvoiceSending;
