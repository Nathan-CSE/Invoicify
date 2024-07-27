import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { InputLabel, Select, MenuItem, SelectChangeEvent, Box, FormControl } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

export default function DownloadReport(props: { invoiceName: String }) {
  const [open, setOpen] = React.useState(false);
  const [downloadFormat, setDownloadFormat] = React.useState('');
  const { invoiceName } = props;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (event: SelectChangeEvent) => {
    console.log('this is event.target: ', event.target);
    setDownloadFormat(event.target.value);
  };

  return (
    <>
      <Button
        onClick={handleClickOpen}
        startIcon={<DownloadIcon />}
        variant='contained'
        sx={{
          height: '50px',
          padding: '25px',
        }}
      >
        Download Report
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        PaperProps={{
          component: 'form',
          onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
            event.preventDefault();
            const formData = new FormData(event.currentTarget);
            const formJson = Object.fromEntries((formData as any).entries());
            handleClose();
          },
        }}
      >
        <DialogTitle>Download report for {invoiceName}?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Select a download format below.
          </DialogContentText>

          <FormControl fullWidth variant="outlined" margin="normal" required sx={{ mt: 2, mb: -1 }}>      
            <InputLabel id="select-format">Download Format</InputLabel>
            <Select
              labelId="select-format"
              id="select-format"
              value={downloadFormat}
              label="Download Format"
              onChange={handleChange}
              required
              fullWidth
            >
              <MenuItem value={'JSON'}>JSON</MenuItem>
              <MenuItem value={'HTML'}>HTML</MenuItem>
              <MenuItem value={'PDF'}>PDF</MenuItem>

            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type="submit">Download</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}