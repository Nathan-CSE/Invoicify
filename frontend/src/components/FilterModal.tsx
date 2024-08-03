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
  DialogContent,
  DialogActions,
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
    <Dialog onClose={onCancel} open={open} maxWidth='sm'>
      <DialogTitle fontWeight={'medium'}>Filter Invoices</DialogTitle>
      <DialogContent>
        <FormControl>
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
              label='Filter by invoice ID'
            />
            <FormControlLabel
              value='name'
              control={<Radio />}
              onClick={() => {
                setFilterOption('name');
              }}
              label='Filter alphabetically by invoice name'
            />
            <FormControlLabel
              value='status'
              control={<Radio />}
              onClick={() => {
                setFilterOption('status');
              }}
              label='Show validated invoices only'
            />
          </RadioGroup>
        </FormControl>
      </DialogContent>
      <DialogActions sx={{ m: 1 }}>
        <Button variant='contained' onClick={handleClose}>
          CONFIRM
        </Button>
        <Button variant='contained' color='error' onClick={onCancel}>
          CANCEL
        </Button>
      </DialogActions>
    </Dialog>
  );
}
