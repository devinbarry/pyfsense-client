import unittest
from unittest.mock import patch, MagicMock
from v1.client import ClientConfig, PFSenseAPIClient

from ..mocks import get_response_json


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

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_carp_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_carp_status()

        mock_call.assert_called_once_with(url="/api/v1/status/carp", method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_update_carp_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.update_carp_status(enable=True, maintenance_mode=True)

        mock_call.assert_called_once_with(url="/api/v1/status/carp", method="PUT",
                                          payload={"enable": True, "maintenance_mode": True})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_gateway_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_gateway_status()

        mock_call.assert_called_once_with(url="/api/v1/status/gateway", method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_system_status(self, mock_call):
        mock_response = MagicMock()
        mock_response.json.return_value = get_response_json()
        mock_call.return_value = mock_response

        response = self.client.get_system_status()

        mock_call.assert_called_once_with(url='/api/v1/status/system', method='GET', payload={})
        self.assertEqual(response, mock_response)


    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_interface_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_interface_status()

        mock_call.assert_called_once_with(url="/api/v1/status/interface", method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_configuration_history_status_log(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_configuration_history_status_log()

        mock_call.assert_called_once_with(url="/api/v1/status/log/config_history", method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_dhcp_status_log(self, mock_call):
        mock_response = MagicMock()
        mock_response.json.return_value = get_response_json()
        mock_call.return_value = mock_response

        response = self.client.get_dhcp_status_log()

        mock_call.assert_called_once_with(url='/api/v1/status/log/dhcp', method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_firewall_status_log(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_firewall_status_log()

        mock_call.assert_called_once_with(url="/api/v1/status/log/firewall", method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_system_status_log(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_system_status_log()

        mock_call.assert_called_once_with(url="/api/v1/status/log/system", method='GET', payload={})
        self.assertEqual(response, mock_response)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_openvpn_status(self, mock_call):
        mock_response = MagicMock()
        mock_call.return_value = mock_response

        response = self.client.get_openvpn_status()

        mock_call.assert_called_once_with(url="/api/v1/status/openvpn", method='GET', payload={})
        self.assertEqual(response, mock_response)

