import {
  Box,
  Breadcrumbs,
  Button,
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
import { Link, useNavigate } from 'react-router-dom';
import ErrorModal from '../components/ErrorModal';
import { ReactComponent as InvoiceSvg } from '../assets/invoice.svg';
import { ReactComponent as InvoiceSettings } from '../assets/settings_mini.svg';
import SettingsMenu from '../components/SettingsMenu';
import FilterModal from '../components/FilterModal';
import PrintableInvoice from '../components/PrintableInvoice';

export default function InvoiceManagement(props: { token: string }) {
  const navigate = useNavigate();

  interface Details {
    id: number;
    name: string;
    completed_ubl: any;
    fields: any;
    rule: string;
    user_id: number;
    is_ready: boolean;
  }

  // const [details, setDetails] = React.useState<Details[]>([]);
  const [details, setDetails] = React.useState<Map<number, Details>>(new Map());

  const openSettings = () => () => {
    alert(1);
  };

  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  // All these related to the filter modal
  const [filterOpen, setFilterOpen] = React.useState(false);
  const [filterValue, setFilterValue] = React.useState('');

  const handleClickFilter = () => {
    setFilterOpen(true);
  };

  const handleCloseFilter = (value: string) => {
    setFilterValue(value);
    setFilterOpen(false);
  };

  const handleCancelFilter = () => {
    setFilterOpen(false);
  };

  const handleCardClick =
    (id: number) => (event: React.MouseEvent<HTMLButtonElement>) => {
      // alert(1);
      console.log(id);
      let cardDetails = details.get(id);
      console.log(cardDetails);
      let cardFields = cardDetails?.fields;
      navigate('/invoice-preview-history', {
        state: { fields: cardFields, name: cardDetails?.name },
      });
    };
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

        // Checks for the filter options
        // If the filter is not chosen it will default to id
        if (filterValue === 'status') {
          for (let d of Object.values(data)) {
            if (d.is_ready) {
              temp.push(d);
            }
          }
        } else {
          for (let d of Object.values(data)) {
            temp.push(d);
          }
        }

        // Lexiographically sort if the filter option is enabled
        if (filterValue === 'name') {
          temp = [...temp].sort((a, b) => a.name.localeCompare(b.name));
        }

        const initialMap = new Map<number, Details>();
        temp.forEach((detail) => {
          initialMap.set(detail.id, detail);
        });
        setDetails(initialMap);
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
    // Object.values(details).map((items
    return Array.from(details.values()).map((items) => (
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
          <SettingsMenu id={items.id} token={props.token}></SettingsMenu>
          <CardActionArea onClick={handleCardClick(items.id)}>
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
                    Status: Validated
                  </Typography>

                  {
                    // Vaulted till a later sprint
                    /* <Typography variant='subtitle1' gutterBottom>
                    Validated with {items.rule}
                  </Typography> */
                  }
                </>
              ) : (
                <>
                  <Typography variant='subtitle1' gutterBottom>
                    Status: Unvalidated
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
    setFilterValue('id');
    getDetails();
  }, []);

  // We need this because it seems like when we refresh the page
  // We lose the token so the data is not rendered again
  // The token will pop in and render and then will render the data again
  React.useEffect(() => {
    getDetails();
  }, [props.token]);

  React.useEffect(() => {
    getDetails();
  }, [filterValue]);

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
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            width: '100%',
            mb: 2,
          }}
        >
          <Typography variant='h4'>Invoice Management</Typography>
          <Button variant='contained' onClick={handleClickFilter}>
            FILTER
          </Button>
          <FilterModal
            open={filterOpen}
            onClose={handleCloseFilter}
            onCancel={handleCancelFilter}
          />
        </Box>
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
