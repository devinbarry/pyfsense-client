import pytest
from unittest.mock import patch

from pyfsense_client.v2 import (
    PfSenseV2Client,
    ClientConfig,
    SortOrder,
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
# Tests for DHCP Leases
#


@patch.object(PfSenseV2Client, "_request")
def test_get_dhcp_leases(mock_request, pf_client):
    mock_request.return_value.data = [
        {
            "ip": "192.168.1.10",
            "mac": "00:1A:2B:3C:4D:5E",
            "hostname": "Device1",
            "if": "LAN",
            "start": "2025-01-01T12:00:00Z",
            "end": "2025-01-02T12:00:00Z",
            "active_status": "static",
            "online_status": "'active/online'",
            "descr": "Friendly name for Device1",
        }
    ]
    leases = pf_client.get_dhcp_leases(limit=10, offset=0)
    assert len(leases) == 1
    assert leases[0].ip == "192.168.1.10"
    assert leases[0].mac == "00:1A:2B:3C:4D:5E"
    assert leases[0].hostname == "Device1"
    assert leases[0].status == "active"




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
        {
            "ip": "192.168.1.10",
            "mac": "00:1A:2B:3C:4D:5E",
            "hostname": "Device1",
            "if": "LAN",
            "start": "2025-01-01T12:00:00Z",
            "end": "2025-01-02T12:00:00Z",
            "active_status": "static",
            "online_status": "'active/online'",
            "descr": "Friendly name for Device1",
        }]

    # Test with all optional parameters
    leases = pf_client.get_dhcp_leases(
        limit=10,
        offset=5,
        sort_by=["hostname", "ip"],
        sort_order=SortOrder.DESCENDING,
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


