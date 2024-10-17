import unittest
from pydantic import ValidationError
from pyfsense_client.models.firewall_alias import FirewallAlias, FirewallAliasCreate, FirewallAliasUpdate, AliasType


class TestFirewallAliasModels(unittest.TestCase):

    def test_firewall_alias_base_with_string_fields(self):
        alias = FirewallAlias(
            name='test_alias',
            type=AliasType.HOST,
            address='192.168.1.1 192.168.1.2',
            detail='Server1||Server2',
            descr='Test alias description'
        )
        self.assertEqual(alias.address, ['192.168.1.1', '192.168.1.2'])
        self.assertEqual(alias.detail, ['Server1', 'Server2'])

    def test_firewall_alias_base_with_list_fields(self):
        alias = FirewallAlias(
            name='test_alias',
            type=AliasType.HOST,
            address=['192.168.1.1', '192.168.1.2'],
            detail=['Server1', 'Server2'],
            descr='Test alias description'
        )
        self.assertEqual(alias.address, ['192.168.1.1', '192.168.1.2'])
        self.assertEqual(alias.detail, ['Server1', 'Server2'])

    def test_firewall_alias_create(self):
        alias = FirewallAliasCreate(
            name='test_alias',
            type=AliasType.PORT,
            address='80 443',
            detail='HTTP||HTTPS',
            apply=False
        )
        self.assertEqual(alias.apply, False)
        self.assertEqual(alias.address, ['80', '443'])
        self.assertEqual(alias.detail, ['HTTP', 'HTTPS'])

    def test_firewall_alias_update(self):
        alias = FirewallAliasUpdate(
            id='existing_alias',
            name='updated_alias',
            type=AliasType.NETWORK,
            address='10.0.0.0/24 10.0.1.0/24',
            detail='Subnet1||Subnet2',
            apply=True
        )
        self.assertEqual(alias.id, 'existing_alias')
        self.assertEqual(alias.apply, True)

    def test_invalid_alias_type(self):
        with self.assertRaises(ValidationError):
            FirewallAlias(
                name='invalid_alias',
                type='invalid_type',  # This should raise a validation error
                address='192.168.1.1',
                detail='Invalid'
            )

    def test_missing_fields(self):
        with self.assertRaises(ValidationError):
            FirewallAlias(
                name='missing_fields',
                type=AliasType.HOST
                # Missing 'address' and 'detail'
            )
