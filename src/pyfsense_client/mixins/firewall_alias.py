from typing import Any, Dict
from pydantic import validate_call

from ..client import ClientABC, APIResponse
from ..models import FirewallAliasCreate, FirewallAliasUpdate

class FirewallAliasMixin(ClientABC):

    def get_firewall_alias(self, **kwargs) -> APIResponse:
        """get a list of firewall aliases"""
        url = "/api/v1/firewall/alias"
        return self.call(url=url, method="GET", payload=dict(kwargs))

    @validate_call
    def create_firewall_alias(self, alias: FirewallAliasCreate) -> APIResponse:
        """Add a new host, network or port firewall alias."""
        url = "/api/v1/firewall/alias"
        method = "POST"
        return self.call(url=url, method=method, payload=alias.dict())

    @validate_call
    def delete_firewall_alias(self, name: str, apply: bool = True) -> APIResponse:
        """Delete an existing alias and (optionally) reload filter."""
        url = "/api/v1/firewall/alias"
        method = "DELETE"
        payload = {"id": name, "apply": apply}
        return self.call(url=url, method=method, payload=payload)

    @validate_call
    def update_firewall_alias(self, item: FirewallAliasUpdate) -> APIResponse:
        """Modify an existing firewall alias."""
        method = "PUT"
        url = "/api/v1/firewall/alias"
        return self.call(url=url, method=method, payload=item.dict())

    def get_firewall_alias_advanced(self) -> APIResponse:
        url = "/api/v1/firewall/alias/advanced"
        return self.call(url=url, method="GET")

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