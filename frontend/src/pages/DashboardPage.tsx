import React from 'react';
import { Link } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { CardActionArea } from '@mui/material';
import { ReactComponent as TickSvg } from '../assets/validate.svg';
import { ReactComponent as PenSvg } from '../assets/create.svg';
import { ReactComponent as SendSvg } from '../assets/send.svg';
import useAuth from '../helpers/useAuth';

import { ReactComponent as ManageSvg } from '../assets/manage.svg';
import { ReactComponent as CogSvg } from '../assets/settings.svg';
import { ReactComponent as DocSvg } from '../assets/documentation.svg';
import PageHeader from '../components/PageHeader';

function DashboardPage(props: {
  token: string;
  setToken: React.Dispatch<React.SetStateAction<string>>;
}) {
  console.log(props.token);
  useAuth(props.token);

  interface dashboardCardInfo {
    svg: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
    route: string;
    cy: string;
  }

  interface dashboardDict {
    [key: string]: dashboardCardInfo;
  }

  const options = {
    'Create/Upload an Invoice': {
      svg: PenSvg,
      route: '/invoice-creation',
      cy: 'dashboard-creation',
    },
    'Validate an Invoice': {
      svg: TickSvg,
      route: '/invoice-validation',
      cy: 'dashboard-validation',
    },
    'Send an Invoice': {
      svg: SendSvg,
      route: '/invoice-sending',
      cy: 'dashboard-sending',
    },
    'Manage Invoices': {
      svg: ManageSvg,
      route: '/invoice-management',
      cy: 'dashboard-management',
    },
    'Account Settings': {
      svg: CogSvg,
      route: '/settings',
      cy: 'dashboard-settings',
    },
    'Documentation Info': {
      svg: DocSvg,
      route: '/documentation',
      cy: 'dashboard-documentation',
    },
  };

  const breadcrumbNav = {
    Dashboard: '/dashboard',
  };

  // Function to generate the dashboard cards
  // - Sets up the route, the relevant image and naming
  function generateOptions(options: dashboardDict): JSX.Element[] {
    return Object.entries(options).map(([name, items], index) => (
      <Grid key={index} item>
        <Card
          data-cy={items.cy}
          component={Link}
          to={items.route}
          sx={{
            border: 1,
            borderRadius: '16px',
            width: '20rem',
            height: '18rem',
            alignContent: 'center',
            textAlign: 'center',
            display: 'flex',
            textDecoration: 'none',
          }}
        >
          <CardActionArea>
            <CardContent>
              <items.svg />
              <Typography variant='h6' component='div'>
                {name}
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid>
    ));
  }

  return (
    <>
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <PageHeader HeaderTitle={'Welcome!'} BreadcrumbDict={breadcrumbNav} />

        <Grid
          container
          spacing={9}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          {generateOptions(options)}
        </Grid>
      </Container>
    </>
  );
}

export default DashboardPage;
