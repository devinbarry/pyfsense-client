import unittest
from unittest.mock import patch
from v1.client import ClientConfig, PFSenseAPIClient

class TestDHCPMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_config = {
            "username": "test_user",
            "password": "test_pass",
            "hostname": "test.example.com",
            "mode": "jwt",
            "jwt": "test_jwt_token",
        }

    def setUp(self):
        config = ClientConfig(**self.test_config)
        self.client = PFSenseAPIClient(config=config)

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_dhcp_status_log(self, mock_call):
        pass

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_dhcpd_leases(self, mock_call):
        pass

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_dhcpd_service_configuration(self, mock_call):
        pass
