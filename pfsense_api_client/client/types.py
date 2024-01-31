from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List
from pydantic import BaseModel, Field, field_validator


class ClientConfig(BaseModel):
    """
    Configuration model for pfSense API client.

    Attributes:
        username (Optional[str]): Username for authentication.
        password (Optional[str]): Password for authentication.
        hostname (str): Hostname or IP address of the server.
        port (int): Port number for the connection. Defaults to 443.
        mode (str): Connection mode. Defaults to 'local'.
        jwt (Optional[str]): JWT token for authentication. Required if mode is 'jwt'.
        client_id (Optional[str]): Client ID for authentication. Required if mode is 'api_token'.
        client_token (Optional[str]): Client token for authentication. Required if mode is 'api_token'.

    Example config file:
    ```json
    {
        "username" : "me",
        "password" : "mysupersecretpassword",
        "hostname" : "example.com",
        "port" : 8443
    }
    ```
    """
    username: str | None
    password: str | None
    hostname: str
    port: int = 443
    mode: str = "local"
    jwt: str | None = None
    client_id: str | None = None
    client_token: str | None = None


def load_client_config(filename: str) -> ClientConfig:
    """
    Loads the client configuration from a JSON file.

    Args:
        filename (str): Path to the configuration file.

    Returns:
        ClientConfig: An instance of ClientConfig with data loaded from the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValidationError: If the data in the file does not conform to the ClientConfig schema.
    """
    config_path = Path(filename).expanduser()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file {config_path.as_posix()} does not exist.")

    with config_path.open(encoding="utf8") as file:
        return ClientConfig(**json.load(file))



class APIResponse(BaseModel):
    """
    Standard JSON API response from the pFsense API.
    """
    status: str
    code: int
    return_code: int = Field(default=..., title="return", alias="return", description="The return field from the API")
    message: str
    data: Any

    @field_validator("code")
    def validate_code(cls, value: int) -> int:
        """
        Validates it's an integer in the expected list.
        """
        valid_codes = {200, 400, 401, 403, 404, 500}
        if value not in valid_codes:
            raise ValueError(f"Got an invalid status code ({value}).")
        return value


class APIResponseDict(APIResponse):
    """
    Dict-style JSON API response from the pFsense API.
    """
    data: Dict[str, Any]


class APIResponseList(APIResponse):
    """
    List-style JSON API response from the pFsense API.
    """
    data: List[Any]
