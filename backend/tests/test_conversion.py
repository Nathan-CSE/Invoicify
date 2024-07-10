import pytest
import json

from src.services.conversion import ConversionService
from tests.const_data import json_str_1, xml_str_1

cs = ConversionService()

def test_json_conversion_to_xml_successful():
    xml_str = cs.json_to_xml(json_str_1, "AUNZ_PEPPOL_1_0_10")

    assert xml_str == xml_str_1

def test_json_conversion_to_xml_invalid_rule():
    with pytest.raises(NotImplementedError):
        cs.json_to_xml(json_str_1, "blah blah")

def test_xml_conversion_to_json_successful():
    json_str = cs.xml_to_json(xml_str_1)

    assert json.loads(json_str) == json.loads(json_str_1)

