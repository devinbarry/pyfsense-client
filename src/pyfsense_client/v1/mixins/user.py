from typing import Any, Dict

from ..client import ClientABC, APIResponse


class UserMixin(ClientABC):
    def create_users(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-users"""
        url = "/api/v1/user"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_users(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-users"""
        url = "/api/v1/user"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)

    def get_users(self, *args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#3-read-users"""
        url = "/api/v1/user"
        method = "GET"
        return self.call(url=url, method=method, payload=args)

    def update_users(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-users"""
        url = "/api/v1/user"
        method = "PUT"
        return self.call(url=url, method=method, payload=args)

    def create_ldap_auth_servers(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-ldap-auth-servers"""
        url = "/api/v1/user/auth_server/ldap"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def create_radius_auth_servers(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-create-radius-auth-servers"""
        url = "/api/v1/user/auth_server/radius"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_auth_servers(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#3-delete-auth-servers"""
        url = "/api/v1/user/auth_server"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)

    def delete_ldap_auth_servers(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-delete-ldap-auth-servers"""
        url = "/api/v1/user/auth_server/ldap"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)

    def delete_radius_auth_servers(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#5-delete-radius-auth-servers"""
        url = "/api/v1/user/auth_server/radius"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)

    def get_auth_servers(self, *filterargs: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#6-read-auth-servers"""
        url = "/api/v1/user/auth_server"
        return self.call(url=url, method="GET", payload=filterargs)

    def get_ldap_auth_servers(self, *filterargs: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#7-read-ldap-auth-servers"""
        url = "/api/v1/user/auth_server/ldap"
        return self.call(url=url, method="GET", payload=filterargs)

    def get_radius_auth_servers(self, *filterargs: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#8-read-radius-auth-servers"""
        url = "/api/v1/user/auth_server/radius"
        return self.call(url=url, method="GET", payload=filterargs)

    def create_user_group(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-user-group"""
        url = "/api/v1/user/group"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_user_group(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-user-group"""
        url = "/api/v1/user/group"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)

    def create_user_privileges(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-user-privileges"""
        url = "/api/v1/user/privilege"
        method = "POST"
        return self.call(url=url, method=method, payload=args)

    def delete_user_privileges(self, **args: Dict[str, Any]) -> APIResponse:
        """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-user-privileges"""
        url = "/api/v1/user/privilege"
        method = "DELETE"
        return self.call(url=url, method=method, payload=args)
