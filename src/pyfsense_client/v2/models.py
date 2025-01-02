from typing import Any
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Base model for API responses"""
    code: int
    status: str
    response_id: str
    message: str
    data: dict[str, Any] | None = None
    _links: dict[str, Any] | None = None
