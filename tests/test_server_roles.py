import tests.docker_base as docker_base
import tractdb.server.roles
import unittest


def setup():
    pass


def teardown():
    pass


class TestServerRoles(unittest.TestCase):
    @property
    def accounts_admin(self):
        return tractdb.server.accounts.AccountsAdmin(
            couchdb_url='http://{}:5984'.format(
                docker_base.ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    @property
    def roles_admin(self):
        return tractdb.server.roles.RolesAdmin(
            couchdb_url='http://{}:5984'.format(
                docker_base.ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    def test_add_delete_role(self):
        if 'test-create-account' in self.accounts_admin.list_accounts():
            self.accounts_admin.delete_account('test-create-account')

        self.assertNotIn(
            'test-create-account',
            self.accounts_admin.list_accounts()
        )

        self.accounts_admin.create_account(
            'test-create-account',
            'test-create-account-password'
        )

        self.assertIn(
            'test-create-account',
            self.accounts_admin.list_accounts()
        )

        self.assertNotIn(
            'test-role',
            self.roles_admin.list_roles(
                'test-create-account'
            )
        )

        self.roles_admin.add_role(
            'test-create-account',
            'test-role'
        )

        self.assertIn(
            'test-role',
            self.roles_admin.list_roles(
                'test-create-account'
            )
        )

        self.roles_admin.delete_role(
            'test-create-account',
            'test-role'
        )

        self.assertNotIn(
            'test-role',
            self.roles_admin.list_roles(
                'test-create-account'
            )
        )

        self.accounts_admin.delete_account(
            'test-create-account'
        )

        self.assertNotIn(
            'test-create-account',
            self.accounts_admin.list_accounts()
        )

    def test_list_roles(self):
        if 'test-create-account' in self.accounts_admin.list_accounts():
            self.accounts_admin.delete_account('test-create-account')

        self.accounts_admin.create_account(
            'test-create-account',
            'test-create-account-password'
        )

        self.assertIsInstance(
            self.roles_admin.list_roles('test-create-account'),
            list
        )

        self.accounts_admin.delete_account(
            'test-create-account'
        )
