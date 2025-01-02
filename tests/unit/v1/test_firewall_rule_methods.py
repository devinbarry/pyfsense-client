import unittest
from unittest.mock import patch
from pyfsense_client.v1.client import ClientConfig, PFSenseAPIClient

class TestFirewallRuleMethods(unittest.TestCase):

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

    @patch('pyfsense_client.v1.client.client.PFSenseAPIClient.call')
    def test_get_firewall_rules(self, mock_call):
        pass

    @patch('pyfsense_client.v1.client.client.PFSenseAPIClient.call')
    def test_get_firewall_rules_interface_wan(self, mock_call):
        pass

    @patch('pyfsense_client.v1.client.client.PFSenseAPIClient.call')
    def test_get_firewall_rules_interface_lan(self, mock_call):
        pass
