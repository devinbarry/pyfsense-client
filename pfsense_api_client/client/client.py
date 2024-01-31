import requests

from .base import ClientBase
from ..mixins.firewall import FirewallMixin
from ..mixins.service  import ServiceMixin
from ..mixins.status import StatusMixin
from ..mixins.system import SystemMixin


class PFSenseAPIClient(ClientBase, FirewallMixin, ServiceMixin, StatusMixin, SystemMixin):
    """pfSense API Client"""

    def request_access_token(self) -> requests.Response:
        """gets a temporary access token
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-request-access-token
        """
        url = "/api/v1/access_token"
        return self.call(url=url, method="POST")

    def execute_shell_command(self, shell_cmd: str) -> requests.Response:
        """execute a shell command on the firewall
        https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-execute-shell-command
        """
        url = "/api/v1/diagnostics/command_prompt"
        method = "POST"

        return self.call(
            url=url,
            method=method,
            payload={"shell_cmd": shell_cmd},
        )
