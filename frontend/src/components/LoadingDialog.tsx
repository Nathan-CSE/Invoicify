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
          sx={{
            zIndex: 'tooltip'
          }}
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


// const [loading, setLoading] = React.useState(false);
  
// const handleSubmit = async (event: any) => {
//   event.preventDefault();

//   const formData = new FormData();

//   if (files.length > 0) {
//     files.forEach(item => {
//       formData.append("files", item);
//     });
//   } else {
//     alert('You must upload a valid file to create an invoice.');
//     return;
//   }

//   // console.log('file to be sent: ', file);
//   setLoading(true);
//   try {
//     const response = await axios.post('http://localhost:5000/invoice/uploadCreate', formData, {
//       headers: {
//         Authorisation: `${props.token}`,
//         'Content-Type': 'multipart/form-data',
//       },
//     });

//     setLoading(false);
//     if (response.status === 200) {
//       console.log(response.data);
//       var str = JSON.stringify(response.data, null, 2);
//       console.log(str);
//       navigate('/invoice-creation-confirmation', {
//         state: {
//           invoice: response.data,
//           type: 'upload',
//           invoiceId: response.data.data[0].invoiceId,
//         },
//       });
//     } else {
//       console.log(response);
//       alert('Unable to create invoice');
//     }
//   } catch (err) {
//     alert(err);

//   } 
// };

// return (
//   <>
//     <Container maxWidth='lg' sx={{ marginTop: 11 }}>
//       <LoadingDialog open={loading} message='Creating invoice(s)...' />