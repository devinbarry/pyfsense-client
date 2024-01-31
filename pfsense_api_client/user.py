""" user-related functionality """

from typing import Any, Dict

from requests import Response

from client.api_types import ClientBase


def create_users(self: ClientBase, **args: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-users"""
    url = "/api/v1/user"
    method = "POST"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def delete_users(self: ClientBase, **args: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-users"""
    url = "/api/v1/user"
    method = "DELETE"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def get_users(self: ClientBase, *filterargs: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#3-read-users"""
    url = "/api/v1/user"
    response: Response = self.call(url, params=filterargs)
    return response


def update_users(self: ClientBase, **args: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-update-users"""
    url = "/api/v1/user"
    method = "PUT"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def create_ldap_auth_servers(
    self: ClientBase, **args: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-ldap-auth-servers"""
    url = "/api/v1/user/auth_server/ldap"
    method = "POST"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def create_radius_auth_servers(
    self: ClientBase, **args: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-create-radius-auth-servers"""
    url = "/api/v1/user/auth_server/radius"
    method = "POST"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def delete_auth_servers(self: ClientBase, **args: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#3-delete-auth-servers"""
    url = "/api/v1/user/auth_server"
    method = "DELETE"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def delete_ldap_auth_servers(
    self: ClientBase, **args: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#4-delete-ldap-auth-servers"""
    url = "/api/v1/user/auth_server/ldap"
    method = "DELETE"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def delete_radius_auth_servers(
    self: ClientBase, **args: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#5-delete-radius-auth-servers"""
    url = "/api/v1/user/auth_server/radius"
    method = "DELETE"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def get_auth_servers(
    self: ClientBase, *filterargs: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#6-read-auth-servers"""
    url = "/api/v1/user/auth_server"
    response: Response = self.call(url, payload=filterargs)
    return response


def get_ldap_auth_servers(
    self: ClientBase, *filterargs: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#7-read-ldap-auth-servers"""
    url = "/api/v1/user/auth_server/ldap"
    response: Response = self.call(url, payload=filterargs)
    return response


def get_radius_auth_servers(
    self: ClientBase, *filterargs: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#8-read-radius-auth-servers"""
    url = "/api/v1/user/auth_server/radius"
    response: Response = self.call(url, payload=filterargs)
    return response


def create_user_group(self: ClientBase, **args: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-user-group"""
    url = "/api/v1/user/group"
    method = "POST"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def delete_user_group(self: ClientBase, **args: Dict[str, Any]) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-user-group"""
    url = "/api/v1/user/group"
    method = "DELETE"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def create_user_privileges(
    self: ClientBase, **args: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#1-create-user-privileges"""
    url = "/api/v1/user/privilege"
    method = "POST"
    response: Response = self.call(url=url, method=method, payload=args)
    return response


def delete_user_privileges(
    self: ClientBase, **args: Dict[str, Any]
) -> Response:
    """https://github.com/jaredhendrickson13/pfsense-api/blob/master/README.md#2-delete-user-privileges"""
    url = "/api/v1/user/privilege"
    method = "DELETE"
    response: Response = self.call(url=url, method=method, payload=args)
    return response
