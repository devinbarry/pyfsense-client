from typing import Any
from pydantic import BaseModel, Field
from enum import StrEnum


class APIResponse(BaseModel):
    """
    Generic V2 API response shape. Adjust as needed.
    """
    code: int
    status: str
    response_id: str | None = Field(default=None)
    message: str
    data: dict[str, Any] | list[Any] | None = None
    _links: dict[str, Any] | None = None


class JWTAuthResponse(APIResponse):
    """
    Specialized response for /api/v2/auth/jwt endpoint.
    Expects `data` to contain a `token` field with the JWT.
    """
    pass
