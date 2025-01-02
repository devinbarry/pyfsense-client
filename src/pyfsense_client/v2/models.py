from typing import Any
from pydantic import BaseModel, Field
from enum import StrEnum


class APIResponse(BaseModel):
    """
    Generic V2 API Response shape. Adjust as needed.

    Example JSON:
    {
      "code": 200,
      "status": "ok",
      "response_id": "some-uuid",
      "message": "Request completed successfully.",
      "data": {},
      "_links": {}
    }
    """
    code: int
    status: str
    response_id: str | None = Field(default=None)
    message: str
    data: dict[str, Any] | None = None
    _links: dict[str, Any] | None = None


class JWTAuthResponse(APIResponse):
    """
    Specialized response for /api/v2/auth/jwt endpoint.
    Expects `data` to contain a `token` field with the JWT.
    """
    pass


#
# Firewall Aliases
#

class FirewallAliasType(StrEnum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"
    # Adjust if there are more types in your pfSense instance.


class FirewallAlias(BaseModel):
    """
    Representation of a firewall alias as returned by GET requests.
    Adjust field names to match your pfSense V2 API.
    """
    name: str
    type: FirewallAliasType
    addresses: list[str] = []  # noqa
    details: list[str] = []  # noqa
    description: str | None = None


class FirewallAliasCreate(BaseModel):
    """
    Model used for creating a firewall alias via POST.
    """
    name: str
    type: FirewallAliasType
    addresses: list[str] = []  # noqa
    details: list[str] = []  # noqa
    description: str | None = None
    apply: bool = True  # If the API supports immediate apply in create


class FirewallAliasUpdate(BaseModel):
    """
    Model used for updating a firewall alias via PATCH or PUT.
    """
    name: str
    type: FirewallAliasType
    addresses: list[str] = []  # noqa
    details: list[str] = []  # noqa
    description: str | None = None
    apply: bool = True  # If the API supports immediate apply in update
