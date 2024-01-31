import unittest
from unittest.mock import patch, MagicMock
from pfsense_api_client.client import ClientConfig, PFSenseAPIClient

class TestStatusMixin(unittest.TestCase):
    
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
    def test_get_carp_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_carp_status()

        mock_call.assert_called_once_with(url="/api/v1/status/carp", payload={})
        self.assertEqual(response, mock_response)

    @patch('pfsense_api_client.client.client.PFSenseAPIClient.call')
    def test_update_carp_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.update_carp_status(enable=True, maintenance_mode=True)

        mock_call.assert_called_once_with(url="/api/v1/status/carp", method="PUT", payload={"enable": True, "maintenance_mode": True})
        self.assertEqual(response, mock_response)

    @patch('pfsense_api_client.client.client.PFSenseAPIClient.call')
    def test_get_gateway_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_gateway_status()

        mock_call.assert_called_once_with(url="/api/v1/status/gateway", payload={})
        self.assertEqual(response, mock_response)
