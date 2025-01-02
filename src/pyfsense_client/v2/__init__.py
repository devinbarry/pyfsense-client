"""
V2 Client Module Initialization
"""

from .client import PfSenseClient, ClientConfig
from .exceptions import (
    APIError,
    AuthenticationError,
    ValidationError
)
from .models import (
    APIResponse,
    JWTAuthResponse,
    FirewallAliasCreate,
    FirewallAliasUpdate,
    FirewallAlias
)

__all__ = [
    "PfSenseClient",
    "ClientConfig",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "APIResponse",
    "JWTAuthResponse",
    "FirewallAliasCreate",
    "FirewallAliasUpdate",
    "FirewallAlias"
]
