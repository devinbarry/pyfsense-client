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
    Simple e2e test to verify authentication and retrieval of firewall aliases.
    """

    # Load config from environment variables
    # Adjust or add more fields if needed for your environment.
    config = ClientConfig(
        host=os.getenv("PFSENSE_HOST"),       # e.g. "https://192.168.1.1"
        verify_ssl=False,                     # for self-signed certs, or True if you have valid SSL
        timeout=30,
        username=os.getenv("PFSENSE_USER"),   # for JWT auth
        password=os.getenv("PFSENSE_PASS"),   # for JWT auth
        api_key=os.getenv("PFSENSE_API_KEY"), # for API key auth
    )

    client = PfSenseClient(config)

    # If we do not already have a JWT token or an API key set, try to auth using username/password.
    # If you want to prefer the API key over username/password, check that below.
    # Or skip if an API key is already configured.
    if not config.api_key and not config.jwt_token:
        # Attempt JWT auth
        try:
            jwt_token = client.authenticate_jwt()
            print(f"Successfully retrieved JWT token: {jwt_token[:10]}...")  # partial print
        except AuthenticationError:
            pytest.fail("JWT authentication failed. Check username/password.")

    # Now attempt to retrieve firewall aliases to confirm we have valid auth
    try:
        aliases = client.get_firewall_aliases()
        print(f"Retrieved {len(aliases)} firewall alias(es).")
        # We won't fail if it's 0, but let's at least ensure it didn't blow up
        assert isinstance(aliases, list)
    except Exception as ex:
        pytest.fail(f"Failed to get firewall aliases: {ex}")
