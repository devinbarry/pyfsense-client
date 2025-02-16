[![PythonSupport][1]][1l] [![License: GPL v3][2]][2l]

# Pyfsense Client

Pyfsense Client is a Python API client for interacting with pfSense REST API endpoints provided by the package
at https://github.com/jaredhendrickson13/pfsense-api.

This project now provides **two versions** of the API client:

- **V2 API (Current):** Developed entirely from scratch, this is the actively maintained version. It supports modern authentication methods (API key and JWT-based) and targets the latest pfSense API implementations.
- **V1 API (Legacy Support):** Full support for the original V1 endpoints remains available for backward compatibility, though new development is focused on V2.

The V1 code is currently being tested against pfSense 24.03 and the v1.7.6 API endpoints.
The V2 code is currently being tested against pfSense 24.11 and the v2.3.3 API endpoints.

---

## Table of Contents

- [Installation](#installation)
- [Using the V2 API (Current)](#using-the-v2-api-current)
- [Using the V1 API (Legacy Support)](#using-the-v1-api-legacy-support)
- [Configuring Authentication](#configuring-authentication)
- [Ignoring Certificate Validation](#ignoring-certificate-validation)
- [Development](#development)

---

## Installation

Install via pip:

    pip install pyfsense-client

---

## Using the V2 API (Current)

The V2 API is the recommended and actively maintained version of the Pyfsense Client. It supports both API key and JWT-based authentication.

### Example Usage

    from pyfsense_client.v2 import PfSenseV2Client, ClientConfig

    # Configure your connection
    config_data = {
        "host": "example.com",           # Base URL or IP of your pfSense instance
        "verify_ssl": False,             # Disable SSL verification if needed
        "timeout": 30,                   # Request timeout in seconds
        "username": "your_username",     # For JWT-based auth (optional if using API key)
        "password": "your_password",     # For JWT-based auth (optional if using API key)
        # "api_key": "your_api_key",     # Alternatively, use API key based authentication
    }

    config = ClientConfig(**config_data)
    client = PfSenseV2Client(config=config)

    # For JWT-based authentication, you can call:
    jwt_token = client.authenticate_jwt()
    print("JWT token:", jwt_token)

    # Example: Retrieve all firewall aliases
    aliases = client.get_firewall_aliases()
    for alias in aliases:
        print(alias)

For additional endpoints (such as DHCP leases, applying firewall changes, etc.), refer to the V2 API documentation in the project docs.

---

## Using the V1 API (Legacy Support)

If you need to interact with legacy systems or prefer the older endpoints, the V1 API client is still fully supported.

### Example Usage

    from pyfsense_client.v1 import PfSenseV1Client, ClientConfig

    # Configure your connection for V1
    config_data = {
        "hostname": "example.com",
        "mode": "api_token",             # Options include "local", "jwt", or "api_token"
        "client_id": "your_client_id",     # Required for API token mode
        "client_token": "your_client_token",  # Required for API token mode
        "verify_ssl": False,
    }

    config = ClientConfig(**config_data)
    client = PfSenseV1Client(config=config)

    # Example: Execute a shell command on the firewall
    response = client.execute_shell_command("ls -la")
    print(response)

*Keep in mind that while the V1 API is still available, new features and improvements will be added only to the V2 implementation.*

---

## Configuring Authentication

### V2 API

- **API Key Authentication:** Pass your API key in the configuration via the `api_key` field.
- **JWT-based Authentication:** Provide `username` and `password` (or call `authenticate_jwt()` to obtain a token). The token will be automatically attached to subsequent requests.

### V1 API

The V1 client supports multiple authentication modes:
- **Local:** Requires `username` and `password`.
- **JWT:** Requires a valid `jwt` token.
- **API Token:** Requires both `client_id` and `client_token`.

---

## Ignoring Certificate Validation

If your pfSense instance uses self-signed certificates or you wish to disable SSL certificate validation, set `verify_ssl=False` in your client configuration.

---

## Development

You can build a Docker image for development. This image will install all dependencies and mount the source code for live development.

### Building the Docker Image

    docker compose -f local.yml build

### Running Unit Tests

    docker compose -f local.yml up


## Notes

*The V1 implementation is a heavy rewrite of (https://github.com/yaleman/pfsense-api-client).*

---

[1]: https://img.shields.io/badge/python-3.11+-blue.svg
[1l]: https://github.com/devinbarry/pyfsense-client
[2]: https://img.shields.io/badge/License-GPLv3-blue.svg
[2l]: https://www.gnu.org/licenses/gpl-3.0

---

This README should help you get started with the new V2 API while still providing guidance for legacy V1 usage. Happy coding!
