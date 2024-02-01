from __future__ import annotations
from requests import Response
from abc import ABC, abstractmethod


class ClientABC(ABC):

    @abstractmethod
    def _call(self, url, method="GET", payload=None, params=None, **kwargs) -> Response:
        pass

    @abstractmethod
    def call(self, url, method="GET", payload=None):
        pass
