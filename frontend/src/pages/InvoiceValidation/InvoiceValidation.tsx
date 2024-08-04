import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useNavigate } from 'react-router-dom';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DropzoneArea } from 'mui-file-dropzone';
import axios, { AxiosError } from 'axios';
import MultipleSelect from '../../components/MultipleSelect';
import FactCheckIcon from '@mui/icons-material/FactCheck';
import LoadingDialog from '../../components/LoadingDialog';
import useAuth from '../../helpers/useAuth';
import PageHeader from '../../components/PageHeader';
import ErrorModal from '../../components/ErrorModal';

function InvoiceValidation(props: { token: string }) {
  useAuth(props.token);

  const navigate = useNavigate();
  const [loading, setLoading] = React.useState(false);
  const [invoices, setInvoices] = React.useState<string[]>([]);
  const [ruleSet, setRuleSet] = React.useState<string[]>([]);
  const [files, setFiles] = React.useState<File[] | null>([]);
  const [availableInvoices, setAvailableInvoices] = React.useState<
    { invoiceId: number; name: string }[]
  >([]);

  // Error handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  const breadcrumbNav = {
    Dashboard: '/dashboard',
    'Invoice Validation': '/invoice-validation',
  };

  const handleChange = (event: SelectChangeEvent<string[]>) => {
    const { name, value } = event.target;

    if (name === 'rule-set') {
      setRuleSet(value as string[]);
    } else {
      setInvoices(typeof value === 'string' ? value.split(',') : value);
    }
  };

  const handleSubmit = async (event: any) => {
    event.preventDefault();

    if (files === null && invoices.length === 0) {
      setOpenError(true);
      setError(
        'You must either upload or select an xml file to create an invoice.'
      );

      return;
    }

    const formData = new FormData();

    if (files) {
      files.forEach((item) => {
        formData.append('files', item);
      });
    }

    try {
      var response;
      setLoading(true);

      if (files) {
        response = await axios.post(
          `http://localhost:5000/invoice/uploadValidate?rules=${ruleSet}`,
          formData,
          {
            headers: {
              Authorisation: `${props.token}`,
              'Content-Type': 'multipart/form-data',
            },
          }
        );
      } else {
        response = await axios.get(
          `http://localhost:5000/invoice/validate?rules=${ruleSet}&id=${invoices}`,
          {
            headers: {
              Authorisation: `${props.token}`,
            },
          }
        );
      }

      setLoading(false);

      if (response.status === 200) {
        navigate('/invoice-validation-report', {
          state: { response: response.data, ruleSet: ruleSet },
        });
      } else {
        navigate('/invoice-validation-report', {
          state: { response: response.data, ruleSet: ruleSet },
        });
      }
    } catch (err) {
      setLoading(false);
      setOpenError(true);
      setError(
        'Unable to validate invoice. Make sure the XML file itself is complete and has no syntactic errors.'
      );
    }
  };

  const handleFileChange = (loadedFiles: File[]) => {
    if (loadedFiles.length > 0) {
      setFiles(loadedFiles);
      setInvoices([]); // Clear invoice selection if a file is uploaded
    } else {
      setFiles(null);
    }
  };

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          'http://localhost:5000/invoice/history?is_ready=false',
          {
            headers: {
              Authorisation: `${props.token}`,
            },
          }
        );

        var allInvoices = [];

        if (response.status === 200) {
          for (let i = 0; i < response.data.length; i++) {
            var invoiceInfo = {
              name: response.data[i].name,
              invoiceId: response.data[i].id,
            };

            allInvoices.push(invoiceInfo);
          }

          setAvailableInvoices(allInvoices);
        } else {
          setOpenError(true);
          setError('Unable to retrieve valid invoices');
        }
      } catch (error) {
        setLoading(false);
        const err = error as AxiosError<{ message: string }>;
        if (err.response) {
          setOpenError(true);
          setError(err.response.data.message);
        } else if (error instanceof Error) {
          setOpenError(true);
          setError(error.message);
        }
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <LoadingDialog open={loading} message='Validating invoice(s)...' />
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        <PageHeader
          HeaderTitle={'Invoice Validation'}
          BreadcrumbDict={breadcrumbNav}
        />

        <form onSubmit={handleSubmit}>
          <Box sx={{ my: 5 }}>
            <DropzoneArea
              acceptedFiles={['.xml']}
              fileObjects={files}
              onChange={handleFileChange}
              dropzoneText={'Upload a UBL2.1 XML Invoice File'}
              filesLimit={10}
            />
          </Box>

          <Typography variant='h5' textAlign='center' sx={{ my: 2 }}>
            OR
          </Typography>

          <MultipleSelect
            invoices={invoices}
            availableInvoices={availableInvoices}
            file={files}
            handleChange={handleChange}
          />

          <Box sx={{ minWidth: 120, my: 3 }}>
            <FormControl variant='standard' fullWidth>
              <InputLabel id='select-rule-set'>Rule Set</InputLabel>
              <Select
                data-cy='validation-select'
                labelId='select-rule-set'
                id='rule-set'
                name='rule-set'
                value={ruleSet}
                label='Rule Set'
                onChange={handleChange}
                required
              >
                <MenuItem value={'AUNZ_PEPPOL_1_0_10'}>
                  AUNZ_PEPPOL_1_0_10
                </MenuItem>
                <MenuItem value={'AUNZ_PEPPOL_SB_1_0_10'}>
                  AUNZ_PEPPOL_SB_1_0_10
                </MenuItem>
                <MenuItem value={'AUNZ_UBL_1_0_10'}>AUNZ_UBL_1_0_10</MenuItem>
                <MenuItem value={'FR_EN16931_CII_1_3_11'}>
                  FR_EN16931_CII_1_3_11
                </MenuItem>
                <MenuItem value={'FR_EN16931_UBL_1_3_11'}>
                  FR_EN16931_UBL_1_3_11
                </MenuItem>
                <MenuItem value={'RO_RO16931_UBL_1_0_8_EN16931'}>
                  RO_RO16931_UBL_1_0_8_EN16931
                </MenuItem>
                <MenuItem value={'RO_RO16931_UBL_1_0_8_CIUS_RO'}>
                  RO_RO16931_UBL_1_0_8_CIUS_RO
                </MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Box textAlign='center'>
            <Button
              data-cy='validation-submit'
              type='submit'
              variant='contained'
              startIcon={<FactCheckIcon />}
              sx={{
                padding: '15px',
              }}
            >
              Validate Invoice(s)
            </Button>
          </Box>
        </form>
      </Container>
      {openError && (
        <ErrorModal open={openError} setOpen={setOpenError}>
          {error}
        </ErrorModal>
      )}
    </>
  );
}

export default InvoiceValidation;
