import base.docker.docker_commands
import tractdb.client
import unittest


TEST_ACCOUNT = 'test-account'
TEST_ACCOUNT_PASSWORD = 'test-account-password'
TEST_ROLE = 'test-role'


def setup():
    pass


def teardown():
    pass


class TestClientAccounts(unittest.TestCase):
    @property
    def client_admin(self):
        return tractdb.client.TractDBClient(
            tractdb_url='http://{}:8080'.format(
                base.docker.docker_commands.machine_ip()
            ),
            client_account='docker-couchdb-test-admin',
            client_account_password='docker-couchdb-test-admin-password'
        )

    def setUp(self):
        if TEST_ACCOUNT in self.client_admin.list_accounts():
            self.client_admin.delete_account(TEST_ACCOUNT)

    def tearDown(self):
        if TEST_ACCOUNT in self.client_admin.list_accounts():
            self.client_admin.delete_account(TEST_ACCOUNT)

    def test_create_delete_account(self):
        self.assertNotIn(
            TEST_ACCOUNT,
            self.client_admin.list_accounts()
        )

        self.client_admin.create_account(
            TEST_ACCOUNT,
            TEST_ACCOUNT_PASSWORD
        )

        self.assertIn(
            TEST_ACCOUNT,
            self.client_admin.list_accounts()
        )

        self.client_admin.delete_account(
            TEST_ACCOUNT
        )

        self.assertNotIn(
            TEST_ACCOUNT,
            self.client_admin.list_accounts()
        )

    def test_add_delete_role(self):
        self.client_admin.create_account(
            TEST_ACCOUNT,
            TEST_ACCOUNT_PASSWORD
        )

        self.assertNotIn(
            TEST_ROLE,
            self.client_admin.list_roles(
                TEST_ACCOUNT
            )
        )

        self.client_admin.add_role(
            TEST_ACCOUNT,
            TEST_ROLE
        )

        self.assertIn(
            TEST_ROLE,
            self.client_admin.list_roles(
                TEST_ACCOUNT
            )
        )

        self.client_admin.delete_role(
            TEST_ACCOUNT,
            TEST_ROLE
        )

        self.assertNotIn(
            TEST_ROLE,
            self.client_admin.list_roles(
                TEST_ACCOUNT
            )
        )

        self.client_admin.delete_account(
            TEST_ACCOUNT
        )

    def test_list_accounts(self):
        self.assertIsInstance(
            self.client_admin.list_accounts(),
            list
        )

    def test_list_roles(self):
        self.client_admin.create_account(
            TEST_ACCOUNT,
            TEST_ACCOUNT_PASSWORD
        )

        self.assertIsInstance(
            self.client_admin.list_roles(TEST_ACCOUNT),
            list
        )

        self.client_admin.delete_account(
            TEST_ACCOUNT
        )
