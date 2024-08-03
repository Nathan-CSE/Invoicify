import {
  Box,
  Container,
  Stack,
  Typography,
} from '@mui/material';
import useAuth from '../helpers/useAuth';
import PageHeader from '../components/PageHeader';

function DocPage(props: { token: string }) {
  useAuth(props.token);
  const breadcrumbNav = {
    'Dashboard': '/dashboard',
    'Documentation': '/documentation'
  }

  return (
    <Container maxWidth='lg' sx={{ mt: 11 }}>

      <PageHeader HeaderTitle={'Documentation'} BreadcrumbDict={breadcrumbNav} />

      <Stack spacing={3} sx={{ mt: 5, mb: 10 }}>
        <Typography variant='h4' gutterBottom>
          What is UBL2.1 (Universal Business Language) and its importance
        </Typography>
        <Typography variant='body1' gutterBottom>
          UBL 2.1 is widely used in electronic invoicing to standardise the
          format and ensure interoperability between different systems. Here are
          some key aspects of UBL 2.1 in invoicing:
        </Typography>
        <Typography variant='body1' gutterBottom>
          <ul>
            <Stack spacing={2}>
              <li>
                Standardised Format: UBL 2.1 provides a consistent XML-based
                format for invoices, which helps in reducing errors and
                improving efficiency in processing invoices
              </li>
              <li>
                Compliance: Many countries require the use of UBL 2.1 for
                business-to-government electronic invoicing, ensuring compliance
                with local regulations
              </li>
              <li>
                Automation: By using UBL 2.1, businesses can automate the
                invoicing process, from creation to delivery and payment,
                reducing manual intervention
              </li>
              <li>
                Customisation: UBL 2.1 can be tailored to meet specific business
                needs, allowing for the inclusion of additional information as
                required
              </li>
            </Stack>
          </ul>
        </Typography>
        <Typography variant='body1' gutterBottom>
          This website provides a tool to create UBL2.1 XMLs via Json, Validate
          UBL2.1 XMLs against the ANZ PEPPOL ruleset, and send the invoices to a
          designated end user.
        </Typography>
        <Typography variant='h4' gutterBottom>
          Invoice Creation
        </Typography>
        <Typography variant='body1' gutterBottom>
          This website will provide 2 ways of creating an UBL2.1 XML for
          invoices. To reduce the barrier for our customers to use the system,
          our customers should be able to convert data from their current system
          to standard e-invoices in batches.
          <ol>
            <Stack spacing={2}>
              <li>
                <Box sx={{ fontWeight: 'bold' }}>Creation via a form</Box>
                <Box>
                  We offer a service for our end users to create an invoice
                  based on predetermined minimum fields that are required for a
                  valid UBL invoice to be created. This option allows our end
                  users to create an invoice when they don’t have a PDF or JSON
                  file formatted UBL
                </Box>
              </li>
              <li>
                <Box sx={{ fontWeight: 'bold' }}>
                  Creation via uploading JSON
                </Box>
                <Box>
                  The second service we offer to our end users for creation is
                  the ability to create an invoice with a JSON file. By
                  uploading the file(s), we are able to create and generate the
                  invoice in the UBL2.1 XML invoice format. This creation
                  feature will allow our users to upload and create multiple
                  invoices at once
                </Box>
              </li>
            </Stack>
          </ol>
        </Typography>
        <Typography variant='h4' gutterBottom>
          Invoice Validation
        </Typography>
        <Typography variant='body1' gutterBottom>
          This service creates a report outlining any validation errors
          according to Australian rules. In order to maintain an efficient
          system, it is essential that the invoices are validated based on the
          rules employed by a governing entity. The rules can be found in the
          official ATO github repository:
          <a href='https://github.com/A-NZ-PEPPOL/A-NZ-PEPPOL-BIS-3.0/tree/master/Specifications'>
            {' '}
            Here{' '}
          </a>
          . Latest Details of Validation rules can be found in Appendix A and B
          of the document “Specifications/A-NZ_Invoice_Extension_versionX.docx”
          in the ATO GitHub repository.
          <Typography variant='body1' gutterBottom sx={{ mt: 3 }}>
            This service offers the validation process via uploading their own
            UBL2.1 XMLs or choosing to validate an existing invoice in the
            system for the user.
          </Typography>
          The validation microservice has four components:
          <ul>
            <Stack spacing={2}>
              <li>
                Validating Wellformedness (Checking if the input is valid and
                the file itself has valid contents)
              </li>
              <li>
                Syntax Rules (Validates EN16931 business rules) (Appendix B, BR
                Rules)
              </li>
              <li>
                PEPPOL rules (Validates Specific AUNZ business rules) (Appendix
                B, PEPPOL Rules)
              </li>
              <li>Schema Validation (Validates the schema of the invoice)</li>
            </Stack>
          </ul>
        </Typography>
        <Typography variant='h4' gutterBottom>
          Invoice Sending
        </Typography>
        <Typography variant='body1' gutterBottom>
          After invoices are generated, the web service enables distribution of
          the invoices to corresponding recipients. The invoice is sent via
          email. The email Input will conform to the UBL format in the
          recommended format. (i.e. The UBL2.1 XMLs will need to pass the
          invoice validation process of our website.) The service also offers
          the ability to upload and send PDFs/ Jsons straight away, skipping the
          validation process.
          <Typography variant='body1' gutterBottom sx={{ mt: 3 }}>
            To convert from a JSON to an XML, you must comply with the following
            formatting rules:
          </Typography>
          <ol>
            <Stack spacing={2}>
              <li>
                <Box sx={{ fontWeight: 'bold' }}>If capitalised JSON key</Box>
                <Box>
                  <ul>
                    <li>XML tag = JSON key</li>
                    <li>If typeof JSON value == string</li>
                    <ul>
                      <li>XML tag’s value = JSON value</li>
                    </ul>
                  </ul>
                </Box>
              </li>
              <li>
                <Box sx={{ fontWeight: 'bold' }}>
                  If non-capitalised JSON key
                </Box>
                <Box>
                  <ul>
                    <li>If JSON key == “@value”</li>
                    <ul>
                      <li>XML tag’s value = JSON value</li>
                    </ul>
                    <li>Else</li>
                    <ul>
                      <li>XML attribute = JSON key</li>
                      <li>XML attribute value = JSON value</li>
                    </ul>
                  </ul>
                </Box>
              </li>
            </Stack>
          </ol>
        </Typography>
      </Stack>
    </Container>
  );
}

export default DocPage;
