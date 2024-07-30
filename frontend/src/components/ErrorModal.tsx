import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Typography from '@mui/material/Typography';
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
