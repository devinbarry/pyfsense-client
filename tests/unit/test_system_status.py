import json
import unittest
from requests.models import Response
from unittest.mock import patch

from pyfsense_client.client import ClientConfig, PFSenseAPIClient


class TestSystemStatus(unittest.TestCase):

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


    @patch('pyfsense_client.client.client.PFSenseAPIClient._request')
    def test_get_system_status_with_mock_response(self, mock_request):
        # Create a mock response
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({
            "status": "ok",
            "code": 200,
            "return": 0,
            "message": "Success",
            "data": {
                "system_platform": "Netgate pfSense Plus",
                "system_serial": "E349395X0900892",
                "system_netgate_id": "b8de6f8803d9503d49fa",
                "bios_vendor": "American Megatrends Inc.",
                "bios_version": "1.3a",
                "bios_date": "07/13/2020",
                "cpu_model": "Intel(R) Xeon(R) D-2123IT CPU @ 2.20GHz",
                "kernel_pti": True,
                "mds_mitigation": "inactive",
                "temp_c": 60,
                "temp_f": 136.4,
                "load_avg": [0.01, 0.05, 0.01],
                "cpu_count": 8,
                "mbuf_usage": 0.04,
                "mem_usage": 0.06,
                "swap_usage": 0,
                "disk_usage": 0.01
            }
        }).encode('utf-8')

        # Set the return value of the call method to the mock response
        mock_request.return_value = mock_response

        # Call the get_system_status method
        response = self.client.get_system_status()

        # Check if the returned response is equal to the mock response
        self.assertEqual(response.model_dump(by_alias=True), mock_response.json())

        # Verify if the call method was called with the correct arguments
        mock_request.assert_called_once_with(url="/api/v1/status/system", method="GET", payload={})
