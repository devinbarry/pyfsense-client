import requests


class APIError(Exception):
    """Base exception for API errors"""

    def __init__(self, message: str, response: requests.Response | None = None):
        super().__init__(message)
        self.response = response


class AuthenticationError(APIError):
    """Raised when authentication fails"""
    pass


class ValidationError(APIError):
    """Raised when request validation fails"""
    pass