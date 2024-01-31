from typing import Any, Dict, List
from pydantic import BaseModel, Field, field_validator


class PFSenseConfig(BaseModel):
    """
    This defines the expected config file.

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
