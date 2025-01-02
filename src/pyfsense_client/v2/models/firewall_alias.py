from typing import Any
from pydantic import BaseModel, Field
from enum import StrEnum


class FirewallAliasType(StrEnum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class FirewallAlias(BaseModel):
    """
    Represents a firewall alias object as returned by GET endpoints.
    Adjust fields to match your pfSense V2 API (names, etc.).
    """
    name: str
    type: FirewallAliasType
    addresses: list[str] = Field(default_factory=list)
    details: list[str] = Field(default_factory=list)
    description: str | None = None


class FirewallAliasCreate(BaseModel):
    """
    Model for creating firewall aliases (POST).
    """
    name: str
    type: FirewallAliasType
    addresses: list[str] = Field(default_factory=list)
    details: list[str] = Field(default_factory=list)
    description: str | None = None
    apply: bool = True


class FirewallAliasUpdate(BaseModel):
    """
    Model for updating firewall aliases (PATCH or PUT).
    """
    name: str
    type: FirewallAliasType
    addresses: list[str] = Field(default_factory=list)
    details: list[str] = Field(default_factory=list)
    description: str | None = None
    apply: bool = True
