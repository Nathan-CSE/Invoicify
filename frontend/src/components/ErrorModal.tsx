import * as React from 'react';
import { Alert, Snackbar } from '@mui/material';

function ErrorModal(props: {
  children: string;
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const handleClose = () => {
    props.setOpen(false);
  };

  return (
    <>
      <Snackbar
        open={props.open}
        autoHideDuration={10000}
        onClose={handleClose}
      >
        <Alert
          variant='filled'
          severity='error'
          onClose={handleClose}
          aria-labelledby='errorModalTitle'
        >
          {props.children}
        </Alert>
      </Snackbar>
    </>
  );
}

export default ErrorModal;
