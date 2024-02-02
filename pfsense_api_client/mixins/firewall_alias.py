from enum import Enum
from typing import Any, Dict, List, Union, Optional
from pydantic import BaseModel, validate_call

from ..client import ClientABC, APIResponse

class AliasTypes(str, Enum):
    """types for firewall aliases"""
    host = "host"
    network = "network"
    port = "port"

class FirewallAliasUpdate(BaseModel):
    """validating the firewall alias update"""
    name: str
    type: AliasTypes
    descr: Optional[str]
    address: Union[str, List[str]]
    detail: Union[str, List[str]]
    apply: bool


class FirewallAlias(BaseModel):
    """validating the firewall alias"""
    name: str
    type: AliasTypes
    descr: str
    address: Union[str, List[str]]
    detail: Union[str, List[str]]
    apply: bool


class FirewallAliasMixin(ClientABC):

    def get_firewall_alias(self, **kwargs) -> APIResponse:
        """get a list of firewall aliases"""
        url = "/api/v1/firewall/alias"
        return self.call(url=url, method="GET", payload=dict(kwargs))

    @validate_call
    def create_firewall_alias(self, name: str, alias_type: str, descr: str, address: Union[str, List[str]],
                              detail: Union[str, List[str]], apply: bool = True) -> APIResponse:
        """Add a new host, network or port firewall alias."""
        url = "/api/v1/firewall/alias"
        method = "POST"
        payload = FirewallAlias(name=name, type=alias_type, descr=descr, address=address, detail=detail,
                                apply=apply).dict()
        return self.call(url=url, method=method, payload=payload)

    @validate_call
    def delete_firewall_alias(self, name: str, apply: bool = True) -> APIResponse:
        """Delete an existing alias and (optionally) reload filter."""
        url = "/api/v1/firewall/alias"
        method = "DELETE"
        payload = {"id": name, "apply": apply}
        return self.call(url=url, method=method, payload=payload)

    @validate_call
    def update_firewall_alias(self, *args: FirewallAliasUpdate) -> APIResponse:
        """Modify an existing firewall alias."""
        method = "PUT"
        url = "/api/v1/firewall/alias"
        payload = FirewallAliasUpdate(*args).dict()
        return self.call(url=url, method=method, payload=payload)

    def get_firewall_alias_advanced(self, **kwargs) -> APIResponse:
        url = "/api/v1/firewall/alias/advanced"
        return self.call(url=url, method="GET", payload=dict(kwargs))

    @validate_call
    def delete_firewall_alias_advanced(self, name: str, apply: bool = True) -> APIResponse:
        url = "/api/v1/firewall/alias/advanced"
        method = "DELETE"
        payload = {"id": name, "apply": apply}
        return self.call(url=url, method=method, payload=payload)

    def create_firewall_alias_entry(self, **args: Dict[str, Any]) -> APIResponse:
        """Add new entries to an existing firewall alias."""
        method = "POST"
        url = "/api/v1/firewall/alias/entry"
        return self.call(url=url, method=method, payload=args)

    def delete_firewall_alias_entry(self, **args: Dict[str, Any]) -> APIResponse:
        """Delete existing entries from an existing firewall alias."""
        method = "DELETE"
        url = "/api/v1/firewall/alias/entry"
        return self.call(url=url, method=method, payload=args)
