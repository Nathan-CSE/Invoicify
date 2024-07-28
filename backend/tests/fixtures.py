import pytest

from app import create_app
from models import Invoice, User
from src.services.utils import salt_and_hash, db_insert

@pytest.fixture
def client():
    app = create_app(":memory:")
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def user(client):
    user = User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM")
    
    db_insert(user)
    return user

@pytest.fixture
def user_2(client):
    user = User(email="abc2@gmail.com", password=salt_and_hash("abc2"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiYzJAZ21haWwuY29tIn0.Sz2dvn-pLfOtbpDEoFO7Mooc9xLL4fTYhMCoyeHBnKY")
    
    db_insert(user)
    return user

@pytest.fixture
def invoice(user):
    invoice = Invoice(
<<<<<<< Updated upstream
        name="test-invoice.xml", 
        fields={"ID":"Invoice03","IssueDate":"2022-07-31","InvoiceTypeCode":"380","Note":"Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.","DocumentCurrencyCode":"AUD","BuyerReference":"Simple solar plan","InvoicePeriod":{"StartDate":"2022-06-15","EndDate":"2022-07-15"},"BillingReference":{"InvoiceDocumentReference":{"ID":"Invoice01","IssueDate":"2022-07-29"}},"AdditionalDocumentReference":{"ID":"Invoice03.pdf","Attachment":{"EmbeddedDocumentBinaryObject":{"mimeCode":"application/pdf","filename":"Invoice03.pdf","@value":"UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz"}}},"AccountingSupplierParty":{"Party":{"EndpointID":{"schemeID":"0151","@value":"47555222000"},"PostalAddress":{"CityName":"Harrison","PostalZone":"2912","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Grey Roo Energy","CompanyID":{"schemeID":"0151","@value":"47555222000"}}}},"AccountingCustomerParty":{"Party":{"EndpointID":{"schemeID":"0151","@value":"47555222000"},"PartyIdentification":{"ID":"AccountNumber123"},"PostalAddress":{"StreetName":"100 Queen Street","CityName":"Sydney","PostalZone":"2000","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Trotters Incorporated","CompanyID":{"schemeID":"0151","@value":"91888222000"}},"Contact":{"Name":"Lisa Johnson"}}},"TaxTotal":{"TaxAmount":{"currencyID":"AUD","@value":"-15.94"},"TaxSubtotal":{"TaxableAmount":{"currencyID":"AUD","@value":"-159.43"},"TaxAmount":{"currencyID":"AUD","@value":"-15.94"},"TaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}}},"LegalMonetaryTotal":{"LineExtensionAmount":{"currencyID":"AUD","@value":"-159.43"},"TaxExclusiveAmount":{"currencyID":"AUD","@value":"-159.43"},"TaxInclusiveAmount":{"currencyID":"AUD","@value":"-175.37"},"PayableAmount":{"currencyID":"AUD","@value":"-175.37"}},"InvoiceLine":[{"ID":"1","InvoicedQuantity":{"unitCode":"KWH","@value":"-325.2"},"LineExtensionAmount":{"currencyID":"AUD","@value":"-129.04"},"Item":{"Name":"Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","@value":"0.3968"}}},{"ID":"2","InvoicedQuantity":{"unitCode":"DAY","@value":"-31"},"LineExtensionAmount":{"currencyID":"AUD","@value":"-30.39"},"Item":{"Name":"Adjustment - reverse prior Supply charge","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","@value":"0.9803"}}}]},
=======
        name="test-invoice", 
        fields={"ID":"Invoice03","IssueDate":"2022-07-31","InvoiceTypeCode":"380","Note":"Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.","DocumentCurrencyCode":"AUD","BuyerReference":"Simple solar plan","InvoicePeriod":{"StartDate":"2022-06-15","EndDate":"2022-07-15"},"BillingReference":{"InvoiceDocumentReference":{"ID":"Invoice01","IssueDate":"2022-07-29"}},"AdditionalDocumentReference":{"ID":"Invoice03.pdf","Attachment":{"EmbeddedDocumentBinaryObject":{"mimeCode":"application/pdf","filename":"Invoice03.pdf","value":"UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz"}}},"AccountingSupplierParty":{"Party":{"EndpointID":{"schemeID":"0151","value":"47555222000"},"PostalAddress":{"CityName":"Harrison","PostalZone":"2912","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Grey Roo Energy","CompanyID":{"schemeID":"0151","value":"47555222000"}}}},"AccountingCustomerParty":{"Party":{"EndpointID":{"schemeID":"0151","value":"47555222000"},"PartyIdentification":{"ID":"AccountNumber123"},"PostalAddress":{"StreetName":"100 Queen Street","CityName":"Sydney","PostalZone":"2000","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Trotters Incorporated","CompanyID":{"schemeID":"0151","value":"91888222000"}},"Contact":{"Name":"Lisa Johnson"}}},"TaxTotal":{"TaxAmount":{"currencyID":"AUD","value":"-15.94"},"TaxSubtotal":{"TaxableAmount":{"currencyID":"AUD","value":"-159.43"},"TaxAmount":{"currencyID":"AUD","value":"-15.94"},"TaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}}},"LegalMonetaryTotal":{"LineExtensionAmount":{"currencyID":"AUD","value":"-159.43"},"TaxExclusiveAmount":{"currencyID":"AUD","value":"-159.43"},"TaxInclusiveAmount":{"currencyID":"AUD","value":"-175.37"},"PayableAmount":{"currencyID":"AUD","value":"-175.37"}},"InvoiceLine":[{"ID":"1","InvoicedQuantity":{"unitCode":"KWH","value":"-325.2"},"LineExtensionAmount":{"currencyID":"AUD","value":"-129.04"},"Item":{"Name":"Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","value":"0.3968"}}},{"ID":"2","InvoicedQuantity":{"unitCode":"DAY","value":"-31"},"LineExtensionAmount":{"currencyID":"AUD","value":"-30.39"},"Item":{"Name":"Adjustment - reverse prior Supply charge","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","value":"0.9803"}}}]},
>>>>>>> Stashed changes
        rule="AUNZ_PEPPOL_1_0_10",
        user_id=user.id,
        is_ready=False
    )
    
    db_insert(invoice)
    return invoice

@pytest.fixture
def invoice_2(user):
    invoice = Invoice(
        name="test-invoice2.xml", 
        fields={
            "Name": "Invoice 2",
            "Fields": {
                "yo": "Yo"
            },
        },
        rule="AUNZ_PEPPOL_1_0_10",
        user_id=user.id,
        completed_ubl="blahblahlba",
        is_ready=True
    )
    
    db_insert(invoice)
    return invoice
    