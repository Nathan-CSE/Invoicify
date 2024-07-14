import * as React from 'react';
import Button from '@mui/material/Button';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';

import {
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Box,
} from '@mui/material';

export interface SimpleDialogProps {
  open: boolean;
  onClose: (value: string) => void;
  onCancel: () => void;
}

export default function FilterModal(props: SimpleDialogProps) {
  const { onClose, onCancel, open } = props;

  const [filterOption, setFilterOption] = React.useState('id');
  const handleClose = () => {
    onClose(filterOption);
  };

  return (
    <Dialog onClose={onCancel} open={open}>
      <Box sx={{ width: '24rem', height: '17rem' }}>
        <DialogTitle>Filter Invoices</DialogTitle>
        <FormControl sx={{ pl: '2.5rem' }}>
          <FormLabel id='filter-radial-options'>Filter Options</FormLabel>
          <RadioGroup
            aria-labelledby='filter-radial-options'
            name='radio-buttons-group'
          >
            <FormControlLabel
              value='id'
              control={<Radio />}
              onClick={() => {
                setFilterOption('id');
              }}
              label='Invoice ID'
            />
            <FormControlLabel
              value='name'
              control={<Radio />}
              onClick={() => {
                setFilterOption('name');
              }}
              label='Invoice Name'
            />
            <FormControlLabel
              value='status'
              control={<Radio />}
              onClick={() => {
                setFilterOption('status');
              }}
              label='Invoice Status'
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
          <Button variant='contained' onClick={handleClose}>
            CONFIRM
          </Button>
          <Button variant='contained' color='error' onClick={onCancel}>
            CANCEL
          </Button>
        </Box>
      </Box>
    </Dialog>
  );
}
