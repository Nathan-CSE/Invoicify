import React from 'react';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import Chip from '@mui/material/Chip';
import TagIcon from '@mui/icons-material/Tag';
import { Typography } from '@mui/material';

function MultipleSelect(props: {
  invoices: string[];
  availableInvoices: { invoiceId: number; name: string }[];
  file: File[] | null;
  handleChange: (
    event: SelectChangeEvent<string[]>,
    child: React.ReactNode
  ) => void;
}) {
  const { invoices, availableInvoices, file, handleChange } = props;

  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl variant='standard' fullWidth>
        <InputLabel id='select-invoice-label' sx={{ paddingTop: '10px' }}>
          Select Invoice
        </InputLabel>
        <Select
          data-cy='multiple-select'
          labelId='select-invoice-label'
          id='select-invoice'
          name='select-invoice'
          multiple
          value={invoices}
          label='Select Invoice'
          onChange={handleChange}
          disabled={Boolean(file)}
          renderValue={(selected) => (
            <Box
              sx={{
                display: 'flex',
                flexWrap: 'nowrap',
                gap: 0.5,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
                maxWidth: '100%',
              }}
            >
              {selected.map((value: string) => {
                const invoice = availableInvoices.find(
                  (item) => item.invoiceId === Number(value)
                );
                return (
                  <Chip
                    key={value}
                    label={invoice ? invoice.name : value}
                    sx={{
                      height: 25,
                    }}
                  />
                );
              })}
            </Box>
          )}
          sx={{ height: '45px' }}
        >
          {availableInvoices.map((invoice) => {
            return (
              <MenuItem
                data-cy={invoice.name}
                key={invoice.invoiceId}
                value={invoice.invoiceId.toString()}
              >
                <Checkbox
                  checked={invoices.includes(invoice.invoiceId.toString())}
                />
                <TagIcon
                  style={{
                    paddingBottom: '1px',
                    marginRight: '4px',
                    fontSize: 15,
                  }}
                />
                <Typography
                  sx={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {invoice.invoiceId}: {invoice.name}
                </Typography>
              </MenuItem>
            );
          })}
        </Select>
      </FormControl>
    </Box>
  );
}

export default MultipleSelect;
