import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DropzoneArea } from "mui-file-dropzone";
import axios from 'axios';
import { Card, CardActionArea, CardContent, Grid, TextField } from '@mui/material';
import { ReactComponent as InvoiceSvg } from '../../assets/invoice.svg';


export default function InvoiceSending(props: { token: string; }) {
  console.log('user token: ', props.token);
  console.log("location state: ", useLocation().state);
  const { invoiceNames } = useLocation().state;

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

          <Typography
            component={Link}
            to='/invoice-sending'
          >
            Invoice Sending
          </Typography>

          <Typography color='text.primary'>
            Invoice Sending Confirmation
          </Typography>
        </Breadcrumbs>

        <Box
          sx={{
            my: 10,
            padding: 5,
            height: '25vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            border: 'solid 0.5px',
            borderRadius: 4
          }}
        >
          <Box sx={{ mt: 1 }}>
            <Typography textAlign='center'>
              File sent successfully!
            </Typography>
          </Box>
        
        </Box>

        <Grid container spacing={4} sx={{ my: 5 }}>
          {invoiceNames.map((invoice: any) => (
            <Grid item xs={12} sm={6} md={4} key={invoice.invoiceId}>
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
                <CardActionArea>
                  <CardContent>
                    <InvoiceSvg style={{ width: '100px', height: '100px', marginBottom: '16px' }} />
                    <Typography variant='h6' component='div'>
                      {invoice.filename}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Grid container justifyContent="center" spacing={6}>
          <Grid item>
            <Button
              component={Link}
              to='/dashboard'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
              }}
            >
              Back to Dashboard
            </Button>
          </Grid>

          <Grid item>
            <Button
              component={Link}
              to='/invoice-sending'
              variant='contained'
              sx={{
                height: '50px',
                padding: '25px',
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