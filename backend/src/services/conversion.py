import json
from xml.etree.ElementTree import Element, SubElement, tostring

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