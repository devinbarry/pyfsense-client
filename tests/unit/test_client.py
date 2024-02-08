import unittest
from tempfile import NamedTemporaryFile

import requests_mock
import json
from requests.exceptions import HTTPError
from pyfsense_client.client import ClientConfig, ClientBase, APIResponse, load_client_config

class TestPfsenseApiClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up test configuration for all tests
        cls.test_config = {
            "username": "test_user",
            "password": "test_pass",
            "hostname": "test.example.com",
            "mode": "jwt",
            "jwt": "test_jwt_token"
        }

    def test_client_base_initialization(self):
        config = ClientConfig(**self.test_config)
        client = ClientBase(config=config)
        self.assertEqual(client.config.username, "test_user")
        self.assertEqual(client.config.password, "test_pass")
        self.assertEqual(client.config.hostname, "test.example.com")

    def test_client_base_request(self):
        with requests_mock.Mocker() as m:
            test_url = "https://test.example.com/test"
            m.get(test_url, json={"status": "success", "data": "test_data"})

            config = ClientConfig(**self.test_config)
            client = ClientBase(config=config)
            response = client._request("/test")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["status"], "success")
            self.assertEqual(response.json()["data"], "test_data")

    def test_client_base_config_loading(self):
        tmp_path = self.create_temporary_file(self.test_config)
        config = load_client_config(tmp_path)
        client = ClientBase(config=config)
        self.assertEqual(client.config.username, "test_user")
        self.assertEqual(client.config.hostname, "test.example.com")

    def create_temporary_file(self, content):
        # Helper method to create a temporary file
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(json.dumps(content).encode())
            return tmp_file.name

    def test_client_base_http_methods(self):
        for method, mock_method in [("GET", "get"), ("POST", "post"), ("PUT", "put"), ("DELETE", "delete")]:
            with requests_mock.Mocker() as m:
                test_url = f"https://test.example.com/test_{method.lower()}"
                getattr(m, mock_method)(test_url, json={"method": method})

                config = ClientConfig(**self.test_config)
                client = ClientBase(config=config)
                response = client._request(f"/test_{method.lower()}", method=method)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["method"], method)

    def test_client_base_error_handling(self):
        with requests_mock.Mocker() as m:
            test_url = "https://test.example.com/error"
            m.get(test_url, status_code=400, json={"error": "Bad Request"})

            config = ClientConfig(**self.test_config)
            client = ClientBase(config=config)
            with self.assertRaises(HTTPError):
                response = client._request("/error")
                response.raise_for_status()

    def test_client_base_call_method(self):
        with requests_mock.Mocker() as m:
            test_url = "https://test.example.com/api"
            mock_response = {
                "code": 200,
                "return": 0,
                "message": "Success",
                "status": "success",
                "data": {"key": "value"}
            }
            m.get(test_url, json=mock_response)

            config = ClientConfig(**self.test_config)
            client = ClientBase(config=config)
            api_response = client.call("/api")

            self.assertIsInstance(api_response, APIResponse)
            self.assertEqual(api_response.status, "success")
            self.assertEqual(api_response.data, {"key": "value"})
            self.assertEqual(api_response.code, 200)
