from enum import StrEnum
from pydantic import BaseModel, field_validator


class AliasType(StrEnum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class FirewallAlias(BaseModel):
    name: str
    type: AliasType
    address: str | list[str]
    detail: str | list[str]
    descr: str | None = None

    @field_validator("address")
    @classmethod
    def split_address_str(cls, value: str | list[str]) -> str | list[str]:
        if isinstance(value, list):
            return value
        return value.split(" ") if " " in value else [value]

    @field_validator("detail")
    @classmethod
    def split_detail_str(cls, value: str | list[str]) -> str | list[str]:
        if isinstance(value, list):
            return value
        return value.split("||") if "||" in value else [value]


class FirewallAliasCreate(FirewallAlias):
    apply: bool = True


class FirewallAliasUpdate(FirewallAlias):
    id: str
    apply: bool = True
