import unittest
from unittest.mock import patch
from pyfsense_client.client import ClientConfig, PFSenseAPIClient
from pyfsense_client.models import FirewallAliasCreate, FirewallAliasUpdate

class TestFirewallAliasMethods(unittest.TestCase):

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
    def test_get_firewall_alias(self, mock_call):
        pass

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_get_firewall_alias_by_name(self, mock_call):
        pass

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_create_firewall_alias(self, mock_call):
        pass

    @patch('pyfsense_client.client.client.PFSenseAPIClient.call')
    def test_delete_firewall_alias(self, mock_call):
        pass
