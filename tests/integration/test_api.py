import unittest
import json
from .utils import client

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = client

    def test_get_system_api_version(self):
        """ tests getting the API version """
        response = self.client.get_system_api_version()
        print(json.dumps(response.dict()))
        self.assertTrue(response.status)

    def test_update_system_api_configuration(self):
        """ tests setting the API to not-read-only """
        response = self.client.update_system_api_configuration(readonly=False)
        print(json.dumps(response.json()))
        self.assertIsNotNone(response)
