import unittest
import requests


class TestFirewallAlias(unittest.TestCase):

    def setUp(self):
        self.client = PFSenseAPIClient(
            config_filename="~/.config/pfsense-api.json"
        )

    def test_get_firewall_alias(self):
        """ pulls the full list of aliases """
        result = self.client.get_firewall_alias()
        self.assertIsNotNone(result)
        print(result.json())

    def test_get_firewall_alias_name(self):
        """ pulls a firewall alias called zzz_testing """
        result: requests.Response = self.client.get_firewall_alias(name="zzz_testing")
        self.assertEqual(result.status_code, 200)
        self.assertIn("zzz_testing", result.text)
        print(result.json())

    def test_create_bogus_alias(self):
        """ creates an alias called zzz_bogus """
        try:
            result: requests.Response = self.client.create_firewall_alias(
                name="zzzbogus",
                alias_type="host",
                descr = "Bogus description",
                address = "bogus.lol",
                detail = "bogus.lol is bogus",
                apply = False,
            )
        except requests.exceptions.HTTPError as httperror:
            if httperror.response.status_code == 400:
                self.skipTest("Skipping because the alias 'zzzbogus' already exists")
            else:
                raise requests.exceptions.HTTPError from httperror

        self.assertEqual(result.status_code, 200)

    def test_delete_bogus_alias(self):
        """ deletes an alias called zzzbogus """
        result: requests.Response = self.client.delete_firewall_alias(
            name="zzzbogus",
            apply = False,
        )
        print(f"{result.content=}")
        self.assertEqual(result.status_code, 200)
