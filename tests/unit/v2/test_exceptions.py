import requests
from pyfsense_client.v2.exceptions import APIError, AuthenticationError, ValidationError


def test_api_error():
    err = APIError("Something went wrong")
    assert str(err) == "Something went wrong"
    assert err.response is None


def test_api_error_with_response():
    mock_resp = requests.Response()
    mock_resp.status_code = 500
    err = APIError("Server Error", mock_resp)
    assert str(err) == "Server Error"
    assert err.response == mock_resp


def test_authentication_error():
    err = AuthenticationError("401 Unauthorized")
    assert str(err) == "401 Unauthorized"


def test_validation_error():
    err = ValidationError("400 Bad Request")
    assert str(err) == "400 Bad Request"
