from __future__ import annotations
import logging
from typing import Any
from requests import Response, Session

from .abc import ClientABC
from .types import ClientConfig, APIResponse
from ..mixins.firewall import FirewallMixin
from ..mixins.service  import ServiceMixin
from ..mixins.status import StatusMixin
from ..mixins.system import SystemMixin


class ClientBase(ClientABC):
    def __init__(self, config:  ClientConfig):
        self.config = config
        self.session = Session()
        self.logger = logging.getLogger(__name__)

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

        response = self.session.request(url=url, method=method, allow_redirects=False, verify=self.config.verify_ssl,
                                    **kwargs)
        self.logger.debug(f"API response: {response.json()}")
        return response

    def call_api(self, url: str, method: str = "GET", payload: dict[str, Any] | None = None) -> APIResponse:
        response = self.call(url=url, method=method, payload=payload)
        return APIResponse.model_validate(response.json())



class PFSenseAPIClient(ClientBase, FirewallMixin, ServiceMixin, StatusMixin, SystemMixin):
    """pfSense API Client"""

    def request_access_token(self) -> Response:
        """gets a temporary access token
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-request-access-token
        """
        url = "/api/v1/access_token"
        return self.call(url=url, method="POST")

    def execute_shell_command(self, shell_cmd: str) -> Response:
        """execute a shell command on the firewall
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-execute-shell-command
        """
        url = "/api/v1/diagnostics/command_prompt"
        method = "POST"
        return self.call(url=url, method=method, payload={"shell_cmd": shell_cmd})
