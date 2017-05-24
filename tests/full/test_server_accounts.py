import base.docker.docker_commands
import tractdb.server.accounts
import unittest


TEST_ACCOUNT = 'test-account'
TEST_ACCOUNT_PASSWORD = 'test-account-password'
TEST_ROLE = 'test-role'


def setup():
    pass


def teardown():
    pass


class TestServerAccounts(unittest.TestCase):
    @property
    def admin(self):
        return tractdb.server.accounts.AccountsAdmin(
            couchdb_url='http://{}:5984'.format(
                base.docker.docker_commands.machine_ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    def setUp(self):
        if TEST_ACCOUNT in self.admin.list_accounts():
            self.admin.delete_account(TEST_ACCOUNT)

    def tearDown(self):
        if TEST_ACCOUNT in self.admin.list_accounts():
            self.admin.delete_account(TEST_ACCOUNT)

    def test_create_delete_account(self):
        self.assertNotIn(
            TEST_ACCOUNT,
            self.admin.list_accounts()
        )

        self.admin.create_account(
            TEST_ACCOUNT,
            TEST_ACCOUNT_PASSWORD
        )

        self.assertIn(
            TEST_ACCOUNT,
            self.admin.list_accounts()
        )

        self.admin.delete_account(
            TEST_ACCOUNT
        )

        self.assertNotIn(
            TEST_ACCOUNT,
            self.admin.list_accounts()
        )

    def test_add_delete_role(self):
        self.assertNotIn(
            TEST_ACCOUNT,
            self.admin.list_accounts()
        )

        self.admin.create_account(
            TEST_ACCOUNT,
            TEST_ACCOUNT_PASSWORD
        )

        self.assertIn(
            TEST_ACCOUNT,
            self.admin.list_accounts()
        )

        self.assertNotIn(
            TEST_ROLE,
            self.admin.list_roles(
                TEST_ACCOUNT
            )
        )

        self.admin.add_role(
            TEST_ACCOUNT,
            TEST_ROLE
        )

        self.assertIn(
            TEST_ROLE,
            self.admin.list_roles(
                TEST_ACCOUNT
            )
        )

        self.admin.delete_role(
            TEST_ACCOUNT,
            TEST_ROLE
        )

        self.assertNotIn(
            TEST_ROLE,
            self.admin.list_roles(
                TEST_ACCOUNT
            )
        )

        self.admin.delete_account(
            TEST_ACCOUNT
        )

        self.assertNotIn(
            TEST_ACCOUNT,
            self.admin.list_accounts()
        )

    def test_list_accounts(self):
        self.assertIsInstance(
            self.admin.list_accounts(),
            list
        )

    def test_list_roles(self):
        self.admin.create_account(
            TEST_ACCOUNT,
            TEST_ACCOUNT_PASSWORD
        )

        self.assertIsInstance(
            self.admin.list_roles(TEST_ACCOUNT),
            list
        )

        self.admin.delete_account(
            TEST_ACCOUNT
        )
