import * as React from 'react';
import { Breadcrumbs, Divider, Stack, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';

interface BreadcrumbDict {
  [key: string]: string;
}

export default function BreadcrumbNav(props: { HeaderTitle: string, BreadcrumbDict: BreadcrumbDict }) {
  const { HeaderTitle, BreadcrumbDict } = props; 
  const entries = Object.entries(BreadcrumbDict);
  const lastIndex = entries.length - 1;
  

  return (
    <>

      <Typography variant='h4'>{HeaderTitle}</Typography>

      <Divider sx={{ borderBottomWidth: 1.5, marginBottom: 1 }} />

      <Breadcrumbs
        aria-label='breadcrumb'
        separator={<NavigateNextIcon fontSize='small' />}
      >
        {entries.length === 1 ? (
          <Stack direction="row" spacing={1} sx={{ mb: 4 }}>
            <NavigateNextIcon fontSize='small' sx={{ mt: 0.1, color: 'black' }}/>
            <Typography color='text.primary'>
              {entries[0][0]}
            </Typography>
          </Stack>
        ) : (
          entries.map(([pageName, route], index) => (
            index === lastIndex ? (
              <Typography key={route} color="text.primary">
                {pageName}
              </Typography>
            ) : (
              <Typography component={Link} to={route}>
                {pageName}
              </Typography>
            )
          ))
        )}
      </Breadcrumbs>
    </>
  );
}
