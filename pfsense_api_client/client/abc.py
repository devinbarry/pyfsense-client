from __future__ import annotations
from typing import Any
from requests import Response, Session
from abc import ABC, abstractmethod


class ClientABC(ABC):
    def __init__(self):
        self.session = Session()

    @abstractmethod
    def call(self, url: str, method: str = "GET", payload: Any = None, params: Any = None, **kwargs: Any) -> Response:
        pass
