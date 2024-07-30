import { Box } from '@mui/material';
import CreationGUI from './InvoiceCreation/CreationGUI';
import { useLocation } from 'react-router-dom';

export default function InvoiceEdit(props: { token: string }) {
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
