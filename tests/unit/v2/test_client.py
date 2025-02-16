import pytest
import requests
from unittest.mock import patch, MagicMock
from pydantic import ValidationError as PydanticValidationError

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
        jwt_token=None,
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
        "data": {"foo": "bar"},
    }

    result = pf_client._handle_response(mock_response)
    assert result.code == 200
    assert result.status == "success"
    assert result.data == {"foo": "bar"}


def test_handle_response_401(pf_client):
    # Create a mock response whose raise_for_status() immediately throws 401
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "401 Error"
    )

    # We expect the client to raise our custom AuthenticationError
    with pytest.raises(AuthenticationError) as excinfo:
        pf_client._handle_response(mock_response)
    assert "Authentication failed (401)" in str(excinfo.value)


def test_handle_response_400(pf_client):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "400 Error"
    )

    with pytest.raises(ValidationError) as excinfo:
        pf_client._handle_response(mock_response)
    assert "Request validation failed (400)" in str(excinfo.value)


def test_handle_response_500(pf_client):
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Error"
    )

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
        "data": {"foo": "bar"},
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
        timeout=pf_client._default_timeout,
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
        {
            "id": 1,
            "name": "TestAlias",
            "type": "host",
            "descr": "",
            "address": [],
            "detail": [],
        }
    ]
    aliases = pf_client.get_firewall_aliases()
    assert len(aliases) == 1
    assert aliases[0].id == 1
    assert aliases[0].name == "TestAlias"


@patch.object(PfSenseV2Client, "_request")
def test_create_firewall_alias(mock_request, pf_client):
    mock_request.return_value.data = {
        "id": 5,
        "name": "NewAlias",
        "type": "host",
        "descr": "",
        "address": [],
        "detail": [],
    }
    fa_create = FirewallAliasCreate(name="NewAlias", type="host")
    alias = pf_client.create_firewall_alias(fa_create)
    assert alias.id == 5
    assert alias.name == "NewAlias"


@patch.object(PfSenseV2Client, "_request")
def test_update_firewall_alias(mock_request, pf_client):
    mock_request.return_value.data = {
        "id": 5,
        "name": "UpdatedAlias",
        "type": "host",
        "descr": "",
        "address": [],
        "detail": [],
    }
    fa_update = FirewallAliasUpdate(id=5, name="UpdatedAlias", type="host")
    alias = pf_client.update_firewall_alias(fa_update)
    assert alias.id == 5
    assert alias.name == "UpdatedAlias"


@patch.object(PfSenseV2Client, "_request")
def test_delete_firewall_alias(mock_request, pf_client):
    """Test successful and error cases for firewall alias deletion."""
    # Test successful deletion
    mock_request.return_value.data = {"deleted": True}
    mock_request.return_value.code = 200
    mock_request.return_value.message = "Alias deleted successfully"
    mock_request.return_value.status = "success"

    response = pf_client.delete_firewall_alias(123)

    # Verify request
    mock_request.assert_called_once_with(
        "DELETE",
        "/api/v2/firewall/alias",
        params={"id": 123},
    )

    # Verify response
    assert response.code == 200
    assert response.status == "success"
    assert response.message == "Alias deleted successfully"
    assert response.data == {"deleted": True}

    # Reset mock for next test
    mock_request.reset_mock()

    # Test deleting non-existent alias
    mock_request.return_value.data = {"error": "Alias not found"}
    mock_request.return_value.code = 404
    mock_request.return_value.message = "Alias with ID 999 not found"
    mock_request.return_value.status = "error"

    response = pf_client.delete_firewall_alias(999)

    mock_request.assert_called_once_with(
        "DELETE",
        "/api/v2/firewall/alias",
        params={"id": 999},
    )

    assert response.code == 404
    assert response.status == "error"
    assert response.message == "Alias with ID 999 not found"
    assert response.data == {"error": "Alias not found"}


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
            "status": "active",
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


# Additional tests after the code review


def test_pf_client_url_normalization(client_config):
    """Test different URL formats are normalized correctly."""
    # Test without protocol
    client_config.host = "pfsense.local"
    client = PfSenseV2Client(client_config)
    assert client.base_url == "https://pfsense.local"

    # Test with trailing slash
    client_config.host = "https://pfsense.local/"
    client = PfSenseV2Client(client_config)
    assert client.base_url == "https://pfsense.local"

    # Test with http protocol
    client_config.host = "http://pfsense.local"
    client = PfSenseV2Client(client_config)
    assert client.base_url == "http://pfsense.local"


@patch.object(PfSenseV2Client, "_request")
def test_get_dhcp_leases_empty_response(mock_request, pf_client):
    """Test DHCP lease retrieval with empty response."""
    mock_request.return_value.data = None
    leases = pf_client.get_dhcp_leases()
    assert len(leases) == 0

    mock_request.return_value.data = []
    leases = pf_client.get_dhcp_leases()
    assert len(leases) == 0


@patch.object(PfSenseV2Client, "_request")
def test_get_dhcp_leases_with_params(mock_request, pf_client):
    """Test DHCP lease retrieval with all possible parameters."""
    mock_request.return_value.data = [
        {"ip": "192.168.1.10", "mac": "00:1A:2B:3C:4D:5E", "hostname": "Device1"}
    ]

    # Test with all optional parameters
    leases = pf_client.get_dhcp_leases(
        limit=10,
        offset=5,
        sort_by=["hostname", "ip"],
        sort_order="SORT_DESC",
        query={"status": "active"},
    )

    mock_request.assert_called_once_with(
        "GET",
        "/api/v2/status/dhcp_server/leases",
        params={
            "limit": 10,
            "offset": 5,
            "sort_by": ["hostname", "ip"],
            "sort_order": "SORT_DESC",
            "query": {"status": "active"},
        },
    )
    assert len(leases) == 1
    assert leases[0].ip == "192.168.1.10"


@patch.object(PfSenseV2Client, "_request")
def test_replace_all_firewall_aliases(mock_request, pf_client):
    """Test replacing all firewall aliases."""
    mock_request.return_value.data = [
        {
            "id": 1,
            "name": "NewAlias1",
            "type": "host",
            "descr": "",
            "address": ["192.168.1.1"],
            "detail": [],
        },
        {
            "id": 2,
            "name": "NewAlias2",
            "type": "network",
            "descr": "",
            "address": ["10.0.0.0/24"],
            "detail": [],
        },
    ]

    aliases_to_create = [
        FirewallAliasCreate(name="NewAlias1", type="host", address=["192.168.1.1"]),
        FirewallAliasCreate(name="NewAlias2", type="network", address=["10.0.0.0/24"]),
    ]

    result = pf_client.replace_all_firewall_aliases(aliases_to_create)

    mock_request.assert_called_once_with(
        "PUT",
        "/api/v2/firewall/aliases",
        json=[alias.model_dump() for alias in aliases_to_create],
    )

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "NewAlias1"
    assert result[1].id == 2
    assert result[1].name == "NewAlias2"


@patch.object(PfSenseV2Client, "_request")
def test_delete_all_firewall_aliases(mock_request, pf_client):
    """Test bulk deletion of firewall aliases."""
    mock_request.return_value.data = {"deleted": 2}

    # Test with all parameters
    result = pf_client.delete_all_firewall_alias(
        limit=10, offset=5, query={"type": "host"}
    )
    mock_request.assert_called_once_with(
        "DELETE",
        "/api/v2/firewall/aliases",
        params={"limit": 10, "offset": 5, "type": "host"},
    )
    assert result.data == {"deleted": 2}


@patch.object(PfSenseV2Client, "_request")
def test_replace_all_firewall_aliases_empty_response(mock_request, pf_client):
    """Test replacing all firewall aliases with empty response."""
    mock_request.return_value.data = None
    result = pf_client.replace_all_firewall_aliases([])
    assert len(result) == 0

    mock_request.return_value.data = []
    result = pf_client.replace_all_firewall_aliases([])
    assert len(result) == 0


@patch.object(PfSenseV2Client, "_request")
def test_get_firewall_alias_validation(mock_request, pf_client):
    """Test get_firewall_alias with invalid response data."""
    # Test with missing required fields
    mock_request.return_value.data = {"id": 1}  # Missing other required fields

    with pytest.raises(PydanticValidationError) as exc_info:
        pf_client.get_firewall_alias(1)
    errors = exc_info.value.errors()
    assert any(err["type"] == "missing" and err["loc"] == ("name",) for err in errors)
    assert any(err["type"] == "missing" and err["loc"] == ("type",) for err in errors)
    assert any(err["type"] == "missing" and err["loc"] == ("descr",) for err in errors)

    # Test with invalid enum value
    mock_request.return_value.data = {
        "id": 1,
        "name": "TestAlias",
        "type": "invalid_type",  # Invalid enum value
        "descr": "test",
        "address": [],
        "detail": [],
    }

    with pytest.raises(PydanticValidationError) as exc_info:
        pf_client.get_firewall_alias(1)
    errors = exc_info.value.errors()
    assert any(err["type"] == "enum" and err["loc"] == ("type",) for err in errors)

    # Test with wrong data types
    mock_request.return_value.data = {
        "id": "not_an_integer",  # Should be int
        "name": "TestAlias",
        "type": "host",
        "descr": "test",
        "address": "not_a_list",  # Should be list
        "detail": [],
    }

    with pytest.raises(PydanticValidationError) as exc_info:
        pf_client.get_firewall_alias(1)
    errors = exc_info.value.errors()
    assert any(err["type"] == "int_parsing" and err["loc"] == ("id",) for err in errors)
    assert any(
        err["type"] == "list_type" and err["loc"] == ("address",) for err in errors
    )
