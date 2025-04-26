from enum import StrEnum
from dataclasses import dataclass
from typing import Any

import requests

from .exceptions import APIError, AuthenticationError, ValidationError
from .models import (
    APIResponse,
    FirewallAlias,
    FirewallAliasCreate,
    FirewallAliasUpdate,
    DHCPLease,
)


class SortOrder(StrEnum):
    ASCENDING = "SORT_ASC"
    DESCENDING = "SORT_DESC"


class SortFlags(StrEnum):
    SORT_REGULAR = "SORT_REGULAR"
    SORT_NUMERIC = "SORT_NUMERIC"
    SORT_STRING = "SORT_STRING"
    SORT_LOCALE_STRING = "SORT_LOCALE_STRING"
    SORT_NATURAL = "SORT_NATURAL"
    SORT_FLAG_CASE = "SORT_FLAG_CASE"


@dataclass
class ClientConfig:
    """
    Configuration for the pfSense API client.

    Attributes:
        host (str): The base URL or IP of the pfSense instance, e.g. "https://192.168.1.1"
        verify_ssl (bool): Whether to verify SSL certificates.
        timeout (int): Request timeout in seconds.
        username (str | None): For JWT-based auth calls.
        password (str | None): For JWT-based auth calls.
        api_key (str | None): If using API key-based authentication (the server expects "X-API-Key: <api_key>").
        jwt_token (str | None): If you already have a JWT token or want to store it after calling `authenticate_jwt()`.
    """

    host: str
    verify_ssl: bool = True
    timeout: int = 30
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    jwt_token: str | None = None


class PfSenseV2Client:
    """
    Client for interacting with pfSense V2 REST API.

    Features:
      - API Key or JWT-based auth
      - Endpoints for firewall aliases
      - Endpoints for DHCP leases
      - Apply/pending changes endpoints
    """

    def __init__(self, config: ClientConfig):
        """
        Initialize the pfSense V2 API Client.

        Args:
            config (ClientConfig): The configuration object with host, credentials, etc.
        """
        self.config = config
        self._session = requests.Session()

        # Normalize base URL
        self.base_url = self.config.host.rstrip("/")
        if not (self.base_url.startswith("http://") or self.base_url.startswith("https://")):
            self.base_url = f"https://{self.base_url}"

        # Configure request session
        self._session.verify = self.config.verify_ssl
        self._default_timeout = self.config.timeout

        # If we already have an API key or JWT token, attach it to the session headers
        if self.config.api_key:
            self._session.headers.update({"X-API-Key": f"{self.config.api_key}"})
        elif self.config.jwt_token:
            self._session.headers.update({"Authorization": f"Bearer {self.config.jwt_token}"})

    #
    # Internal request methods
    #

    def _handle_response(self, response: requests.Response) -> APIResponse:
        """
        Handle the raw response from requests and convert to an APIResponse or raise an error.

        Raises:
            AuthenticationError: If the response is 401
            ValidationError: If the response is 400
            APIError: For other 4xx/5xx errors or JSON parse issues
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed (401).", response)
            elif response.status_code == 400:
                raise ValidationError("Request validation failed (400).", response)
            else:
                raise APIError(f"API request failed: {str(exc)}", response)

        # Attempt to parse JSON into the standard APIResponse
        try:
            parsed = response.json()
            return APIResponse.model_validate(parsed)
        except Exception as exc:
            raise APIError(f"Failed to parse JSON response: {str(exc)}", response)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | list[dict] | None = None,
    ) -> APIResponse:
        """
        Core request method that returns an APIResponse (or raises an error).

        Args:
            method (str): One of GET, POST, PATCH, DELETE
            endpoint (str): Path part of the URL, e.g. '/api/v2/firewall/alias'
            params (Optional[dict[str, Any]]): Optional query params
            json (list[dict] or dict): Optional JSON body

        Returns:
            APIResponse: The parsed API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=self._default_timeout,
        )
        return self._handle_response(response)

    #
    # Auth
    #

    def authenticate_jwt(self, username: str | None = None, password: str | None = None) -> str:
        """
        Obtain a JWT token from the pfSense V2 API by calling POST /api/v2/auth/jwt.

        Args:
            username (str | None): If not provided, uses config.username
            password (str | None): If not provided, uses config.password

        Returns:
            str: The JWT token
        """
        username = username or self.config.username
        password = password or self.config.password
        if not username or not password:
            raise ValueError("No username/password provided for JWT auth.")

        endpoint = "/api/v2/auth/jwt"
        body = {"username": username, "password": password}
        raw_resp = self._request("POST", endpoint, json=body)

        if not raw_resp.data or "token" not in raw_resp.data:
            raise AuthenticationError("No token returned in JWT auth response.", None)

        token = raw_resp.data["token"]
        self._session.headers.update({"Authorization": f"Bearer {token}"})
        self.config.jwt_token = token
        return token

    #
    # Firewall Aliases (plural)
    #

    def get_firewall_aliases(self) -> list[FirewallAlias]:
        """
        GET /api/v2/firewall/aliases
        Returns a list of all firewall aliases.
        """
        endpoint = "/api/v2/firewall/aliases"
        resp = self._request("GET", endpoint)
        if not resp.data or not isinstance(resp.data, list):
            return []
        return [FirewallAlias.model_validate(item) for item in resp.data]

    def replace_all_firewall_aliases(self, aliases: list[FirewallAliasCreate]) -> list[FirewallAlias]:
        """
        PUT /api/v2/firewall/aliases
        Returns a list of all firewall aliases.
        """
        endpoint = "/api/v2/firewall/aliases"
        resp = self._request("PUT", endpoint, json=[alias.model_dump() for alias in aliases])
        if not resp.data or not isinstance(resp.data, list):
            return []
        return [FirewallAlias.model_validate(item) for item in resp.data]

    def delete_all_firewall_alias(
        self,
        limit: int = 0,
        offset: int = 0,
        query: dict[str, str | int | bool] | None = None,
    ) -> APIResponse:
        """
        DELETE /api/v2/firewall/aliases
        Deletes multiple existing Firewall Aliases using a query.

        WARNING: This will delete all objects that match the query, use with caution.

        Args:
            limit (int): The maximum number of objects to delete at once. Set to 0 for no limit. Default is 0.
            offset (int): The starting point in the dataset to begin fetching objects. Default is 0.
            query (dict[str, Any] | None): The arbitrary query parameters to include in the request. Default is None.
        """
        endpoint = "/api/v2/firewall/aliases"
        params = {"limit": limit, "offset": offset}
        if query:
            params.update(query)
        return self._request("DELETE", endpoint, params=params)

    #
    # Firewall Alias (singular)
    #

    def get_firewall_alias(self, alias_id: int) -> FirewallAlias:
        """
        GET /api/v2/firewall/alias?id=<alias_id>
        Retrieve a single firewall alias by its integer ID.
        """
        endpoint = "/api/v2/firewall/alias"
        params = {"id": alias_id}
        resp = self._request("GET", endpoint, params=params)
        return FirewallAlias.model_validate(resp.data)

    def create_firewall_alias(self, alias: FirewallAliasCreate) -> FirewallAlias:
        """
        POST /api/v2/firewall/alias
        Create a new firewall alias.

        Args:
            alias (FirewallAliasCreate): The alias creation model.

        Returns:
            FirewallAlias: The created alias as returned by the API.
        """
        endpoint = "/api/v2/firewall/alias"
        resp = self._request("POST", endpoint, json=alias.model_dump())
        return FirewallAlias.model_validate(resp.data)

    def update_firewall_alias(self, alias: FirewallAliasUpdate) -> FirewallAlias:
        """
        PATCH /api/v2/firewall/alias
        Update an existing firewall alias.

        Args:
            alias (FirewallAliasUpdate): The alias update model (must include id).

        Returns:
            FirewallAlias: The updated firewall alias.
        """
        endpoint = "/api/v2/firewall/alias"
        resp = self._request("PATCH", endpoint, json=alias.model_dump())
        return FirewallAlias.model_validate(resp.data)

    def delete_firewall_alias(self, alias_id: int) -> APIResponse:
        """
        DELETE /api/v2/firewall/alias?id=<alias_id>
        Delete an existing firewall alias by ID.
        """
        endpoint = "/api/v2/firewall/alias"
        params = {"id": alias_id}
        return self._request("DELETE", endpoint, params=params)

    #
    # Apply endpoints (pending changes)
    #

    def get_firewall_apply_status(self) -> APIResponse:
        """
        GET /api/v2/firewall/apply
        Check if there are pending changes to apply.
        """
        endpoint = "/api/v2/firewall/apply"
        return self._request("GET", endpoint)

    def apply_firewall_changes(self) -> APIResponse:
        """
        POST /api/v2/firewall/apply
        Apply pending changes immediately.
        """
        endpoint = "/api/v2/firewall/apply"
        return self._request("POST", endpoint)

    #
    # DHCP Leases
    #

    def get_dhcp_leases(
        self,
        limit: int = 0,
        offset: int = 0,
        sort_by: list[str] | None = None,
        sort_order: SortOrder = SortOrder.ASCENDING,
        sort_flags: SortFlags = SortFlags.SORT_REGULAR,
    ) -> list[DHCPLease]:
        """
        GET /api/v2/status/dhcp_server/leases
        Fetches active and static DHCP leases from the system.

        Arguments:
            limit (int): The maximum number of lease records to return. (0 = no limit).
            offset (int): The starting point for the records to return in a paginated response.
            sort_by (list[str]): Optional. A list of fields by which the results should be sorted.
            sort_order (SortOrder): The direction of sorting, ascending or descending.
            sort_flags (SortFlags): The manner in which sorting is applied.

        Returns:
            list[DHCPLease]: A list of parsed DHCP lease objects.
        """
        endpoint = "/api/v2/status/dhcp_server/leases"
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
            "sort_order": sort_order,
        }
        if sort_by:
            params["sort_by"] = sort_by
        if sort_flags:
            params["sort_flags"] = sort_flags

        resp = self._request("GET", endpoint, params=params)
        if not resp.data or not isinstance(resp.data, list):
            return []
        return [DHCPLease.model_validate(item) for item in resp.data]
