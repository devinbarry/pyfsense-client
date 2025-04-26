from pydantic import BaseModel, Field
from datetime import datetime


class DHCPLease(BaseModel):
    """
    Matches the DHCP lease object per the doc:
    {
      "ip": "192.168.1.10",
      "mac": "00:1A:2B:3C:4D:5E",
      "hostname": "Device1",
      "if": "LAN",
      "start": "2025-01-01T12:00:00Z",
      "end": "2025-01-02T12:00:00Z",
      "active_status": "active",
      "online_status": "string",
      "descr": "string"
    }
    """

    ip: str
    mac: str
    hostname: str | None
    interface: str | None = Field(alias="if")  # Use 'interface' in Python, but 'if' in JSON
    start: datetime | None = None
    end: datetime | None = None
    active_status: str
    online_status: str
    descr: str | None = None
