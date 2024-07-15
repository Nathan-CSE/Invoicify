import { Box, Breadcrumbs, Divider, Grid, Typography } from '@mui/material';
import * as React from 'react';
import { useLocation } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import { Link, useNavigate } from 'react-router-dom';

export default function HistoryPreviewInvoice(props: { token: string }) {
  const location = useLocation();
  const name = location.state.name;
  const dataFields = location.state.fields;

  const formatJSON = (dataFields: any, indentLevel = 0) => {
    let formattedString = '';
    const indent = ' '.repeat(indentLevel * 2); // Use two spaces for each indent level

    // Checks if its an object and has children to loop through so we recurse
    // Else we just display the value
    for (const [key, value] of Object.entries(dataFields)) {
      if (typeof value === 'object') {
        formattedString += `${indent}${key}:\n${formatJSON(
          value,
          indentLevel + 1
        )}`;
      } else {
        formattedString += `${indent}${key}: ${value}\n`;
      }
    }

    return formattedString;
  };
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
