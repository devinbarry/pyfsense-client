import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator
from requests import Response, Session


class PFSenseConfig(BaseModel):
    """This defines the expected config file

        Example config file:
    ```json
    {
            "username" : "me",
            "password" : "mysupersecretpassword",
            "hostname" : "example.com",
            "port" : 8443,
    }
    ```
    """

    username: Optional[str]
    password: Optional[str]
    port: int = 443
    hostname: str
    mode: str = "local"
    jwt: Optional[str]
    client_id: Optional[str]
    client_token: Optional[str]



class APIResponse(BaseModel):
    """standard JSON API response from the pFsense API"""

    status: str
    code: int
    return_code: int = Field(
        ..., title="return", alias="return", description="The return field from the API"
    )
    message: str
    data: Any

    @validator("code")
    def validate_code(cls, value: int) -> int:
        """validates it's an integer in the expected list"""
        if value not in [200, 400, 401, 403, 404, 500]:
            raise ValueError(f"Got an invalid status code ({value}).")
        return value


class APIResponseDict(APIResponse):
    """Dict-style JSON API response from the pFsense API"""

    data: Dict[str, Any]


class APIResponseList(APIResponse):
    """List-style JSON API response from the pFsense API"""

    data: List[Any]
