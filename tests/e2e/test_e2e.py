import os
import pytest
from dotenv import load_dotenv

from pyfsense_client.v2 import (
    PfSenseClient,
    ClientConfig,
    AuthenticationError,
)

load_dotenv()


@pytest.mark.skipif(
    condition=not os.getenv("PFSENSE_HOST"),
    reason="Requires a real pfSense server IP/URL in env var PFSENSE_HOST"
)
def test_auth_and_get_aliases():
    """
    Existing example test to verify authentication and retrieval of firewall aliases.
    """
    config = ClientConfig(
        host=os.getenv("PFSENSE_HOST"),
        verify_ssl=False,
        timeout=30,
        username=os.getenv("PFSENSE_USER"),
        password=os.getenv("PFSENSE_PASS"),
        api_key=os.getenv("PFSENSE_API_KEY"),
    )
    client = PfSenseClient(config)

    # Attempt JWT auth if needed
    if not config.api_key and not config.jwt_token:
        try:
            jwt_token = client.authenticate_jwt()
            print(f"Successfully retrieved JWT token: {jwt_token[:10]}...")
        except AuthenticationError:
            pytest.fail("JWT authentication failed. Check username/password.")

    # Get aliases
    try:
        aliases = client.get_firewall_aliases()
        print(f"Retrieved {len(aliases)} firewall alias(es).")
        assert isinstance(aliases, list)
    except Exception as ex:
        pytest.fail(f"Failed to get firewall aliases: {ex}")


@pytest.mark.skipif(
    condition=not os.getenv("PFSENSE_HOST"),
    reason="Requires a real pfSense server IP/URL in env var PFSENSE_HOST"
)
def test_fetch_dhcp_leases():
    """
    New test to fetch DHCP leases from pfSense after successful authentication.
    """
    config = ClientConfig(
        host=os.getenv("PFSENSE_HOST"),
        verify_ssl=False,
        timeout=30,
        username=os.getenv("PFSENSE_USER"),
        password=os.getenv("PFSENSE_PASS"),
        api_key=os.getenv("PFSENSE_API_KEY"),
    )
    client = PfSenseClient(config)

    # Attempt JWT auth if not already set
    if not config.api_key and not config.jwt_token:
        try:
            jwt_token = client.authenticate_jwt()
            print(f"Successfully retrieved JWT token: {jwt_token[:10]}...")
        except AuthenticationError:
            pytest.fail("JWT authentication failed. Check username/password.")

    # Now fetch the DHCP leases
    try:
        leases = client.get_dhcp_leases(limit=10, offset=0)
        print(f"Retrieved {len(leases)} DHCP lease(s).")
        assert isinstance(leases, list)
    except Exception as ex:
        pytest.fail(f"Failed to get DHCP leases: {ex}")
