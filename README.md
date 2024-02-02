# pfSense API Client

pfSense API client is a Python client for pfsense API endpoints provided by the package at https://github.com/jaredhendrickson13/pfsense-api.

This repository is a rewrite of the code at https://github.com/yaleman/pfsense-api-client.

This code is currently being tested against pfSense 23.09 and the V1 API endpoints (also version 23.09).

### ⚠️ WARNING ⚠️
This is code is experimental and might not be suitable for production use for all methods.

## Configuring authentication

Technically this library supports all authentication methods but we are only testing with API token.

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
