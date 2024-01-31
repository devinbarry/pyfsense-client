import pytest
from pydantic import ValidationError
from pfsense_api_client.client import ClientConfig, APIResponse

# Test for ClientConfig
def test_pfsense_config_username_and_pass():
    config = ClientConfig(
        username="user",
        password="pass",
        hostname="example.com"
    )
    assert config.username == "user"
    assert config.password == "pass"
    assert config.hostname == "example.com"
    assert config.port == 443  # Default value

def test_pfsense_config_token():
    config = ClientConfig(
        mode="api_token",
        hostname="example.com",
        client_id="client_id",
        client_token="client_token",
    )
    assert config.username is None
    assert config.password is None
    assert config.hostname == "example.com"
    assert config.port == 443  # Default value
    assert config.mode == "api_token"
    assert config.client_id == "client_id"
    assert config.client_token == "client_token"

def test_pfsense_config_invalid():
    with pytest.raises(ValidationError):
        ClientConfig(hostname="example.com")

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
