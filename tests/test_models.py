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
    response = APIResponse(
        status="success",
        code=200,
        message="OK",
        data={"key": "value"}
    )
    assert response.status == "success"
    assert response.code == 200
    assert response.message == "OK"
    assert response.data == {"key": "value"}

def test_apiresponse_invalid_code():
    with pytest.raises(ValidationError):
        APIResponse(
            status="error",
            code=999,  # Invalid code
            message="Error",
            data=None
        )

# Test for APIResponseDict
def test_apiresponse_dict():
    response = APIResponseDict(
        status="success",
        code=200,
        message="OK",
        data={"key": "value"}
    )
    assert response.data == {"key": "value"}

# Test for APIResponseList
def test_apiresponse_list():
    response = APIResponseList(
        status="success",
        code=200,
        message="OK",
        data=["item1", "item2"]
    )
    assert response.data == ["item1", "item2"]
