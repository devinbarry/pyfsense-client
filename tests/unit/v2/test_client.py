import pytest
import requests
from unittest.mock import patch, MagicMock

from pyfsense_client.v2 import (
    PfSenseV2Client,
    ClientConfig,
    APIError,
    AuthenticationError,
    ValidationError,
    FirewallAliasCreate,
    FirewallAliasUpdate,
)

@pytest.fixture
def client_config():
    """Fixture for a basic ClientConfig."""
    return ClientConfig(
        host="https://example-pfsense",
        verify_ssl=False,
        timeout=5,
        username="admin",
        password="pfsense",
        api_key=None,
        jwt_token=None
    )

@pytest.fixture
def pf_client(client_config):
    """Fixture that returns a PfSenseV2Client with the above config."""
    return PfSenseV2Client(client_config)

#
# Tests for the PfSenseV2Client initialization
#

def test_pf_client_initialization(client_config):
    client = PfSenseV2Client(client_config)
    assert client.base_url == "https://example-pfsense"
    assert client._session.verify is False
    assert client._default_timeout == 5
    # By default, no extra auth headers should be set if no api_key / jwt_token
    assert "X-API-Key" not in client._session.headers
    assert "Authorization" not in client._session.headers

def test_pf_client_initialization_with_key(client_config):
    client_config.api_key = "12345"
    client = PfSenseV2Client(client_config)
    assert client._session.headers["X-API-Key"] == "12345"

def test_pf_client_initialization_with_jwt(client_config):
    client_config.jwt_token = "my-jwt-token"
    client = PfSenseV2Client(client_config)
    assert client._session.headers["Authorization"] == "Bearer my-jwt-token"

#
# Tests for _handle_response
#

@patch("requests.Response.raise_for_status")
def test_handle_response_200(mock_raise_for_status, pf_client):
    # Mock a successful response
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "code": 200,
        "status": "success",
        "message": "OK",
        "data": {"foo": "bar"}
    }

    result = pf_client._handle_response(mock_response)
    assert result.code == 200
    assert result.status == "success"
    assert result.data == {"foo": "bar"}

def test_handle_response_401(pf_client):
    # Create a mock response whose raise_for_status() immediately throws 401
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Error")

    # We expect the client to raise our custom AuthenticationError
    with pytest.raises(AuthenticationError) as excinfo:
        pf_client._handle_response(mock_response)
    assert "Authentication failed (401)" in str(excinfo.value)

def test_handle_response_400(pf_client):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Error")

    with pytest.raises(ValidationError) as excinfo:
        pf_client._handle_response(mock_response)
    assert "Request validation failed (400)" in str(excinfo.value)

def test_handle_response_500(pf_client):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Error")

    # This should raise a generic APIError (status != 401 or 400).
    with pytest.raises(APIError) as excinfo:
        pf_client._handle_response(mock_response)
    # Confirm it's the "API request failed" path, not a JSON parse issue
    assert "API request failed" in str(excinfo.value)

def test_handle_response_bad_json(pf_client):
    """Test JSON parsing errors raise APIError."""
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json.side_effect = ValueError("No JSON object could be decoded")

    with pytest.raises(APIError) as excinfo:
        pf_client._handle_response(mock_response)
    assert "Failed to parse JSON response" in str(excinfo.value)

#
# Tests for _request
#

@patch("requests.Session.request")
def test_request_success(mock_request, pf_client):
    # Mock a response
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "code": 200,
        "status": "success",
        "message": "OK",
        "data": {"foo": "bar"}
    }
    mock_request.return_value = mock_response

    resp = pf_client._request("GET", "/test-endpoint")
    assert resp.code == 200
    assert resp.data == {"foo": "bar"}
    mock_request.assert_called_once_with(
        method="GET",
        url="https://example-pfsense/test-endpoint",
        params=None,
        json=None,
        timeout=pf_client._default_timeout
    )

#
# Tests for authenticate_jwt
#

@patch.object(PfSenseV2Client, "_request")
def test_authenticate_jwt_success(mock_request, pf_client):
    mock_request.return_value.data = {"token": "fake-jwt-token"}
    token = pf_client.authenticate_jwt()
    assert token == "fake-jwt-token"
    assert pf_client.config.jwt_token == "fake-jwt-token"
    assert pf_client._session.headers["Authorization"] == "Bearer fake-jwt-token"

def test_authenticate_jwt_no_credentials(pf_client):
    pf_client.config.username = None
    pf_client.config.password = None
    with pytest.raises(ValueError) as excinfo:
        pf_client.authenticate_jwt()
    assert "No username/password provided" in str(excinfo.value)

@patch.object(PfSenseV2Client, "_request")
def test_authenticate_jwt_missing_token(mock_request, pf_client):
    mock_request.return_value.data = {}  # No 'token' key
    with pytest.raises(AuthenticationError) as excinfo:
        pf_client.authenticate_jwt()
    assert "No token returned in JWT auth response" in str(excinfo.value)

#
# Tests for firewall alias endpoints
#

@patch.object(PfSenseV2Client, "_request")
def test_get_firewall_aliases(mock_request, pf_client):
    mock_request.return_value.data = [
        {"id": 1, "name": "TestAlias", "type": "host", "descr": "", "address": [], "detail": []}
    ]
    aliases = pf_client.get_firewall_aliases()
    assert len(aliases) == 1
    assert aliases[0].id == 1
    assert aliases[0].name == "TestAlias"

@patch.object(PfSenseV2Client, "_request")
def test_create_firewall_alias(mock_request, pf_client):
    mock_request.return_value.data = {
        "id": 5, "name": "NewAlias", "type": "host", "descr": "", "address": [], "detail": []
    }
    fa_create = FirewallAliasCreate(name="NewAlias", type="host")
    alias = pf_client.create_firewall_alias(fa_create)
    assert alias.id == 5
    assert alias.name == "NewAlias"

@patch.object(PfSenseV2Client, "_request")
def test_update_firewall_alias(mock_request, pf_client):
    mock_request.return_value.data = {
        "id": 5, "name": "UpdatedAlias", "type": "host", "descr": "", "address": [], "detail": []
    }
    fa_update = FirewallAliasUpdate(id=5, name="UpdatedAlias", type="host")
    alias = pf_client.update_firewall_alias(fa_update)
    assert alias.id == 5
    assert alias.name == "UpdatedAlias"

@patch.object(PfSenseV2Client, "_request")
def test_delete_firewall_alias(mock_request, pf_client):
    pf_client.delete_firewall_alias(123)
    mock_request.assert_called_once_with(
        "DELETE",
        "/api/v2/firewall/alias",
        params={"id": 123},
    )

#
# Tests for DHCP Leases
#

@patch.object(PfSenseV2Client, "_request")
def test_get_dhcp_leases(mock_request, pf_client):
    mock_request.return_value.data = [
        {
            "ip": "192.168.1.10",
            "mac": "00:1A:2B:3C:4D:5E",
            "hostname": "Device1",
            "status": "active"
        }
    ]
    leases = pf_client.get_dhcp_leases(limit=10, offset=0)
    assert len(leases) == 1
    assert leases[0].ip == "192.168.1.10"
    assert leases[0].mac == "00:1A:2B:3C:4D:5E"
    assert leases[0].hostname == "Device1"
    assert leases[0].status == "active"

#
# Tests for Apply Endpoints
#

@patch.object(PfSenseV2Client, "_request")
def test_get_firewall_apply_status(mock_request, pf_client):
    mock_request.return_value.data = {"pending_changes": True}
    resp = pf_client.get_firewall_apply_status()
    assert resp.data["pending_changes"] is True

@patch.object(PfSenseV2Client, "_request")
def test_apply_firewall_changes(mock_request, pf_client):
    mock_request.return_value.data = {"applied": True}
    resp = pf_client.apply_firewall_changes()
    assert resp.data["applied"] is True
