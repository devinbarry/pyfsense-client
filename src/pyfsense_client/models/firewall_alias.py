from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_serializer


class AliasType(Enum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class FirewallAlias(BaseModel):
    """validating the firewall alias"""
    name: str
    type: AliasType
    address: str | list[str]
    descr: str
    detail: str | list[str]

    @field_serializer('address')
    def split_address_str(address: str | list[str]) -> str | list[str]:
        if isinstance(address, list) or " " not in address:
            return address
        return address.split(' ')

    @field_serializer('detail')
    def split_detail_str(detail: str | list[str]) -> str | list[str]:
        if isinstance(detail, list) or "||" not in detail:
            return detail
        return detail.split('||')


class FirewallAliasUpdate(FirewallAlias):
    """validating the firewall alias update"""
    id: str
    name: str
    type: AliasType
    descr: Optional[str]
    address: str | list[str]
    detail: str | list[str]
    apply: bool


class FirewallAliasCreate(FirewallAlias):
    """validating the firewall alias create"""
    name: str
    type: AliasType
    descr: Optional[str]
    address: str | list[str]
    detail: str | list[str]
    apply: bool
