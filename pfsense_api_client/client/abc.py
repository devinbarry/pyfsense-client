from __future__ import annotations
from typing import Any
from requests import Response, Session
from abc import ABC, abstractmethod


class ClientABC(ABC):
    def __init__(self, requests_session: Session | None = None):
        self.session = requests_session if requests_session is not None else Session()

    @abstractmethod
    def call(self, url: str, method: str = "GET", payload: Any = None, params: Any = None, **kwargs: Any) -> Response:
        pass
