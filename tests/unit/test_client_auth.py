import unittest
from unittest.mock import patch, MagicMock
from pfsense_api_client.client import ClientConfig, PFSenseAPIClient

class TestClientAuth(unittest.TestCase):

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

    def setUp(self):
        config = ClientConfig(**self.test_config)
        self.client = PFSenseAPIClient(config=config)

    @patch('pfsense_api_client.client.client.PFSenseAPIClient.call')
    def test_request_access_token(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.request_access_token()

        mock_call.assert_called_once_with(url="/api/v1/access_token", method="POST")
        self.assertEqual(response, mock_response)

    @patch('pfsense_api_client.client.client.PFSenseAPIClient.call')
    def test_execute_shell_command(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response
        shell_cmd = "ls"

        response = self.client.execute_shell_command(shell_cmd)

        mock_call.assert_called_once_with(url="/api/v1/diagnostics/command_prompt", method="POST", payload={"shell_cmd": shell_cmd})
        self.assertEqual(response, mock_response)
