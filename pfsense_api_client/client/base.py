import os
import json
from pathlib import Path

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from requests import Response, Session

from .api_types import PFSenseConfig, APIResponse

class ClientABC(ABC):
    def __init__(self, requests_session: Session):
        self.session = requests_session

    @abstractmethod
    def call(self, url: str, method: str = "GET", payload: Optional[Any] = None, params: Optional[Any] = None,
             **kwargs: Dict[str, Any]) -> Response:
        """Abstract method for making a call to a specified URL. This method must be implemented by subclasses.
        - `url`: The URL to which the call is made.
        - `method`: HTTP method (e.g., 'GET', 'POST').
        - `payload`: The payload of the request.
        - `params`: Additional parameters for the request.
        - `**kwargs`: Additional keyword arguments.
        """
        pass



class ClientBase:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, hostname: Optional[str] = None,
                 port: Optional[int] = None, config_filename: Optional[str] = None, mode: Optional[str] = None,
                 requests_session: Session = Session()):
        self.session = requests_session
        if config_filename:
            self.config = self.load_config(config_filename)
        else:
            config_data: Dict[str, Union[str, int]] = {}
            if username:
                config_data["username"] = username
            if password:
                config_data["password"] = password
            if hostname:
                config_data["hostname"] = hostname
            if port:
                config_data["port"] = port
            if mode:
                config_data["mode"] = mode
            self.config = PFSenseConfig.parse_obj(config_data)

        if self.config.mode == "local" and (self.config.username is not None and self.config.password is not None):
            self.session.auth = (self.config.username, self.config.password)
        elif self.config.mode == "local":
            raise ValueError("Authentication Mode is set to local and username or password are not set!")

    @property
    def baseurl(self) -> str:
        """ returns the base URL of the host """
        retval = f"https://{self.config.hostname}"
        if self.config.port:
            retval += f":{self.config.port}"
        return retval

    def load_config(self, filename: str) -> PFSenseConfig:
        """Loads the config from the specified JSON file (see the `PFSenseConfig` class for what fields are required)"""
        self.config_filename = Path(os.path.expanduser(filename))
        if not self.config_filename.exists():
            error = f"Filename {self.config_filename.as_posix()} does not exist."
            raise FileNotFoundError(error)
        with self.config_filename.open(encoding="utf8") as file_handle:
            pydantic_config = PFSenseConfig(**json.load(file_handle))
        self.config = pydantic_config
        return pydantic_config

    def call(self, url: str, method: str = "GET", payload: Optional[Any] = None, params: Optional[Any] = None,
             **kwargs: Dict[str, Any]) -> Response:
        """mocking type for mypy inheritance"""
        if url.startswith("/"):
            url = f"{self.baseurl}{url}"
        if payload is not None and method == "GET":
            kwargs["params"] = payload
        elif payload is not None:
            kwargs["json"] = payload
        if params is not None:
            kwargs["params"] = params
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if self.config.mode == "jwt":
            kwargs["headers"]["Authorization"] = f"Bearer {self.config.jwt}"
        elif self.config.mode == "api_token":
            kwargs["headers"]["Authorization"] = f"{self.config.client_id} {self.config.client_token}"
        return self.session.request(url=url, method=method, allow_redirects=True, **kwargs)

    def call_api(self, url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> APIResponse:
        """makes a call, returns the JSON blob as a dict"""
        response = self.call(url, method, payload)
        return APIResponse.parse_obj(response.json())

    def call_api_dict(self, url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> APIResponse:
        """makes a call, returns the JSON blob as a dict"""
        response = self.call(url, method, payload)
        print(response.json())
        return APIResponse.parse_obj(response.json())

    def call_json(self, url: str, method: str = "GET", payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """makes a call, returns the JSON blob as a dict"""
        response = self.call(url, method, payload)
        result: Dict[str, Any] = response.json()
        return result
