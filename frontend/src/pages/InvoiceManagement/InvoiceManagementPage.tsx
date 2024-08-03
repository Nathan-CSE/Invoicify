import {
  Box,
  Breadcrumbs,
  Button,
  Card,
  CardActionArea,
  CardContent,
  Container,
  Divider,
  Grid,
  Stack,
} from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Typography from '@mui/material/Typography';
import * as React from 'react';
import axios, { AxiosError } from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import ErrorModal from '../../components/ErrorModal';
import { ReactComponent as InvoiceSvg } from '../../assets/invoice.svg';
import SettingsMenu from '../../components/SettingsMenu';
import FilterModal from '../../components/FilterModal';
import FilterListIcon from '@mui/icons-material/FilterList';
import LoadingDialog from '../../components/LoadingDialog';
import ReceiptIcon from '@mui/icons-material/Receipt';
import TagIcon from '@mui/icons-material/Tag';
import CancelIcon from '@mui/icons-material/Cancel';
import RuleIcon from '@mui/icons-material/Rule';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import EditIcon from '@mui/icons-material/Edit';

export default function InvoiceManagement(props: { token: string }) {
  // useAuth(props.token);

  const navigate = useNavigate();
  const [loading, setLoading] = React.useState(false);

  interface Details {
    id: number;
    name: string;
    completed_ubl: any;
    fields: any;
    rule: string;
    user_id: number;
    is_ready: boolean;
    is_gui: boolean;
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
      // console.log(id);
      let cardDetails = details.get(id);
      console.log(cardDetails);
      console.log(details);
      let cardFields = cardDetails?.fields;
      navigate('/invoice-preview-history', {
        state: {
          fields: cardFields,
          name: cardDetails?.name,
          status: cardDetails?.is_gui,
          invoiceId: id,
        },
      });
    };
  // Just to fetch data on load
  const getDetails = async () => {
    setLoading(true);
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

      setLoading(false);

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
      setLoading(false);
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
          data-cy='invoice-card'
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
          <SettingsMenu token={props.token} details={items} />
          <CardActionArea onClick={handleCardClick(items.id)}>
            <CardContent
              sx={{
                mt: 2,
                height: '24rem',
              }}
            >
              <InvoiceSvg />
              <Box
                sx={{
                  display: 'flex',
                  ml: 1,
                  flexDirection: 'column',
                  textAlign: 'left',
                }}
              >
                <Stack
                  direction='row'
                  spacing={1}
                  sx={{ mt: 3 }}
                  alignItems='center'
                >
                  <ReceiptIcon />
                  <Typography
                    variant='h6'
                    component='div'
                    sx={{
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {items.name}
                  </Typography>
                </Stack>

                <Stack direction='row' spacing={1.25} alignItems='center'>
                  <TagIcon style={{ fontSize: 20, marginLeft: 2 }} />
                  <Typography variant='h6' component='div'>
                    ID: {items.id}
                  </Typography>
                </Stack>

                {items.is_gui && (
                  <>
                    <Stack
                      direction='row'
                      spacing={1}
                      sx={{ my: 1 }}
                      alignItems='center'
                    >
                      <EditIcon />
                      <Typography variant='subtitle1' gutterBottom>
                        Editable
                      </Typography>
                    </Stack>
                  </>
                )}

                {items.is_ready ? (
                  <>
                    <Stack
                      direction='row'
                      spacing={1}
                      sx={{ my: 1 }}
                      alignItems='center'
                    >
                      <CheckCircleIcon />
                      <Typography variant='subtitle1' gutterBottom>
                        Status: Validated
                      </Typography>
                    </Stack>

                    <Stack
                      direction='row'
                      spacing={1}
                      sx={{ mb: 1 }}
                      alignItems='center'
                    >
                      <RuleIcon />
                      <Typography variant='subtitle1' gutterBottom>
                        Rule: {items.rule}
                      </Typography>
                    </Stack>
                  </>
                ) : (
                  <>
                    <Stack
                      direction='row'
                      spacing={1}
                      sx={{ mb: 1 }}
                      alignItems='center'
                    >
                      <CancelIcon />
                      <Typography variant='subtitle1' gutterBottom>
                        Status: Unvalidated
                      </Typography>
                    </Stack>
                  </>
                )}
              </Box>
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
      <LoadingDialog open={loading} message='Retrieving invoices...' />
      <Container maxWidth='lg' sx={{ marginTop: 11, position: 'relative' }}>
        {/* Don't use PageHeader component here because of button */}
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            width: '100%',
            mb: 1,
          }}
        >
          <Typography variant='h4'>Invoice Management</Typography>
          <Button
            variant='contained'
            onClick={handleClickFilter}
            startIcon={<FilterListIcon />}
          >
            FILTER
          </Button>
          <FilterModal
            open={filterOpen}
            onClose={handleCloseFilter}
            onCancel={handleCancelFilter}
          />
        </Box>
        <Divider sx={{ width: '100%' }} />
        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize='small' />}
          sx={{ mt: 1, position: 'absolute' }}
        >
          <Typography component={Link} to='/dashboard'>
            Dashboard
          </Typography>

          <Typography color='text.primary'>Invoice Management</Typography>
        </Breadcrumbs>

        <Grid
          container
          spacing={9}
          alignItems='center'
          // justifyContent='center'
          sx={{
            mt: 0,
            display: 'flex',
          }}
        >
          {generateInvoiceCards()}
        </Grid>

        {openError && (
          <ErrorModal open={openError} setOpen={setOpenError}>
            {error}
          </ErrorModal>
        )}
      </Container>
    </>
  );
}
