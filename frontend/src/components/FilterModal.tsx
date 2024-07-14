import * as React from 'react';
import Button from '@mui/material/Button';
import Avatar from '@mui/material/Avatar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import PersonIcon from '@mui/icons-material/Person';
import AddIcon from '@mui/icons-material/Add';
import Typography from '@mui/material/Typography';
import { blue } from '@mui/material/colors';
import {
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Box,
  Grid,
} from '@mui/material';

const emails = ['username@gmail.com', 'user02@gmail.com'];

export interface SimpleDialogProps {
  open: boolean;
  selectedValue: string;
  onClose: (value: string) => void;
}

export default function FilterModal(props: SimpleDialogProps) {
  const { onClose, selectedValue, open } = props;

  const handleClose = () => {
    onClose(selectedValue);
  };

  const handleListItemClick = (value: string) => {
    onClose(value);
  };

  return (
    <Dialog onClose={handleClose} open={open}>
      <Box sx={{ width: '24rem', height: '17rem' }}>
        <DialogTitle>Filter Invoices</DialogTitle>
        <FormControl sx={{ pl: '2rem' }}>
          <FormLabel id='demo-radio-buttons-group-label'>
            Filter Options
          </FormLabel>
          <RadioGroup
            aria-labelledby='demo-radio-buttons-group-label'
            defaultValue='name'
            name='radio-buttons-group'
          >
            <FormControlLabel
              value='name'
              control={<Radio />}
              label='Invoice Name'
            />
            <FormControlLabel
              value='status'
              control={<Radio />}
              label='Invoice Status'
            />
            <FormControlLabel
              value='date'
              control={<Radio />}
              label='Creation Date'
            />
          </RadioGroup>
        </FormControl>
        <Box
          sx={{
            flexDirection: 'row',
            display: 'flex',
            gap: '0.5rem',
            pr: '0.5rem',
            mt: '0.5rem',
            justifyContent: 'flex-end',
          }}
        >
          <Button variant='contained'>CONFIRM</Button>
          <Button variant='contained' color='error' onClick={handleClose}>
            CANCEL
          </Button>
        </Box>
      </Box>
    </Dialog>
  );
}
