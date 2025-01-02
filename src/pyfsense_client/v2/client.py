from typing import Any
import requests
from dataclasses import dataclass
from .exceptions import APIError, AuthenticationError, ValidationError
from .models import APIResponse


@dataclass
class ClientConfig:
    """Configuration for the pfSense API client"""
    host: str
    verify_ssl: bool = True
    timeout: int = 30
    api_key: str | None = None,
    jwt_token: str | None = None


class PfSenseClient:
    """Client for interacting with the pfSense v2 API"""

    def __init__(
            self,
            config: ClientConfig,

    ):
        """Initialize the pfSense API client

        Args:
            config: Client configuration
            api_key: API key for authentication
            jwt_token: JWT token for authentication
        """
        self.config = config
        self._session = requests.Session()

        # Ensure URL has proper format
        self.base_url = config.host.rstrip('/')
        if not self.base_url.startswith(('http://', 'https://')):
            self.base_url = f'https://{self.base_url}'

        # Configure session
        self._session.verify = config.verify_ssl
        if self.config.api_key:
            self._session.headers.update({'Authorization': f'Bearer {self.config.api_key}'})
        elif self.config.jwt_token:
            self._session.headers.update({'Authorization': f'JWT {self.config.jwt_token}'})

    def _handle_response(self, response: requests.Response) -> APIResponse:
        """Handle API response and convert to proper model

        Args:
            response: Raw requests response

        Returns:
            Parsed API response

        Raises:
            AuthenticationError: When authentication fails
            ValidationError: When request validation fails
            APIError: For other API errors
        """
        try:
            response.raise_for_status()
            return APIResponse.model_validate(response.json())
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed", response)
            elif response.status_code == 400:
                raise ValidationError("Request validation failed", response)
            else:
                raise APIError(f"API request failed: {str(e)}", response)
        except Exception as e:
            raise APIError(f"Failed to parse API response: {str(e)}", response)

    def _request(
            self,
            method: str,
            endpoint: str,
            params: dict[str, Any] | None = None,
            json: dict[str, Any] | None = None,
    ) -> APIResponse:
        """Make a request to the API

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json: JSON body data

        Returns:
            Parsed API response
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

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> APIResponse:
        """Make GET request to API endpoint"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: dict[str, Any] | None = None) -> APIResponse:
        """Make POST request to API endpoint"""
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: dict[str, Any] | None = None) -> APIResponse:
        """Make PUT request to API endpoint"""
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint: str) -> APIResponse:
        """Make DELETE request to API endpoint"""
        return self._request("DELETE", endpoint)

    def authenticate(self, client_id: str, client_secret: str) -> None:
        """Authenticate with the API using client credentials

        Args:
            client_id: API client ID
            client_secret: API client secret

        Raises:
            AuthenticationError: If authentication fails
        """
        # Implementation will depend on the specific authentication endpoint
        # This is a placeholder for the actual authentication logic
        pass