import json
import re

from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring, fromstring, ParseError

class ConversionService():
    """
    Conversion service for converting data into an XML format

    Attributes:
        _rules_map: Dict[Dict[String, String]]
            - Contains the customizationID and profileID values for each ruleset

    Methods:
        xml_to_json(self, xml_str)
            - Converts an XML string into a JSON string
        json_to_xml(self, json_str, rule_chosen)
            - Converts a JSON string into an XML string for a specific rule provided
        _extract_tag_from_xml(self, element)
            - Extracts only the tag from an XML element
        _build_json_from_xml
            - Recursively builds a JSON 
        _build_xml_tree_from_json
            - Recursively builds an XML by performing a DFS
        _build_xml_from_json
            - Loops through all key-value pairs within a JSON
    """

    _rules_map = {
        "AUNZ_PEPPOL_1_0_10": {
            "cbc:CustomizationID": "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0",
            "cbc:ProfileID": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
        },
        "AUNZ_PEPPOL_SB_1_0_10": {
            "cbc:CustomizationID": "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:selfbilling:international:aunz:3.0",
            "cbc:ProfileID": "urn:fdc:peppol.eu:2017:poacc:selfbilling:01:1.0"
        }
    }

    def json_to_xml(self, json_str, rule_chosen):
        '''
        Converts a JSON string into an XML string

        Arguments:
            json_str: string
                - A string containing a JSON object.
                Format requirements:
                    - { "ID": "Hello" } => <ID>Hello</ID>
                    - { "ID": { "attribute1": "Hello", value="There" } } => <ID attribute1="Hello">There</ID>
                    - { "ID": { "Profile": "Hello" } } => <ID><Profile>Hello</Profile></ID>
            rule_chosen: string
                - The specific UBL rule to create the XML against
                - Available values: 
                    - AUNZ_PEPPOL_1_0_10, 
                    - AUNZ_PEPPOL_SB_1_0_10, 

        Raises:
            - ValueError: If the json_str cannot be converted to a Python dictionary
            - NotImplementedError: If the provided rule_chosen does not exist in the _rules_map

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
        
        rule = self._rules_map.get(rule_chosen)
        if not rule:
            raise NotImplementedError("Rule has not been added to conversion service")
        
        # Set essential sub-elements for a UBL
        for tag in rule:
            element = SubElement(root, tag)
            element.text = rule[tag]


        self._build_xml_from_json(root, data)

        # Prepend the XML decl
        xml_str = tostring(root, encoding='unicode')
        xml_str = f'<?xml version="1.0" encoding="UTF-8"?>{xml_str}'
        
        return xml_str
    
    def xml_to_json(self, xml_str):
        '''
        Converts a XML string into an JSON string

        Arguments:
            xml_str: string
                - A string containing the XML. 

        Raises:
            - ValueError: If the XML element does not contain a tag
            - ParseError: If the XML is formatted invalidly

        Return Value:
            Returns a string containing the converted JSON
        '''
        fields = {}

        try:
            element_tree = ElementTree(fromstring(xml_str))
            self._build_json_from_xml(element_tree.getroot(), fields)
        except (ParseError, ValueError) as err:
            raise err
        
        fields = fields["Invoice"]
        fields.pop("CustomizationID")
        fields.pop("ProfileID")

        return json.dumps(fields)

    def _extract_tag_from_xml(self, element):
        # Format: {namespace}:tag
        match = re.search(r"\{.+\}(.+)", element.tag)
        if not match:
            raise ValueError("Invalid XML")
        
        return match.group(1) 

    def _build_json_from_xml(self, element, fields):
        element_tag = self._extract_tag_from_xml(element)
        # Contains children elements
        if len(element) > 0:
            # Duplicate element_tag
            if element_tag in fields:
                # First time visiting duplicate
                if not isinstance(fields[element_tag], list):
                    fields[element_tag] = [fields[element_tag]]
                # Append otherwise
                fields[element_tag].append({})
            else:
                # No duplicate
                fields[element_tag] = {}

            for subelement in element:
                subelement_tag = self._extract_tag_from_xml(subelement)

                field_element = fields[element_tag]
                if isinstance(field_element, list):
                    # Move to the most recent element in the list
                    field_element = field_element[len(field_element) - 1]

                # Contains attributes, add them
                if subelement.attrib:
                    field_element[subelement_tag] = subelement.attrib
                # No children elements or attributes
                elif len(subelement) == 0:
                    field_element[subelement_tag] = subelement.text 

                self._build_json_from_xml(subelement, field_element)
        else:
            # Has attributes and a value 
            if isinstance(fields[element_tag], dict):
                fields[element_tag]["value"] = element.text
            # Has only a value
            else:
                fields[element_tag] = element.text


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