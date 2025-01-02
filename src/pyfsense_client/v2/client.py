from dataclasses import dataclass
from typing import Any
import requests

from .models import (
    APIResponse,
    JWTAuthResponse,
    FirewallAlias,
    FirewallAliasCreate,
    FirewallAliasUpdate
)
from .exceptions import (
    APIError,
    AuthenticationError,
    ValidationError
)


@dataclass
class ClientConfig:
    """
    Configuration for the pfSense API client.

    host:
        The base URL or IP of the pfSense instance, e.g. 'https://192.168.1.1'
    verify_ssl:
        Whether to verify SSL certificates.
    timeout:
        Request timeout in seconds.
    username/password (optional):
        If your pfSense is configured to accept user credentials for /api/v2/auth/jwt.
        Adjust as needed.
    api_key/jwt_token (optional):
        For direct usage if you already have an API key or a JWT token you want to supply.
    """
    host: str
    verify_ssl: bool = True
    timeout: int = 30
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    jwt_token: str | None = None


class PfSenseClient:
    """
    Client for interacting with the pfSense v2 API.
    Implements:
      - Basic auth flow for JWT tokens
      - Endpoints for firewall aliases
      - A 'request' wrapper that returns pydantic models
    """

    def __init__(self, config: ClientConfig):
        """
        Initialize the pfSense V2 API Client.

        Args:
            config: A ClientConfig dataclass with all config options.
        """
        self.config = config
        self._session = requests.Session()

        # Make sure the base URL does not end with a slash
        self.base_url = self.config.host.rstrip('/')
        if not (self.base_url.startswith('http://') or self.base_url.startswith('https://')):
            self.base_url = f'https://{self.base_url}'

        # Configure request session
        self._session.verify = self.config.verify_ssl
        self._session.timeout = self.config.timeout

        # If user gave us an API key or JWT token up front, set the header
        if self.config.api_key:
            self._session.headers.update({'Authorization': f'Bearer {self.config.api_key}'})
        elif self.config.jwt_token:
            self._session.headers.update({'Authorization': f'Bearer {self.config.jwt_token}'})

    #
    # Internal request logic
    #

    def _handle_response(self, response: requests.Response) -> APIResponse:
        """
        Handle the raw response from requests and convert to an APIResponse or a derived model.

        Raises:
          AuthenticationError: If the response is 401
          ValidationError: If the response is 400
          APIError: For other 4xx/5xx errors or JSON parse issues
        """
        try:
            # Raise for 4xx or 5xx
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed.", response)
            elif response.status_code == 400:
                raise ValidationError("Request validation failed.", response)
            else:
                raise APIError(f"API request failed: {str(exc)}", response)

        # Attempt to parse JSON into the standard APIResponse
        try:
            parsed = response.json()
            return APIResponse.model_validate(parsed)
        except Exception as exc:
            raise APIError(f"Failed to parse API response: {str(exc)}", response)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None
    ) -> APIResponse:
        """
        Core request method that returns an APIResponse (or raises an error).

        Args:
            method: One of GET, POST, PATCH, PUT, DELETE
            endpoint: Path part of the URL, e.g. '/api/v2/firewall/alias'
            params: Optional query params
            json: Optional JSON body

        Returns:
            APIResponse object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=self.config.timeout
        )
        return self._handle_response(response)

    #
    # Authentication
    #

    def authenticate_jwt(self, username: str | None = None, password: str | None = None) -> str:
        """
        Obtain a JWT token from the pfSense v2 API.
        Based on the documented endpoint: POST /api/v2/auth/jwt

        If username/password is not provided as args, uses the ones in config.
        This method updates the session headers to store the token.

        Returns:
            The JWT token as a string, if successful.
        """
        username = username or self.config.username
        password = password or self.config.password
        if not username or not password:
            raise ValueError("No username/password provided for JWT auth.")

        # Make the POST request to /api/v2/auth/jwt with the username/password
        endpoint = "/api/v2/auth/jwt"
        body = {
            "username": username,
            "password": password
        }
        raw_resp = self._request("POST", endpoint, json=body)

        # We expect raw_resp.data to contain something like {"token": "...."}
        # If your pfSense config uses different field naming, adjust below.
        if not raw_resp.data or "token" not in raw_resp.data:
            raise AuthenticationError("No token returned in JWT auth response.", None)

        token = raw_resp.data["token"]
        self._session.headers.update({'Authorization': f'Bearer {token}'})
        return token

    #
    # Firewall Alias Endpoints
    #

    def get_firewall_aliases(self) -> list[FirewallAlias]:
        """
        GET /api/v2/firewall/aliases
        Return the list of all aliases.

        Returns:
            A list of FirewallAlias objects.
        """
        endpoint = "/api/v2/firewall/aliases"
        resp = self._request("GET", endpoint)
        # resp.data might be a list of alias dicts
        if not resp.data:
            return []
        return [FirewallAlias.model_validate(item) for item in resp.data]

    def get_firewall_alias(self, name: str) -> FirewallAlias:
        """
        GET /api/v2/firewall/alias

        Args:
            name: The alias name. (We assume the API accepts it via query param 'name'.)

        Returns:
            FirewallAlias model for the requested alias.
        """
        endpoint = "/api/v2/firewall/alias"
        params = {"name": name}
        resp = self._request("GET", endpoint, params=params)
        return FirewallAlias.model_validate(resp.data)

    def create_firewall_alias(self, alias: FirewallAliasCreate) -> FirewallAlias:
        """
        POST /api/v2/firewall/alias
        Create a new firewall alias.

        Args:
            alias: FirewallAliasCreate object describing the alias.

        Returns:
            The created FirewallAlias object (as returned by the API).
        """
        endpoint = "/api/v2/firewall/alias"
        resp = self._request("POST", endpoint, json=alias.model_dump())
        return FirewallAlias.model_validate(resp.data)

    def update_firewall_alias(self, alias: FirewallAliasUpdate) -> FirewallAlias:
        """
        PATCH /api/v2/firewall/alias
        Update an existing firewall alias.
        (If your API actually uses PUT or requires an 'id' param, adapt accordingly.)

        Args:
            alias: FirewallAliasUpdate object describing the updated info.

        Returns:
            The updated FirewallAlias object.
        """
        endpoint = "/api/v2/firewall/alias"
        resp = self._request("PATCH", endpoint, json=alias.model_dump())
        return FirewallAlias.model_validate(resp.data)

    def delete_firewall_alias(self, name: str) -> None:
        """
        DELETE /api/v2/firewall/alias
        Delete an existing firewall alias.

        Args:
            name: The alias name.
        """
        endpoint = "/api/v2/firewall/alias"
        params = {"name": name}
        self._request("DELETE", endpoint, params=params)

    #
    # Bulk endpoints for aliases (if you need them):
    #

    def bulk_update_firewall_aliases(self, aliases: list[FirewallAliasUpdate]) -> None:
        """
        PUT /api/v2/firewall/aliases
        Possibly used for bulk creation/updates.
        Adjust to match your actual OpenAPI spec.
        """
        endpoint = "/api/v2/firewall/aliases"
        payload = [alias.model_dump() for alias in aliases]
        self._request("PUT", endpoint, json=payload)

    def bulk_delete_firewall_aliases(self, names: list[str]) -> None:
        """
        DELETE /api/v2/firewall/aliases
        Possibly used for bulk deletions.

        Some APIs might expect `DELETE /api/v2/firewall/aliases` with a JSON body or query params.
        Adjust as needed.
        """
        endpoint = "/api/v2/firewall/aliases"
        payload = {"names": names}
        self._request("DELETE", endpoint, json=payload)

    #
    # Apply endpoints
    #

    def get_firewall_apply_status(self) -> APIResponse:
        """
        GET /api/v2/firewall/apply
        Check if there are pending changes or get apply status.
        """
        endpoint = "/api/v2/firewall/apply"
        return self._request("GET", endpoint)

    def apply_firewall_changes(self) -> APIResponse:
        """
        POST /api/v2/firewall/apply
        Apply pending changes.
        """
        endpoint = "/api/v2/firewall/apply"
        return self._request("POST", endpoint)
