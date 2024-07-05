from xml.etree.ElementTree import tostring, fromstring

from src.services.conversion import ConversionService
from tests.const_data import json_str_1, xml_from_json_str_1

def test_json_conversion_to_xml_successful():
    cs = ConversionService()
    xml_str = cs.json_to_xml(json_str_1)

    assert xml_str == xml_from_json_str_1

