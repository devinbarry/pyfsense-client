[![PythonSupport][1]][1l] [![License: GPL v3][2]][2l]

# Pyfsense Client

Pyfsense Client is a Python API client for pfSense API endpoints provided by the package at https://github.com/jaredhendrickson13/pfsense-api.

This repository is a rewrite of the code at https://github.com/yaleman/pfsense-api-client.

This code is currently being tested against pfSense 24.03 and the v1.7.6 API endpoints.

## Project Status

Project is under development and likely will not have working methods for all endpoints.


This project has not been tested against all endpoints. Integration tests from the original repo have been converted
to unit test stubs but hae not all been written. Writing mocked tests for all the endpoints is a large task and is unlikely to
be finished considering the API has been recently upgraded to version 2. It makes more sense to transition this project to using
version 2 endpoints and write tests for those instead.


## Configuring authentication

Technically this library supports all authentication methods, but we are only testing with API token.

```python
config_data = {
    "hostname": "example.com",
    "mode": "api_token",
    "client_id": "3490580384",
    "client_token": "3495739084",
    "verify_ssl": False,
}

config = ClientConfig(**config_data)
client = PFSenseAPIClient(config=config)
```

Support exists for passing credentials as a JSON file.

```json
{
    "username" : "me",
    "password" : "mysupersecretpassword",
    "hostname" : "example.com",
    "port" : 8443
}
```

## Ignoring Certificate validation

Pass `verify_ssl=False` into the config to disable SSL checking.


## Development

You can build a docker image of the source code using docker compose. This will install all the dependencies from the requirements file and volume mount the code for development.
```bash
docker compose -f local.yml build
```

You can run the unit tests with:
```bash
docker compose -f local.yml up
```

[1]: https://img.shields.io/badge/python-3.10+-blue.svg
[1l]: https://github.com/devinbarry/pyfsense-client
[2]: https://img.shields.io/badge/License-GPLv3-blue.svg
[2l]: https://www.gnu.org/licenses/gpl-3.0
