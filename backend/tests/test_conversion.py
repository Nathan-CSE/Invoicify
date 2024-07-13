import pytest
import json
from xml.etree.ElementTree import ParseError

from src.services.conversion import ConversionService
from tests.data import TEST_DATA

cs = ConversionService()

def test_json_conversion_to_xml_successful():
    xml_str = cs.json_to_xml(TEST_DATA["JSON_STR_1"], "AUNZ_PEPPOL_1_0_10")

    assert xml_str == TEST_DATA["XML_STR_1"]

def test_json_conversion_to_xml_invalid_json():
    with pytest.raises(ValueError):
        cs.json_to_xml(TEST_DATA["INVALID_JSON_STR_1"], "blah blah")

def test_json_conversion_to_xml_invalid_formatted_json():
    #TODO
    pass

def test_json_conversion_to_xml_invalid_rule():
    with pytest.raises(NotImplementedError):
        cs.json_to_xml(TEST_DATA["JSON_STR_1"], "blah blah")

def test_xml_conversion_to_json_successful():
    json_str = cs.xml_to_json(TEST_DATA["XML_STR_1"])

    assert json.loads(json_str) == json.loads(TEST_DATA["JSON_STR_1"])

def test_xml_conversion_to_json_invalid_xml():
    with pytest.raises(ParseError):
        cs.xml_to_json(TEST_DATA["INVALID_XML_STR_1"])