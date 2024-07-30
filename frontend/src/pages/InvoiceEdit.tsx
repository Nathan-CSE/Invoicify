import { Box } from '@mui/material';
import CreationGUI from './InvoiceCreation/CreationGUI';
import { useLocation } from 'react-router-dom';
import useAuth from './useAuth';

export default function InvoiceEdit(props: { token: string }) {
  useAuth(props.token);
  const location = useLocation();

  return (
    <>
      <Box sx={{ mt: 11 }}>
        <CreationGUI
          token={props.token}
          editFlag={true}
          data={location.state.details}
          id={location.state.details.id}
        ></CreationGUI>
      </Box>
    </>
  );
}
