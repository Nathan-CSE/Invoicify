import { Box, Breadcrumbs, Divider, Grid, Typography } from '@mui/material';
import * as React from 'react';
import { useLocation } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { Link, useNavigate } from 'react-router-dom';

export default function HistoryPreviewInvoice(props: { token: string }) {
  const location = useLocation();
  const dataFields = location.state.fields;
  const name = location.state.name;

  function formatJSON(data: any, indentlvl = 0) {
    let formattedString = '';
    const indent = ' '.repeat(indentlvl * 2);
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'object') {
        formattedString += `${indent}${key}:\n${formatJSON(
          value,
          indentlvl + 1
        )}`;
      } else {
        formattedString += `${indent}${key}: ${value}\n`;
      }
    }
    return formattedString;
  }
  return (
    <>
      <Box sx={{ mt: 10, ml: 10 }}>
        <Typography variant='h5' sx={{ mt: 4 }}>
          Previeving: {name}
        </Typography>
        <Divider sx={{ borderColor: 'black', width: '100%' }} />
        <Breadcrumbs
          aria-label='breadcrumb'
          separator={<NavigateNextIcon fontSize='small' />}
          sx={{ mt: 1 }}
        >
          <Typography component={Link} to='/dashboard'>
            Dashboard
          </Typography>

          <Typography component={Link} to='/invoice-management'>
            Invoice Management
          </Typography>
          <Typography color='text.primary'>Invoice Preview</Typography>
        </Breadcrumbs>
        <Typography>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{formatJSON(dataFields)}</pre>
        </Typography>
      </Box>
    </>
  );
}
