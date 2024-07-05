import json
import re
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring, fromstring

class ConversionService():
    """
    Conversion service for converting data into an XML format

    Methods:
        json_to_xml(self, json_str)
            - Converts a JSON string into an XML string
        _build_xml_tree_from_json
            - Recursively builds an XML by performing a DFS
        _build_xml_from_json
            - Loops through all key-value pairs within a JSON

    """
    def json_to_xml(self, json_str):
        '''
        Converts a JSON string into an XML string

        Arguments:
            json_str: string
                - A string containing a JSON object.

                Format requirements:
                    - { "ID": "Hello" } => <ID>Hello</ID>
                    - { "ID": { "attribute1": "Hello", value="There" } } => <ID attribute1="Hello">There</ID>
                    - { "ID": { "Profile": "Hello" } } => <ID><Profile>Hello</Profile></ID>

        Raises:
            - ValueError: If the json_str cannot be converted to a Python dictionary

        Return Value:
            Returns a string containing the converted XML
        '''
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")

        root = Element('Invoice', {
            "xmlns:cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "xmlns:cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "xmlns":"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
        })
        
        # Set essential sub-elements for a UBL
        customisationIdElement = SubElement(root, "cbc:CustomizationID")
        customisationIdElement.text = "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0"
        profileIdElement = SubElement(root, "cbc:ProfileID")
        profileIdElement.text = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"

        self._build_xml_from_json(root, data)

        # Prepend the XML decl
        xml_str = tostring(root, encoding='unicode')
        xml_str = f'<?xml version="1.0" encoding="UTF-8"?>{xml_str}'
        
        return xml_str
    
    def xml_to_json(self, xml_str):
        json = {}

        element_tree = ElementTree(fromstring(xml_str))
        self._build_json_from_xml(element_tree.getroot(), json)
        
        json = json["Invoice"]
        json.pop("CustomizationID")
        json.pop("ProfileID")

        return json

    def _extract_tag_from_xml(self, element):
        match = re.search(r"\{.+\}(.+)", element.tag)
        if not match:
            raise ValueError("Invalid XML")
        
        return match.group(1) 

    def _build_json_from_xml(self, element, json):
        element_tag = self._extract_tag_from_xml(element)
        if len(element) > 0:
            if element_tag in json:
                if not isinstance(json[element_tag], list):
                    json[element_tag] = [json[element_tag]]
                json[element_tag].append({})
            else:
                json[element_tag] = {}

            for subelement in element:
                subelement_tag = self._extract_tag_from_xml(subelement)

                json_element = json[element_tag]
                if isinstance(json[element_tag], list):
                    json_element = json_element[len(json[element_tag]) - 1]

                if subelement.attrib:
                    json_element[subelement_tag] = subelement.attrib
                elif len(subelement) == 0:
                    json_element[subelement_tag] = subelement.text 

                self._build_json_from_xml(subelement, json_element)
        else:
            if isinstance(json[element_tag], dict):
                json[element_tag]["value"] = element.text
            else:
                json[element_tag] = element.text


    def _build_xml_tree_from_json(self, element, key, value):
        '''
        Recursively builds an XML by performing a DFS
        This function does not return any value

        Arguments:
            element: Element
                - The current element being recursed through
            key: string              
                - The string repr of the current element 
            value: Union[dict, str]    
                - The contents of the current element
                - If dict:
                    - Current element contains child elements OR attributes
                    I.e. <Parent><Child></Child></Parent> OR <Parent attributes="hello">...</Parent>
                - If str:
                    - Current element only has a value
                    I.e. <Parent>Hello</Parent>
        '''
        # Capitalised keys in a UBL2.1 are XML tags
        # i.e. <Hello></Hello>
        is_xml_tag = key[0].isupper()

        namespace = "cbc"
        # Sub-element is an XML-tag AND contains attributes OR child elements
        if is_xml_tag and isinstance(value, dict):
            # Sub-element contains no attributes BUT has more child elements
            if not value.get("value"):
                namespace = "cac"

            # Set the sub-element as a child of the element and recurses down the dictionary   
            subelement = SubElement(element, f"{namespace}:{key}")
            self._build_xml_from_json(subelement, value)
        # Sub-element is an XML-tag AND contains no attributes or child elements
        elif is_xml_tag and isinstance(value, str):
            subelement = SubElement(element, f"{namespace}:{key}")
            subelement.text = value
        # Set the element's value
        elif key == "value":
            element.text = value
        # Set the element attributes
        else:
            element.set(key, value)

    def _build_xml_from_json(self, element, data):
        '''
        Loops through all key-value pairs within a JSON
        This function does not return any value

        Arguments:
            element: Element
                - The current element being recursed through
            data: dict
                - A dictionary containing the JSON input for converting to XML
        '''
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    self._build_xml_tree_from_json(element, key, item)
            else:
                self._build_xml_tree_from_json(element, key, value)

xml_from_json_str_1 = '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>Invoice03</cbc:ID><cbc:IssueDate>2022-07-31</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>Simple solar plan</cbc:BuyerReference><cac:InvoicePeriod><cbc:StartDate>2022-06-15</cbc:StartDate><cbc:EndDate>2022-07-15</cbc:EndDate></cac:InvoicePeriod><cac:BillingReference><cac:InvoiceDocumentReference><cbc:ID>Invoice01</cbc:ID><cbc:IssueDate>2022-07-29</cbc:IssueDate></cac:InvoiceDocumentReference></cac:BillingReference><cac:AdditionalDocumentReference><cbc:ID>Invoice03.pdf</cbc:ID><cac:Attachment><cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice03.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject></cac:Attachment></cac:AdditionalDocumentReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PostalAddress><cbc:CityName>Harrison</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyIdentification><cbc:ID>AccountNumber123</cbc:ID></cac:PartyIdentification><cac:PostalAddress><cbc:StreetName>100 Queen Street</cbc:StreetName><cbc:CityName>Sydney</cbc:CityName><cbc:PostalZone>2000</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName><cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID></cac:PartyLegalEntity><cac:Contact><cbc:Name>Lisa Johnson</cbc:Name></cac:Contact></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">-159.43</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">-159.43</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">-159.43</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">-175.37</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">-175.37</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>1</cbc:ID><cbc:InvoicedQuantity unitCode="KWH">-325.2</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-129.04</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>2</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>3</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'

cs = ConversionService()
cs.xml_to_json(xml_from_json_str_1)