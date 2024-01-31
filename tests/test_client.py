import pytest
import requests_mock
import json
from requests.exceptions import HTTPError
from pfsense_api_client.client import ClientConfig, ClientBase, APIResponse, load_client_config

# Example test configuration
test_config = {
    "username": "test_user",
    "password": "test_pass",
    "hostname": "test.example.com",
    "mode": "jwt",
    "jwt": "test_jwt_token"
}


# Test ClientBase Initialization
def test_client_base_initialization():
    config = ClientConfig(**test_config)
    client = ClientBase(config=config)
    assert client.config.username == "test_user"
    assert client.config.password == "test_pass"
    assert client.config.hostname == "test.example.com"


# Test ClientBase with Mocked Request
def test_client_base_call():
    with requests_mock.Mocker() as m:
        # Mocking a GET request
        test_url = "https://test.example.com/test"
        m.get(test_url, json={"status": "success", "data": "test_data"})

        config = ClientConfig(**test_config)
        client = ClientBase(config=config)
        response = client.call("/test")

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["data"] == "test_data"


# Test ClientBase with Config File Loading
def test_client_base_config_loading(tmp_path):
    # Create a temporary config file
    config_file = tmp_path / "config.json"
    with config_file.open("w") as f:
        json.dump(test_config, f)

    config = load_client_config(str(config_file))
    client = ClientBase(config=config)
    assert client.config.username == "test_user"
    assert client.config.hostname == "test.example.com"


@pytest.mark.parametrize("method, mock_method", [
    ("GET", "get"),
    ("POST", "post"),
    ("PUT", "put"),
    ("DELETE", "delete")
])
def test_client_base_http_methods(method, mock_method):
    with requests_mock.Mocker() as m:
        test_url = f"https://test.example.com/test_{method.lower()}"
        getattr(m, mock_method)(test_url, json={"method": method})

        config = ClientConfig(**test_config)
        client = ClientBase(config=config)
        response = client.call(f"/test_{method.lower()}", method=method)

        assert response.status_code == 200
        assert response.json()["method"] == method

# Test ClientBase error handling
def test_client_base_error_handling():
    with requests_mock.Mocker() as m:
        test_url = "https://test.example.com/error"
        m.get(test_url, status_code=400, json={"error": "Bad Request"})

        config = ClientConfig(**test_config)
        client = ClientBase(config=config)
        with pytest.raises(HTTPError):
            response = client.call("/error")
            response.raise_for_status()

# Test ClientBase call_api method
def test_client_base_call_api():
    with requests_mock.Mocker() as m:
        test_url = "https://test.example.com/api"
        m.get(test_url, json={"status": "success", "data": {"key": "value"}})

        config = ClientConfig(**test_config)
        client = ClientBase(config=config)
        api_response = client.call_api("/api")

        assert isinstance(api_response, APIResponse)
        assert api_response.status == "success"
        assert api_response.data == {"key": "value"}


