from pydantic import BaseModel, Field
from enum import StrEnum


class FirewallAliasType(StrEnum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class FirewallAlias(BaseModel):
    """
    Matches the shape of an alias object returned by read/get operations.
    Example doc fields:
      {
        "id": "1",
        "name": "ExampleAlias",
        "type": "host",
        "descr": "Example alias",
        "enabled": true,
        "content": ["192.168.1.1"]
      }
    We unify "content" -> "address", etc.
    """
    id: int
    name: str
    type: FirewallAliasType
    descr: str
    address: list[str] = Field(default_factory=list)
    detail: list[str] = Field(default_factory=list)


class FirewallAliasCreate(BaseModel):
    """
    Shape for alias creation (POST).
    {
      "name": "string",
      "type": "host",
      "descr": "string",
      "address": ["string"],
      "detail": ["string"]
    }
    """
    name: str
    type: FirewallAliasType
    descr: str | None = None
    address: list[str] = Field(default_factory=list)
    detail: list[str] = Field(default_factory=list)


class FirewallAliasUpdate(BaseModel):
    """
    Shape for alias update (PATCH).
    {
      "id": "string",
      "name": "string",
      "type": "host",
      "descr": "string",
      "address": ["string"],
      "detail": ["string"]
    }
    """
    id: int
    name: str
    type: FirewallAliasType
    descr: str | None = None
    address: list[str] = Field(default_factory=list)
    detail: list[str] = Field(default_factory=list)
