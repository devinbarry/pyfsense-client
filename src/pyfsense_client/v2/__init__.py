"""
V2 Client Module Initialization
"""

from .client import PfSenseV2Client, ClientConfig, SortOrder
from .exceptions import APIError, AuthenticationError, ValidationError
from .models import (
    APIResponse,
    JWTAuthResponse,
    FirewallAlias,
    FirewallAliasCreate,
    FirewallAliasUpdate,
    DHCPLease,
)

__all__ = [
    "PfSenseV2Client",
    "ClientConfig",
    "SortOrder",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "APIResponse",
    "JWTAuthResponse",
    "FirewallAlias",
    "FirewallAliasCreate",
    "FirewallAliasUpdate",
    "DHCPLease",
]
