import React from 'react';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import Chip from '@mui/material/Chip';

export default function MultipleSelect(props: { invoices: string[], availableInvoices: { invoiceId: number; name: string; }[], file: File[] | null, handleChange: (event: SelectChangeEvent<string[]>, child: React.ReactNode) => void }) {
  const { invoices, availableInvoices, file, handleChange } = props;
  
  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl variant="standard" fullWidth>
        <InputLabel id="select-invoice-label" sx={{ paddingTop: '10px' }}>Select Invoice</InputLabel>
        <Select
          labelId="select-invoice-label"
          id="select-invoice"
          name='select-invoice'
          multiple
          value={invoices}
          label="Select Invoice"
          onChange={handleChange}
          disabled={Boolean(file)}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'nowrap', gap: 0.5, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '100%' }}>
              {selected.map((value: string) => {
                const invoice = availableInvoices.find(item => item.invoiceId === Number(value));
                return (
                  <Chip
                    key={value}
                    label={invoice ? invoice.name : value}
                    sx={{ height: 25 }}
                  />
                );
              })}
            </Box>
          )}
          sx={{ height: '45px' }}
        >
          {availableInvoices.map((invoice) => (
            <MenuItem key={invoice.invoiceId} value={invoice.invoiceId.toString()}>
              <Checkbox checked={invoices.indexOf(invoice.invoiceId.toString()) > -1} />
              {invoice.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}
