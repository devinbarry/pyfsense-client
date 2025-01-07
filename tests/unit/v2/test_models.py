from datetime import datetime
from pyfsense_client.v2.models import (
    APIResponse,
    JWTAuthResponse,
    FirewallAlias,
    FirewallAliasCreate,
    FirewallAliasUpdate,
    DHCPLease,
    firewall_alias
)


def test_api_response():
    resp = APIResponse(
        code=200,
        status="success",
        message="All good",
        data={"foo": "bar"}
    )
    assert resp.code == 200
    assert resp.status == "success"
    assert resp.message == "All good"
    assert resp.data == {"foo": "bar"}


def test_jwt_auth_response():
    resp = JWTAuthResponse(
        code=200,
        status="success",
        message="JWT token obtained",
        data={"token": "my-jwt-token"}
    )
    assert resp.code == 200
    assert resp.data["token"] == "my-jwt-token"

def test_firewall_alias():
    alias = FirewallAlias(
        id=1,
        name="TestAlias",
        type=firewall_alias.AliasType.HOST,
        descr="Test Description",
        address=["192.168.1.100"],
        detail=[]
    )
    assert alias.id == 1
    assert alias.name == "TestAlias"
    assert alias.type == "host"
    assert alias.descr == "Test Description"
    assert alias.address == ["192.168.1.100"]


def test_firewall_alias_create():
    fac = FirewallAliasCreate(
        name="CreateAlias",
        type=firewall_alias.AliasType.URL,
        descr="A new alias",
        address=["http://example.com"]
    )
    assert fac.name == "CreateAlias"
    assert fac.type == "url"
    assert fac.descr == "A new alias"
    assert fac.address == ["http://example.com"]


def test_firewall_alias_update():
    fau = FirewallAliasUpdate(
        id=2,
        name="UpdateAlias",
        type=firewall_alias.AliasType.NETWORK,
        descr="Updating alias",
        address=["10.0.0.0/24"],
        detail=["some detail"]
    )
    assert fau.id == 2
    assert fau.name == "UpdateAlias"
    assert fau.type == "network"
    assert fau.address == ["10.0.0.0/24"]


def test_dhcp_lease():
    start_time = datetime(2025, 1, 1, 12, 0, 0)
    end_time = datetime(2025, 1, 2, 12, 0, 0)
    lease = DHCPLease(
        ip="192.168.1.10",
        mac="00:1A:2B:3C:4D:5E",
        hostname="Device1",
        start=start_time,
        end=end_time,
        status="active"
    )
    assert lease.ip == "192.168.1.10"
    assert lease.mac == "00:1A:2B:3C:4D:5E"
    assert lease.hostname == "Device1"
    assert lease.start == start_time
    assert lease.end == end_time
    assert lease.status == "active"
