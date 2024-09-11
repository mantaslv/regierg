import pytest
import json
from regierg.services.erg_parser import serialize_erg_data
from regierg.tests.erg_test_cases import test_cases
from datetime import datetime

def case_id(case, idx):
    session_name = case["expected_output"]["session_name"]
    return f"case{idx} - {session_name}"

@pytest.mark.parametrize("case", test_cases, ids=[case_id(case, idx) for idx, case in enumerate(test_cases)])
def test_serialize_erg_data(case):
    input_data = case["input_data"]
    expected_output = case["expected_output"]

    result = serialize_erg_data(input_data)
    result_json = json.loads(result)

    assert result_json == expected_output
