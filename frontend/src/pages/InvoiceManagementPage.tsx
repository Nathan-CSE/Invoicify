import { Box, Breadcrumbs, Divider } from '@mui/material';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import Typography from '@mui/material/Typography';
import * as React from 'react';
import axios, { AxiosError } from 'axios';
import { Link } from 'react-router-dom';
import ErrorModal from '../components/ErrorModal';

export default function InvoiceManagement(props: { token: string }) {
  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

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
        console.log(response);
        // alert(response.data.message);
      } else {
        setOpenError(true);
        setError(response.data.message);
      }
    } catch (error) {
      const err = error as AxiosError<{ message: string }>;
      if (err.response) {
        setOpenError(true);
        setError(err.response.data.message);
      } else if (error instanceof Error) {
        setOpenError(true);
        setError(error.message);
      }
    }
  };

  React.useEffect(() => {
    getDetails();
  }, []);

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
      </Box>
      <Box sx={{ mt: 10 }}>
        {openError && <ErrorModal setOpen={setOpenError}>{error}</ErrorModal>}
      </Box>
    </>
  );
}
