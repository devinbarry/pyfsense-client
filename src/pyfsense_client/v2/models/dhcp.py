from pydantic import BaseModel
from datetime import datetime


class DHCPLease(BaseModel):
    """
    Matches the DHCP lease object per the doc:
    {
      "ip": "192.168.1.10",
      "mac": "00:1A:2B:3C:4D:5E",
      "hostname": "Device1",
      "start": "2025-01-01T12:00:00Z",
      "end": "2025-01-02T12:00:00Z",
      "status": "active",
      "online_status": "string",
      "descr": "string"
    }
    """
    ip: str
    mac: str
    hostname: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    status: str | None = None
    online_status: str | None = None
    descr: str | None = None
