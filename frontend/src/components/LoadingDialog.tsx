// LoadingDialog.tsx
import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function LoadingDialog(props: { open: boolean; message: string }) {
  return (
    <Dialog open={props.open} aria-labelledby='loading-dialog'>
      <DialogContent>
        <Box
          display='flex'
          alignItems='center'
          justifyContent='center'
          flexDirection='column'
        >
          <CircularProgress />
          <Typography variant='body1' sx={{ marginTop: 2 }}>
            {props.message}
          </Typography>
        </Box>
      </DialogContent>
    </Dialog>
  );
}

export default LoadingDialog;
