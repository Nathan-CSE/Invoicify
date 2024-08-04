import React from 'react';
import {
  Button,
  TextField,
  Box,
  Typography,
  Container,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
  Paper,
  IconButton,
  Popover,
  Grid,
  Stack,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import InfoIcon from '@mui/icons-material/Info';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { DropzoneDialogBase } from 'mui-file-dropzone';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import vatRates from '../../VATRates.json';
import ErrorModal from '../../components/ErrorModal';
import axios, { AxiosError } from 'axios';
import LoadingDialog from '../../components/LoadingDialog';
import useAuth from '../../helpers/useAuth';
import SaveIcon from '@mui/icons-material/Save';
import SuccessDialog from '../../components/SuccessDialog';
import PageHeader from '../../components/PageHeader';

interface FileObject {
  file: File;
}

// Edit flag to determine if we are editing
// Data passed in to preload it if we are editing
function CreationGUI(props: {
  token: string;
  editFlag: boolean;
  data: any;
  id: number;
}) {
  useAuth(props.token);

  const [isSmallScreen, setIsSmallScreen] = React.useState(
    window.innerWidth <= 900
  );

  const [openDialog, setDialog] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [loadingMsg, setLoadingMsg] = React.useState<string>('');
  const navigate = useNavigate();
  const countries = Object.keys(vatRates);

  // Preloaded data
  const [fields, setFields] = React.useState<any>(null);

  const breadcrumbNavEdit = {
    Dashboard: '/dashboard',
    'Invoice Management': '/invoice-management',
    'Invoice Edit': '/invoice-edit',
  };

  const breadcrumbNavGUI = {
    Dashboard: '/dashboard',
    'Invoice Creation': '/invoice-creation',
    'Invoice Creation - GUI': '/invoice-creation-GUI',
  };

  const [invName, setInvName] = React.useState<string>('');
  const [invNum, setInvNum] = React.useState<string>('');
  const [date, setDate] = React.useState<Date>(new Date());

  const [sellerABN, setSellerABN] = React.useState<string>('');
  const [sellerName, setSellerName] = React.useState<string>('');
  const [sellerStreetName, setSellerStreetName] = React.useState<string>('');
  const [sellerAddStreetName, setSellerAddStreetName] =
    React.useState<string>('');
  const [sellerCityName, setSellerCityName] = React.useState<string>('');
  const [sellerCode, setSellerCode] = React.useState<string>('');

  const [buyerABN, setBuyerABN] = React.useState<string>('');
  const [buyerName, setBuyerName] = React.useState<string>('');
  const [buyerStreetName, setBuyerStreetName] = React.useState<string>('');
  const [buyerAddStreetName, setBuyerAddStreetName] =
    React.useState<string>('');
  const [buyerCityName, setBuyerCityName] = React.useState<string>('');
  const [buyerCode, setBuyerCode] = React.useState<string>('');

  // Form Information
  const [nextId, setNextId] = React.useState(2);
  const [selectedRowIds, setSelectedRowIds] = React.useState<number[]>([]);
  const [sellerCountry, setSellerCountry] = React.useState('');
  const [buyerCountry, setBuyerCountry] = React.useState('');
  const [vatRate, setVatRate] = React.useState<number>(0);

  const [rows, setRows] = React.useState([
    {
      id: 1,
      quantity: 0,
      unitCode: '',
      item: '',
      description: '',
      unitPrice: 0,
      GST: 0,
      totalPrice: 0,
    },
  ]);
  const handleDateChange = (newDate: any) => {
    setDate(newDate);
  };

  React.useEffect(() => {
    if (props.editFlag && props.data) {
      setFields(props.data.fields);
    }

    const handleResize = () => {
      setIsSmallScreen(window.innerWidth <= 600);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // When the data is loaded in we can preload the fields
  React.useEffect(() => {
    if (props.editFlag) {
      const dateString = fields?.IssueDate || '';
      const [day, month, year] = dateString.split('/');
      const newDate = `${year}-${month}-${day}`;
      setDate(new Date(newDate));

      setInvName(fields?.BuyerReference || '');
      setInvNum(fields?.ID || '');
      setSellerABN(
        fields?.AccountingSupplierParty.Party.PartyLegalEntity.CompanyID[
          '@value'
        ] || ''
      );
      setSellerName(
        fields?.AccountingSupplierParty.Party.PartyLegalEntity
          .RegistrationName || ''
      );
      setSellerStreetName(
        fields?.AccountingSupplierParty.Party.PostalAddress.StreetName || ''
      );
      setSellerAddStreetName(
        fields?.AccountingSupplierParty.Party.PostalAddress
          .AdditionalStreetName || ''
      );
      setSellerCityName(
        fields?.AccountingSupplierParty.Party.PostalAddress.CityName || ''
      );
      setSellerCode(
        fields?.AccountingSupplierParty.Party.PostalAddress.PostalZone || ''
      );

      setBuyerABN(
        fields?.AccountingCustomerParty.Party.PartyLegalEntity.CompanyID[
          '@value'
        ] || ''
      );
      setBuyerName(
        fields?.AccountingCustomerParty.Party.PartyLegalEntity
          .RegistrationName || ''
      );
      setBuyerStreetName(
        fields?.AccountingCustomerParty.Party.PostalAddress.StreetName || ''
      );
      setBuyerAddStreetName(
        fields?.AccountingCustomerParty.Party.PostalAddress
          .AdditionalStreetName || ''
      );
      setBuyerCityName(
        fields?.AccountingCustomerParty.Party.PostalAddress.CityName || ''
      );
      setBuyerCode(
        fields?.AccountingCustomerParty.Party.PostalAddress.PostalZone || ''
      );

      if (buyerCountry == '') {
        setBuyerCountry(
          fields?.AccountingCustomerParty.Party.PostalAddress.Country
            .IdentificationCode || ''
        );
      }
      if (sellerCountry == '') {
        setSellerCountry(
          fields?.AccountingSupplierParty.Party.PostalAddress.Country
            .IdentificationCode || ''
        );
      }

      const selectedCountry = buyerCountry as keyof typeof vatRates;
      setVatRate(vatRates[selectedCountry]);

      // Determines if the invoice items are an array or not and deal with each case
      if (Array.isArray(fields?.InvoiceLine)) {
        let tempRows = rows;
        let firstFlag = true;

        fields?.InvoiceLine.forEach((item: any) => {
          if (firstFlag) {
            const baseAmount =
              parseFloat(item?.Price?.PriceAmount['@value']) /
              (1 +
                Number(fields?.TaxTotal.TaxSubtotal.TaxCategory.Percent / 100));

            const newRow = {
              id: parseInt(item.ID) + 1,
              quantity: parseInt(item?.InvoicedQuantity['@value'], 10) || 0,
              unitCode: item?.InvoicedQuantity.unitCode || '',
              item: item?.Item.Name || '',
              description: item?.Item.Description || '',
              unitPrice: baseAmount || 0.0,
              GST: parseFloat(item.Item.ClassifiedTaxCategory?.Percent) || 0.0,
              totalPrice: parseFloat(item.LineExtensionAmount['@value']),
            };
            firstFlag = false;

            tempRows = [newRow];
            setNextId(nextId + 1);
          } else {
            const baseAmount =
              parseFloat(item?.Price?.PriceAmount['@value']) /
              (1 +
                Number(fields?.TaxTotal.TaxSubtotal.TaxCategory.Percent / 100));

            const newRow = {
              id: parseInt(item.ID) + 1,
              quantity: parseInt(item?.InvoicedQuantity['@value'], 10),
              unitCode: item?.InvoicedQuantity.unitCode,
              item: item?.Item.Name || '',
              description: item?.Item.Description || '',
              unitPrice: baseAmount || 0.0,
              GST: parseFloat(item.Item.ClassifiedTaxCategory?.Percent) || 0.0,
              totalPrice: parseFloat(item.LineExtensionAmount['@value']),
            };
            tempRows.push(newRow);

            setNextId(nextId + 1);
          }
        });
        setRows(tempRows);
        if (vatRate) {
          rows.forEach((row) => {
            handleCellValueChange(row);
          });
        }
      } else {
        if (fields?.InvoiceLine) {
          const baseAmount =
            parseFloat(fields?.InvoiceLine.Price.PriceAmount['@value']) /
            (1 +
              Number(fields?.TaxTotal.TaxSubtotal.TaxCategory.Percent) / 100);

          const newRow = {
            id: 1,
            quantity: parseInt(
              fields?.InvoiceLine.InvoicedQuantity['@value'],
              10
            ),
            unitCode: fields?.InvoiceLine.InvoicedQuantity.unitCode,
            item: fields?.InvoiceLine.Item.Name || '',
            description: fields?.InvoiceLine.Item.Description || '',
            unitPrice: parseFloat(baseAmount.toFixed(2)),
            GST: parseFloat(
              (
                (baseAmount *
                  Number(fields?.TaxTotal.TaxSubtotal.TaxCategory.Percent)) /
                100
              ).toFixed(2)
            ),
            totalPrice: Number(
              fields?.InvoiceLine.LineExtensionAmount['@value']
            ),
          };

          setRows([newRow]);
        }
        if (vatRate) {
          rows.forEach((row) => {
            handleCellValueChange(row);
          });
        }
      }
    }
  }, [fields, buyerCountry]);

  // Uploading additional documents
  const [openFileUpload, setOpenFileUpload] = React.useState(false);
  const [fileList, setFileList] = React.useState<FileObject[]>([]);

  // Error Handling
  const [openError, setOpenError] = React.useState(false);
  const [error, setError] = React.useState('');

  // Popover Info
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);

  const handleClickPopover = (
    event:
      | React.MouseEvent<HTMLButtonElement>
      | React.MouseEvent<HTMLAnchorElement>
  ) => {
    if (event.currentTarget instanceof Element) {
      setAnchorEl(event.currentTarget);
    }
  };

  const handleClosePopover = () => {
    setAnchorEl(null);
  };

  const openPopover = Boolean(anchorEl);
  const id = openPopover ? 'simple-popover' : undefined;

  // Function for monetary totals
  const calculateTotals = () => {
    let totalGST = 0;
    let totalAmount = 0;

    rows.forEach((row) => {
      totalGST += row.GST * row.quantity;
      totalAmount += Number(row.totalPrice);
    });

    return {
      totalGST: totalGST,
      totalTaxable: totalAmount - totalGST,
      totalAmount: totalAmount,
    };
  };

  const { totalGST, totalTaxable, totalAmount } = calculateTotals();

  // Changes the VAT rate based on the buyer's country
  const handleChange = (event: { target: { value: any; name: string } }) => {
    const selectedCountry = event.target.value as keyof typeof vatRates;
    if (event.target.name == 'buyerCountry') {
      setBuyerCountry(selectedCountry);
      setVatRate(vatRates[selectedCountry]);
      rows.forEach((row) => {
        handleCellValueChange(row);
      });
    } else {
      setSellerCountry(selectedCountry);
    }
  };

  // For adding invoice items
  const columns: GridColDef[] = [
    {
      field: 'quantity',
      headerName: 'Quantity',
      type: 'number',
      width: 75,
      editable: true,
    },
    { field: 'unitCode', headerName: 'Unit Code', width: 100, editable: true },
    { field: 'item', headerName: 'Item', width: 120, editable: true },
    {
      field: 'description',
      headerName: 'Description',
      width: 180,
      editable: true,
    },
    {
      field: 'unitPrice',
      headerName: 'Unit Price ($)',
      type: 'number',
      width: 120,
      editable: true,
    },
    {
      field: 'GST',
      headerName: 'GST ($)',
      type: 'number',
      width: 80,
      editable: false,
    },
    {
      field: 'totalPrice',
      headerName: 'Total Price ($)',
      type: 'number',
      width: 120,
      editable: false,
    },
  ];

  const addRow = () => {
    const newRow = {
      id: nextId,
      quantity: 0,
      unitCode: '',
      item: '',
      description: '',
      unitPrice: 0,
      GST: 0,
      totalPrice: 0,
    };
    setRows([...rows, newRow]);
    setNextId(nextId + 1);
  };

  const removeRow = () => {
    let updatedRows = rows.filter((row) => !selectedRowIds.includes(row.id));
    setRows(updatedRows);
    setSelectedRowIds([]);
  };

  const handleCellValueChange = (newRow: {
    id: any;
    quantity: any;
    unitCode?: string;
    item?: string;
    description?: string;
    unitPrice: any;
    GST: any;
    totalPrice: any;
  }) => {
    newRow.GST = (vatRate / 100) * newRow.unitPrice;
    newRow.totalPrice = newRow.quantity * (newRow.unitPrice + newRow.GST);

    const updatedRows = rows.map((row) =>
      row.id === newRow.id ? { ...row, ...newRow } : row
    );

    setRows(updatedRows);
    calculateTotals();
  };

  // Form submission & sending to backend + error handling
  const handleSubmit = async (event: {
    preventDefault: () => void;
    currentTarget: HTMLFormElement | undefined;
  }) => {
    event.preventDefault();

    let errorCheck = false;

    const formData = new FormData(event.currentTarget);
    const invoiceData: any = {
      invoiceName: formData.get('invoiceName'),
      invoiceNumber: Number(formData.get('invoiceNumber')),
      invoiceIssueDate: formData.get('invoiceIssueDate'),
      seller: {
        ABN: Number(formData.get('sellerABN')),
        companyName: formData.get('sellerCompanyName'),
        companyAddress: formData.get('sellerAddress'),
        address: {
          streetName: formData.get('sellerStreetName'),
          additionalStreetName: formData.get('sellerAdditionalStreetName'),
          cityName: formData.get('sellerCityName'),
          postalCode: formData.get('sellerPostalCode'),
          country: sellerCountry,
        },
      },
      buyer: {
        ABN: Number(formData.get('buyerABN')),
        companyName: formData.get('buyerCompanyName'),
        companyAddress: formData.get('buyerAddress'),
        address: {
          streetName: formData.get('buyerStreetName'),
          additionalStreetName: formData.get('buyerAdditionalStreetName'),
          cityName: formData.get('buyerCityName'),
          postalCode: formData.get('buyerPostalCode'),
          country: buyerCountry,
        },
      },
      invoiceItems: rows.map((row) => ({
        quantity: row.quantity,
        unitCode: row.unitCode,
        item: row.item,
        description: row.description,
        unitPrice: row.unitPrice,
        GST: row.GST,
        totalPrice: row.totalPrice,
      })),
      totalGST: totalGST,
      totalTaxable: totalTaxable,
      totalAmount: totalAmount,
      buyerVatRate: Number(vatRate),
      additionalDocuments: fileList.map((file) => ({
        fileName: file.file.name,
        fileSize: file.file.size,
        fileMimeType: file.file.type,
      })),
      extraComments: formData.get('extraComments'),
    };

    if (invoiceData.invoiceIssueDate === '') {
      setOpenError(true);
      setError('Please select an invoice issue date.');
      errorCheck = true;
    }

    for (let i = 0; i < rows.length; i++) {
      const unitCode = rows[i].unitCode;
      const itemQuantity = rows[i].quantity;
      const itemName = rows[i].item;
      const itemDescription = rows[i].description;
      const itemPrice = rows[i].unitPrice;
      const itemGST = rows[i].GST;
      const itemTotalPrice = rows[i].totalPrice;

      if (!unitCode.match(/^[A-Z]{3}$/)) {
        setOpenError(true);
        setError(
          `Invalid unit code '${unitCode}' for item ${rows[i].item}. Unit code must be a 3-letter alphanumeric combination in all uppercase.`
        );
        errorCheck = true;
        break;
      }

      if (
        itemQuantity == 0 ||
        itemName == '' ||
        itemDescription == '' ||
        itemPrice == 0 ||
        itemGST == 0 ||
        itemTotalPrice == 0
      ) {
        setOpenError(true);
        setError(`Fill out all fields for item row ${i + 1}.`);
        errorCheck = true;
        break;
      }
    }

    const { additionalDocuments, extraComments, ...filteredInvoiceData } =
      invoiceData;

    if (errorCheck) {
      return;
    } else {
      if (props.editFlag) {
        setLoadingMsg('Saving edits...');
        setLoading(true);
        const response = await axios.put(
          `http://localhost:5000/invoice/edit/${props.id}`,
          {
            name: `${formData.get('invoiceName')}.xml`,
            fields: filteredInvoiceData,
            rule: 'AUNZ_PEPPOL_1_0_10',
          },

          {
            headers: {
              Authorisation: `${props.token}`,
            },
          }
        );

        setLoading(false);

        if (response.status === 204) {
          setDialog(true);
        } else {
          alert('Unable to edit invoice');
          navigate('/invoice-management');
        }
      } else {
        setLoadingMsg('Creating invoice...');
        setLoading(true);
        try {
          const response = await axios.post(
            'http://localhost:5000/invoice/create',
            filteredInvoiceData,
            {
              headers: {
                Authorisation: `${props.token}`,
              },
            }
          );
          setLoading(false);

          if (response.status === 201) {
            const customResponse = {
              invoice: {
                data: [
                  {
                    filename: response.data.data[0].filename,
                    invoiceId: response.data.data[0].invoiceId,
                  },
                ],
              },
              type: 'GUI',

              invoiceId: response.data.data[0].invoiceId,
            };

            navigate('/invoice-creation-confirmation', {
              state: customResponse,
            });
          } else {
            setOpenError(true);
            setError('Unable to create invoice');
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

        return;
      }
    }
  };

  return (
    <>
      <SuccessDialog
        open={openDialog}
        message={'Edit Successful'}
        setOpen={setDialog}
      />
      <LoadingDialog open={loading} message={loadingMsg} />
      <Container maxWidth='lg' sx={{ marginTop: 11 }}>
        {props.editFlag ? (
          <>
            <PageHeader
              HeaderTitle={'Invoice Edit'}
              BreadcrumbDict={breadcrumbNavEdit}
            />
          </>
        ) : (
          <>
            <PageHeader
              HeaderTitle={'Invoice Creation - GUI'}
              BreadcrumbDict={breadcrumbNavGUI}
            />
          </>
        )}

        <form onSubmit={handleSubmit}>
          {/* INVOICE HEADER */}
          <Typography variant='h5' sx={{ mt: 4 }}>
            Invoice Header
          </Typography>

          <Grid container justifyContent='center' spacing={5} sx={{ mb: 2 }}>
            <Grid item xs={6}>
              <TextField
                data-cy='invoice-gui-name'
                margin='normal'
                required
                id='invoiceName'
                label='Invoice Name'
                name='invoiceName'
                autoFocus
                sx={{ width: '100%' }}
                value={invName}
                onChange={(e) => setInvName(e.target.value)}
              />
            </Grid>

            <Grid item xs={6}>
              <TextField
                data-cy='invoice-gui-number'
                margin='normal'
                required
                id='invoiceNumber'
                label='Invoice Number'
                name='invoiceNumber'
                sx={{ width: '100%' }}
                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                value={invNum}
                onChange={(e) => setInvNum(e.target.value)}
              />
            </Grid>

            <Grid item xs={12} sx={{ mt: -5 }}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker
                    label='Invoice Issue Date'
                    name='invoiceIssueDate'
                    format='yyyy-MM-dd'
                    sx={{ width: '100%' }}
                    value={date}
                    onChange={handleDateChange}
                  />
                </DemoContainer>
              </LocalizationProvider>
            </Grid>
          </Grid>

          {/* BUYER/SELLER HEADER */}
          <Grid container justifyContent='center' spacing={4} sx={{ mb: 2 }}>
            <Grid item xs={12} md={5.8}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Seller Information
              </Typography>

              <TextField
                data-cy='invoice-seller-abn'
                margin='normal'
                required
                id='sellerABN'
                label='Seller ABN'
                name='sellerABN'
                sx={{ width: '100%' }}
                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                value={sellerABN}
                onChange={(e) => setSellerABN(e.target.value)}
              />

              <TextField
                data-cy='invoice-seller-name'
                margin='normal'
                required
                id='sellerCompanyName'
                label='Company Name'
                name='sellerCompanyName'
                sx={{ width: '100%', mb: 3 }}
                value={sellerName}
                onChange={(e) => setSellerName(e.target.value)}
              />

              <Typography variant='h6' sx={{ mt: 1 }}>
                Postal Address
              </Typography>

              <TextField
                data-cy='invoice-seller-streetname'
                margin='normal'
                required
                id='sellerStreetName'
                label='Street Name'
                name='sellerStreetName'
                sx={{ width: '100%' }}
                value={sellerStreetName}
                onChange={(e) => setSellerStreetName(e.target.value)}
              />

              <TextField
                data-cy='invoice-seller-addstreetname'
                margin='normal'
                id='sellerAdditionalStreetName'
                label='Additional Street Name'
                name='sellerAdditionalStreetName'
                sx={{ width: '100%' }}
                value={sellerAddStreetName}
                onChange={(e) => setSellerAddStreetName(e.target.value)}
              />

              <TextField
                data-cy='invoice-seller-cityname'
                margin='normal'
                required
                id='sellerCityName'
                label='City Name'
                name='sellerCityName'
                sx={{ width: '100%' }}
                value={sellerCityName}
                onChange={(e) => setSellerCityName(e.target.value)}
              />

              <TextField
                data-cy='invoice-seller-pc'
                margin='normal'
                required
                id='sellerPostalCode'
                label='Postal Code'
                name='sellerPostalCode'
                sx={{ width: '100%' }}
                value={sellerCode}
                onChange={(e) => setSellerCode(e.target.value)}
              />

              <FormControl sx={{ mt: 2, width: '100%' }}>
                <InputLabel id='country-label'>Country</InputLabel>
                <Select
                  data-cy='invoice-seller-country'
                  labelId='country-label'
                  id='country'
                  required
                  name='sellerCountry'
                  value={sellerCountry}
                  onChange={handleChange}
                  label='Country'
                  // placeholder='Country'
                  sx={{ width: '100%' }}
                >
                  {countries.map((country, index) => (
                    <MenuItem key={index} value={country}>
                      {country}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {!isSmallScreen && (
              <Grid item xs={0}>
                <Divider
                  orientation='vertical'
                  sx={{ height: '90%', mt: 10 }}
                />
              </Grid>
            )}

            <Grid item xs={12} md={5.8}>
              <Typography variant='h5' sx={{ mt: 4 }}>
                Buyer Information
              </Typography>

              <TextField
                data-cy='invoice-buyer-abn'
                margin='normal'
                required
                id='buyerABN'
                label='Buyer ABN'
                name='buyerABN'
                sx={{ width: '100%' }}
                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                value={buyerABN}
                onChange={(e) => setBuyerABN(e.target.value)}
              />

              <TextField
                data-cy='invoice-buyer-name'
                margin='normal'
                required
                id='buyerCompanyName'
                label='Company Name'
                name='buyerCompanyName'
                sx={{ width: '100%', mb: 3 }}
                value={buyerName}
                onChange={(e) => setBuyerName(e.target.value)}
              />

              <Typography variant='h6' sx={{ mt: 1 }}>
                Postal Address
              </Typography>

              <TextField
                data-cy='invoice-buyer-streetname'
                margin='normal'
                required
                id='buyerStreetName'
                label='Street Name'
                name='buyerStreetName'
                sx={{ width: '100%' }}
                value={buyerStreetName}
                onChange={(e) => setBuyerStreetName(e.target.value)}
              />

              <TextField
                data-cy='invoice-buyer-addstreetname'
                margin='normal'
                id='buyerAdditionalStreetName'
                label='Additional Street Name'
                name='buyerAdditionalStreetName'
                sx={{ width: '100%' }}
                value={buyerAddStreetName}
                onChange={(e) => setBuyerAddStreetName(e.target.value)}
              />

              <TextField
                data-cy='invoice-buyer-cityname'
                margin='normal'
                required
                id='buyerCityName'
                label='City Name'
                name='buyerCityName'
                sx={{ width: '100%' }}
                value={buyerCityName}
                onChange={(e) => setBuyerCityName(e.target.value)}
              />

              <TextField
                data-cy='invoice-buyer-pc'
                margin='normal'
                required
                id='buyerPostalCode'
                label='Postal Code'
                name='buyerPostalCode'
                sx={{ width: '100%' }}
                value={buyerCode}
                onChange={(e) => setBuyerCode(e.target.value)}
              />

              <FormControl sx={{ mt: 2, width: '100%' }}>
                <InputLabel id='country-label'>Country</InputLabel>
                <Select
                  data-cy='invoice-buyer-country'
                  labelId='country-label'
                  id='country'
                  required
                  name='buyerCountry'
                  value={buyerCountry}
                  onChange={handleChange}
                  label='Country'
                  sx={{ width: '100%' }}
                >
                  {countries.map((country, index) => (
                    <MenuItem key={index} value={country}>
                      {country}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          {/* INVOICE ITEMS */}
          <Typography variant='h5' sx={{ mt: 4 }}>
            Invoice Items
          </Typography>

          <Box sx={{ width: '100%' }}>
            <Stack direction='row' spacing={1} sx={{ my: 1.5 }}>
              <Button size='small' onClick={addRow} variant='contained'>
                Add a Row
              </Button>
              {selectedRowIds.length > 0 && (
                <Button size='small' onClick={removeRow} variant='contained'>
                  Remove Selected Rows
                </Button>
              )}
            </Stack>
            <Box sx={{ height: 400, width: '100%' }}>
              <DataGrid
                rows={rows}
                columns={columns}
                checkboxSelection
                disableRowSelectionOnClick
                autoPageSize
                disableColumnMenu
                rowSelectionModel={selectedRowIds}
                onRowSelectionModelChange={(rowIds) => {
                  setSelectedRowIds(rowIds.map((id) => Number(id)));
                }}
                processRowUpdate={(newRow) => {
                  handleCellValueChange(newRow);
                  return newRow;
                }}
                onProcessRowUpdateError={(error) => {
                  console.error('Row update error:', error);
                }}
              />
            </Box>
          </Box>

          {/* MONETARY TOTALS */}
          <Stack direction='row' spacing={1} sx={{ mt: 4 }}>
            <Typography variant='h5'>Monetary Totals</Typography>
            <IconButton onClick={handleClickPopover}>
              <InfoIcon sx={{ mt: -0.25 }} />
            </IconButton>
          </Stack>
          <Popover
            id={id}
            open={openPopover}
            anchorEl={anchorEl}
            onClose={handleClosePopover}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left',
            }}
          >
            <Typography sx={{ p: 2 }}>
              GST is determined by the buyer's country.
            </Typography>
          </Popover>

          <TableContainer
            component={Paper}
            sx={{ width: isSmallScreen ? '100%' : '25vw', my: 2 }}
          >
            <Table aria-label='simple table'>
              <TableBody>
                <TableRow>
                  <TableCell>Total GST ({vatRate}%): </TableCell>
                  <TableCell align='right'>
                    ${totalGST.toLocaleString()}
                  </TableCell>
                </TableRow>

                <TableRow>
                  <TableCell>Total Taxable Amount: </TableCell>
                  <TableCell align='right'>
                    ${totalTaxable.toLocaleString()}
                  </TableCell>
                </TableRow>

                <TableRow>
                  <TableCell>Total Amount: </TableCell>
                  <TableCell align='right'>
                    ${totalAmount.toLocaleString()}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>

          <Box textAlign='center'>
            <Button
              data-cy='confirm-gui'
              type='submit'
              startIcon={<SaveIcon />}
              variant='contained'
              sx={{
                padding: '15px',
                my: 6,
              }}
            >
              Finish & Save Invoice
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

export default CreationGUI;
