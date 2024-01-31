from __future__ import annotations
from typing import Any, Dict
from requests import Response, Session
from abc import ABC, abstractmethod

from .types import ClientConfig, APIResponse


class ClientABC(ABC):
    def __init__(self, requests_session: Session | None = None):
        self.session = requests_session if requests_session is not None else Session()

    @abstractmethod
    def call(self, url: str, method: str = "GET", payload: Any = None, params: Any = None, **kwargs: Any) -> Response:
        pass


class ClientBase(ClientABC):
    def __init__(self, config:  ClientConfig, requests_session: Session | None = None):
        super().__init__(requests_session)
        self.config = config

        if self.config.mode == "local" and not (self.config.username and self.config.password):
            raise ValueError("Authentication Mode is set to local but username or password are missing.")

        if self.config.mode == "local":
            self.session.auth = (self.config.username, self.config.password)

    @property
    def baseurl(self) -> str:
        # Check if the port is set and is not the default HTTPS port (443)
        if self.config.port and self.config.port != 443:
            return f"https://{self.config.hostname}:{self.config.port}"
        else:
            return f"https://{self.config.hostname}"

    def call(self, url: str, method: str = "GET", payload: Any = None, params: Any = None, **kwargs: Any) -> Response:
        url = f"{self.baseurl}{url}" if url.startswith("/") else url
        kwargs.setdefault("params", params)
        kwargs.setdefault("json", payload if method != "GET" else None)
        headers = kwargs.setdefault("headers", {})

        if self.config.mode == "jwt":
            headers["Authorization"] = f"Bearer {self.config.jwt}"
        elif self.config.mode == "api_token":
            headers["Authorization"] = f"{self.config.client_id} {self.config.client_token}"

        return self.session.request(url=url, method=method, allow_redirects=True, **kwargs)

    def call_api(self, url: str, method: str = "GET", payload: Dict[str, Any] | None = None) -> APIResponse:
        response = self.call(url, method, payload)
        return APIResponse.model_validate(response.json())
