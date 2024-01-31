import pytest
from pydantic import ValidationError
from pfsense_api_client.client.types import PFSenseConfig, APIResponse, APIResponseDict, APIResponseList

# Test for PFSenseConfig
def test_pfsense_config_valid():
    config = PFSenseConfig(
        username="user",
        password="pass",
        hostname="example.com"
    )
    assert config.username == "user"
    assert config.password == "pass"
    assert config.hostname == "example.com"
    assert config.port == 443  # Default value

def test_pfsense_config_invalid():
    with pytest.raises(ValidationError):
        PFSenseConfig(hostname="example.com")

# Test for APIResponse
def test_apiresponse_valid():
    response_data = {
        "status": "success",
        "code": 200,
        "return": 0,  # Access using the alias
        "message": "OK",
        "data": {"key": "value"}
    }
    response = APIResponse(**response_data)

    assert response.status == "success"
    assert response.code == 200
    assert response.return_code == 0  # Access using the actual field name
    assert response.message == "OK"
    assert response.data == {"key": "value"}



def test_apiresponse_invalid_code():
    with pytest.raises(ValidationError):
        response_data = {
            "status": "error",
            "code": 999,  # Invalid code
            "return": 0,  # Access using the alias
            "message": "Error",
            "data": None
        }
        APIResponse(**response_data)

# Test for APIResponseDict
def test_apiresponse_dict():
    response_data = {
        "status": "success",
        "code": 200,
        "return": 0,  # Access using the alias
        "message": "OK",
        "data": {"key": "value"}
    }
    response = APIResponse(**response_data)
    assert response.data == {"key": "value"}

# Test for APIResponseList
def test_apiresponse_list():
    response_data = {
        "status": "success",
        "code": 200,
        "return": 0,  # Access using the alias
        "message": "OK",
        "data": ["item1", "item2"]
    }
    response = APIResponse(**response_data)
    assert response.data == ["item1", "item2"]
