import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useNavigate } from 'react-router-dom';

export default function SuccessDialog(props: {
  open: boolean;
  message: string;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const navigate = useNavigate();
  const handleClose = () => {
    props.setOpen(false);
    navigate('/invoice-management');
  };

  return (
    <>
      <Dialog
        open={props.open}
        onClose={handleClose}
        sx={{ minWidth: '20rem' }}
      >
        <DialogTitle>SUCCESS</DialogTitle>
        <DialogContent sx={{ minWidth: '20rem' }}>
          <DialogContentText>{props.message}</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
