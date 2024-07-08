import {
  Box,
  Breadcrumbs,
  Card,
  CardActionArea,
  CardContent,
  Divider,
  Grid,
} from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Typography from '@mui/material/Typography';
import * as React from 'react';
import axios, { AxiosError } from 'axios';
import { Link } from 'react-router-dom';
import ErrorModal from '../components/ErrorModal';
import { ReactComponent as InvoiceSvg } from '../assets/invoice.svg';
import { ReactComponent as InvoiceSettings } from '../assets/settings_mini.svg';
import { TempleBuddhist } from '@mui/icons-material';

export default function InvoiceManagement(props: { token: string }) {
  interface Fields {
    key: string;
  }

  interface Details {
    fields: Fields;
    id: number;
    is_ready: boolean;
    name: string;
    user_id: number;
  }

  const [details, setDetails] = React.useState<Details[]>([]);
  const openSettings = () => () => {
    alert(1);
  };

  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');
  // Just to fetch data on load
  const getDetails = async () => {
    try {
      const response = await axios.get(
        'http://localhost:5000/invoice/history',
        {
          headers: {
            Authorisation: `${props.token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      if (response.status === 200) {
        const data: Record<string, Details> = response.data;
        let temp: Details[] = [];
        for (let d of Object.values(data)) {
          temp.push(d);
        }
        setDetails(temp);
      } else {
        setOpenError(true);
        setError(response.data.message);
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        if (error.response) {
          if (error.response.status !== 403) {
            setOpenError(true);
            setError(error.response.data.message);
          }
        }
      } else if (error instanceof Error) {
        setOpenError(true);
        setError(error.message);
      }
    }
  };

  function generateInvoiceCards(): JSX.Element[] {
    return Object.values(details).map((items) => (
      <Grid key={items.id} item>
        <Card
          sx={{
            border: 1,
            borderRadius: '16px',
            width: '20rem',
            height: '24rem',
            alignContent: 'center',
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            textDecoration: 'none',
            position: 'relative',
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              zIndex: 1000,
              cursor: 'pointer',
              pl: 1,
              pt: 1,
            }}
            onClick={openSettings()}
          >
            <InvoiceSettings></InvoiceSettings>
          </Box>
          <CardActionArea>
            <CardContent
              sx={{
                mt: 2,
                height: '24rem',
              }}
            >
              <InvoiceSvg></InvoiceSvg>
              <Typography variant='h6' component='div'>
                {items.name}
              </Typography>

              {items.is_ready ? (
                <>
                  <Typography variant='subtitle1' gutterBottom>
                    Status: Verified
                  </Typography>
                </>
              ) : (
                <>
                  <Typography variant='subtitle1' gutterBottom>
                    Status: Unverified
                  </Typography>
                </>
              )}
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid>
    ));
  }
  React.useEffect(() => {
    getDetails();
  }, []);

  // We need this because it seems like when we refresh the page
  // We lose the token so the data is not rendered again
  // The token will pop in and render and then will render the data again
  React.useEffect(() => {
    getDetails();
  }, [props.token]);

  return (
    <>
      <Box
        sx={{
          mt: 15,
          mx: 5,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          width: '90%',
        }}
      >
        <Typography variant='h4'>Invoice Management</Typography>
        <Divider sx={{ borderColor: 'black', width: '100%' }} />
        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize='small' />}
          sx={{ mt: 1 }}
        >
          <Typography component={Link} to='/dashboard'>
            Dashboard
          </Typography>

          <Typography color='text.primary'>Invoice Management</Typography>
        </Breadcrumbs>
        <Grid
          container
          spacing={9}
          sx={{
            mt: 4,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          {generateInvoiceCards()}
        </Grid>
      </Box>

      <Box sx={{ mt: 10 }}>
        {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
      </Box>
    </>
  );
}
