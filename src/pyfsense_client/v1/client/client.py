from __future__ import annotations
import logging
from json import JSONDecodeError
from requests import Response, Session
from requests.exceptions import HTTPError

from .abc import ClientABC
from .types import ClientConfig, APIResponse
from ..mixins import (
    DNSMixin,
    FirewallMixin,
    FirewallAliasMixin,
    InterfaceMixin,
    RoutingMixin,
    ServiceMixin,
    StatusMixin,
    SystemMixin,
    UserMixin,
)


class CustomHTTPError(HTTPError):
    def __init__(self, *args, **kwargs):
        self.api_code = kwargs.pop("api_code", None)
        self.return_code = kwargs.pop("return_code", None)
        self.api_message = kwargs.pop("api_message", None)
        self.api_data = kwargs.pop("api_data", None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} (API Code: {self.api_code}, Return Code: {self.return_code}, Message: {self.api_message})"


class ClientBase(ClientABC):
    def __init__(self, config: ClientConfig):
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

    def get_url(self, url: str) -> str:
        assert url.startswith("/")
        return f"{self.baseurl}{url}"

    def _request(self, url, method="GET", payload=None, params=None, **kwargs) -> Response:
        url = self.get_url(url)
        kwargs.setdefault("params", params)
        kwargs.setdefault("json", payload if method != "GET" else None)
        headers = kwargs.setdefault("headers", {})
        headers.setdefault("Content-Type", "application/json")

        if self.config.mode == "jwt":
            headers["Authorization"] = f"Bearer {self.config.jwt}"
        elif self.config.mode == "api_token":
            headers["Authorization"] = f"{self.config.client_id} {self.config.client_token}"

        response = self.session.request(
            url=url,
            method=method,
            allow_redirects=False,
            verify=self.config.verify_ssl,
            **kwargs,
        )

        # Attempt to parse the JSON response, regardless of status code
        try:
            response_data = response.json()
            self.logger.debug(f"API response: {response_data}")
        except JSONDecodeError:
            self.logger.debug(f"Non-JSON response: {response.text}")
            if not response.ok:
                # If status code is not 2xx, raise HTTPError
                response.raise_for_status()
            else:
                # If status code is 2xx but response isn't JSON, return the raw response
                return response

        # Check for API-specific error information in the response
        if "code" in response_data and response_data["code"] != 200:
            raise CustomHTTPError(
                response=response,
                api_code=response_data.get("code"),
                return_code=response_data.get("return_code"),
                api_message=response_data.get("message"),
                api_data=response_data.get("data"),
            )

        # If the HTTP status code is not 2xx, raise HTTPError
        if not response.ok:
            response.raise_for_status()

        return response

    def call(self, url, method="GET", payload=None) -> APIResponse:
        response = self._request(url=url, method=method, payload=payload)
        # If the response content is not JSON, return as is
        if not response.headers.get("Content-Type", "").startswith("application/json"):
            return response
        return APIResponse.model_validate(response.json())


class PfSenseV1Client(
    ClientBase,
    DNSMixin,
    FirewallMixin,
    FirewallAliasMixin,
    InterfaceMixin,
    RoutingMixin,
    ServiceMixin,
    StatusMixin,
    SystemMixin,
    UserMixin,
):
    """pfSense API Client"""

    def request_access_token(self) -> APIResponse:
        """gets a temporary access token
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-request-access-token
        """
        url = "/api/v1/access_token"
        return self.call(url=url, method="POST")

    def execute_shell_command(self, shell_cmd: str) -> APIResponse:
        """execute a shell command on the firewall
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-execute-shell-command
        """
        url = "/api/v1/diagnostics/command_prompt"
        method = "POST"
        return self.call(url=url, method=method, payload={"shell_cmd": shell_cmd})
