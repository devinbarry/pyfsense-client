from __future__ import annotations
from requests import Response
from abc import ABC, abstractmethod
from .types import APIResponse


class ClientABC(ABC):
    @abstractmethod
    def _request(self, url, method="GET", payload=None, params=None, **kwargs) -> Response:
        pass

    @abstractmethod
    def call(self, url, method="GET", payload=None) -> APIResponse:
        pass
