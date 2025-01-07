import uuid
import json
import random
import unittest
from requests.models import Response
from unittest.mock import patch

from pyfsense_client.v1.client import ClientConfig, PfSenseV1Client


def randomize_string(length=16):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))


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
        self.client = PfSenseV1Client(config=config)

    @patch('pyfsense_client.v1.client.client.PfSenseV1Client._request')
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
                "system_platform": random.choice(["Netgate pfSense Plus", "Linux Ubuntu", "Windows Server"]),
                "system_serial": randomize_string(16),
                "system_netgate_id": uuid.uuid4().hex,
                "bios_vendor": random.choice(["American Megatrends Inc.", "Phoenix Technologies Ltd.", "Dell Inc."]),
                "bios_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}{chr(random.randint(97, 102))}",
                "bios_date": f"{random.randint(1, 12):02d}/{random.randint(1, 31):02d}/{random.randint(2010, 2024)}",
                "cpu_model": random.choice([
                    "Intel(R) Xeon(R) D-2123IT CPU @ 2.20GHz",
                    "AMD Ryzen 5 3600 6-Core Processor",
                    "Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz"
                ]),
                "kernel_pti": random.choice([True, False]),
                "mds_mitigation": random.choice(["active", "inactive"]),
                "temp_c": round(random.uniform(20, 80), 1),
                "temp_f": round(random.uniform(68, 176), 1),
                "load_avg": [round(random.uniform(0.0, 2.0), 2) for _ in range(3)],
                "cpu_count": random.choice([4, 8, 16, 32]),
                "mbuf_usage": round(random.uniform(0.01, 0.10), 2),
                "mem_usage": round(random.uniform(0.05, 0.50), 2),
                "swap_usage": round(random.uniform(0.0, 0.10), 2),
                "disk_usage": round(random.uniform(0.01, 0.20), 2)
            }
        }).encode('utf-8')

        mock_response.headers = {'Content-Type': 'application/json'}  # Add this line

        # Set the return value of the _request method to the mock response
        mock_request.return_value = mock_response

        # Call the get_system_status method
        response = self.client.get_system_status()

        # Now response should be an APIResponse object
        # Check if the returned response data matches the mock data
        expected_data = json.loads(mock_response._content)
        self.assertEqual(response.model_dump(by_alias=True), expected_data)

        # Verify if the call method was called with the correct arguments
        mock_request.assert_called_once_with(url="/api/v1/status/system", method="GET", payload={})

    @patch('pyfsense_client.v1.client.client.PfSenseV1Client._request')
    def test_get_system_status_with_list_data(self, mock_request):
        # Create a mock response with list data
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({
            "status": "ok",
            "code": 200,
            "return": 0,
            "message": "Success",
            "data": [
                {"name": "System 1", "status": "online"},
                {"name": "System 2", "status": "offline"},
                {"name": "System 3", "status": "online"}
            ]
        }).encode('utf-8')

        mock_response.headers = {'Content-Type': 'application/json'}

        # Set the return value of the _request method to the mock response
        mock_request.return_value = mock_response

        # Call the get_system_status method
        response = self.client.get_system_status()

        # Check if the returned response data matches the mock data
        expected_data = json.loads(mock_response._content)
        self.assertEqual(response.model_dump(by_alias=True), expected_data)

        # Verify if the call method was called with the correct arguments
        mock_request.assert_called_once_with(url="/api/v1/status/system", method="GET", payload={})
