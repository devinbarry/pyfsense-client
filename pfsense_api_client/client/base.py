from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Dict
from requests import Response, Session
from abc import ABC, abstractmethod

from .api_types import PFSenseConfig, APIResponse


class ClientABC(ABC):
    def __init__(self, requests_session: Session | None = None):
        self.session = requests_session if requests_session is not None else Session()

    @abstractmethod
    def call(self, url: str, method: str = "GET", payload: Any = None, params: Any = None, **kwargs: Any) -> Response:
        pass


class ClientBase(ClientABC):
    def __init__(self, username: str | None = None, password: str | None = None, hostname: str | None = None,
                 port: int | None = None, config_filename: str | None = None, mode: str | None = None,
                 requests_session: Session | None = None):
        super().__init__(requests_session)
        self.config = self.load_config(config_filename) if config_filename else PFSenseConfig.parse_obj({
            "username": username,
            "password": password,
            "hostname": hostname,
            "port": port,
            "mode": mode
        })

        if self.config.mode == "local" and not (self.config.username and self.config.password):
            raise ValueError("Authentication Mode is set to local but username or password are missing.")

        if self.config.mode == "local":
            self.session.auth = (self.config.username, self.config.password)

    @property
    def baseurl(self) -> str:
        return f"https://{self.config.hostname}:{self.config.port}" if self.config.port else f"https://{self.config.hostname}"

    def load_config(self, filename: str) -> PFSenseConfig:
        config_path = Path(os.path.expanduser(filename))
        if not config_path.exists():
            raise FileNotFoundError(f"Config file {config_path.as_posix()} does not exist.")

        with config_path.open(encoding="utf8") as file:
            return PFSenseConfig(**json.load(file))

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
        return APIResponse.parse_obj(response.json())
