import unittest
from pydantic import ValidationError
from pyfsense_client.v1.client import ClientConfig, APIResponse


class TestClientConfig(unittest.TestCase):

    def test_pfsense_config_username_and_pass(self):
        config = ClientConfig(
            username="user",
            password="pass",
            hostname="example.com"
        )
        self.assertEqual(config.username, "user")
        self.assertEqual(config.password, "pass")
        self.assertEqual(config.hostname, "example.com")
        self.assertEqual(config.port, 443)  # Default value

    def test_pfsense_config_token(self):
        config = ClientConfig(
            mode="api_token",
            hostname="example.com",
            client_id="client_id",
            client_token="client_token",
        )
        self.assertIsNone(config.username)
        self.assertIsNone(config.password)
        self.assertEqual(config.hostname, "example.com")
        self.assertEqual(config.port, 443)  # Default value
        self.assertEqual(config.mode, "api_token")
        self.assertEqual(config.client_id, "client_id")
        self.assertEqual(config.client_token, "client_token")

    def test_pfsense_config_invalid(self):
        with self.assertRaises(ValidationError):
            ClientConfig(hostname="example.com")


class TestAPIResponse(unittest.TestCase):

    def test_apiresponse_valid_dict(self):
        response_data = {
            "status": "success",
            "code": 200,
            "return": 0,
            "message": "OK",
            "data": {"key": "value"}
        }
        response = APIResponse(**response_data)
        self.assertEqual(response.data, {"key": "value"})

    def test_apiresponse_valid_list(self):
        response_data = {
            "status": "success",
            "code": 200,
            "return": 0,
            "message": "OK",
            "data": ["item1", "item2"]
        }
        response = APIResponse(**response_data)
        self.assertEqual(response.data, ["item1", "item2"])

    def test_apiresponse_invalid_code(self):
        with self.assertRaises(ValidationError):
            response_data = {
                "status": "error",
                "code": 999,  # Invalid code
                "return": 0,
                "message": "Error",
                "data": {}
            }
            APIResponse(**response_data)

    def test_apiresponse_invalid_data(self):
        with self.assertRaises(ValidationError):
            response_data = {
                "status": "error",
                "code": 200,
                "return": 0,
                "message": "Invalid data",
                "data": "This should be a dict or list"
            }
            APIResponse(**response_data)

    def test_apiresponse_dict(self):
        response_data = {
            "status": "success",
            "code": 200,
            "return": 0,
            "message": "OK",
            "data": {"key": "value"}
        }
        response = APIResponse(**response_data)
        self.assertEqual(response.data, {"key": "value"})

    def test_apiresponse_list(self):
        response_data = {
            "status": "success",
            "code": 200,
            "return": 0,
            "message": "OK",
            "data": ["item1", "item2"]
        }
        response = APIResponse(**response_data)
        self.assertEqual(response.data, ["item1", "item2"])

