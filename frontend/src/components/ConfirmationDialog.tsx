import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

// This is vaulted to the other sprint
export default function ConfirmDialog(props: {
  open: boolean;
  function: any;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const handleClose = () => {
    props.setOpen(false);
  };

  return (
    <>
      {/* <Button variant='outlined' onClick={handleClickOpen}>
        Open form dialog
      </Button> */}
      <Dialog open={props.open} onClose={handleClose}>
        <DialogTitle>CAUTION</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Do you wish to proceed with this action?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={props.function}>Confirm</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
