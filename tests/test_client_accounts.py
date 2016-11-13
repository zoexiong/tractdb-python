import tests.docker_base as docker_base
import tractdb.client
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
    def client_admin(self):
        return tractdb.client.TractDBClient(
            tractdb_url='http://{}:8080'.format(
                docker_base.ip()
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
        pass
        # self.assertNotIn(
        #     TEST_ACCOUNT,
        #     self.admin.list_accounts()
        # )
        #
        # self.admin.create_account(
        #     TEST_ACCOUNT,
        #     TEST_ACCOUNT_PASSWORD
        # )
        #
        # self.assertIn(
        #     TEST_ACCOUNT,
        #     self.admin.list_accounts()
        # )
        #
        # self.assertNotIn(
        #     TEST_ROLE,
        #     self.admin.list_roles(
        #         TEST_ACCOUNT
        #     )
        # )
        #
        # self.admin.add_role(
        #     TEST_ACCOUNT,
        #     TEST_ROLE
        # )
        #
        # self.assertIn(
        #     TEST_ROLE,
        #     self.admin.list_roles(
        #         TEST_ACCOUNT
        #     )
        # )
        #
        # self.admin.delete_role(
        #     TEST_ACCOUNT,
        #     TEST_ROLE
        # )
        #
        # self.assertNotIn(
        #     TEST_ROLE,
        #     self.admin.list_roles(
        #         TEST_ACCOUNT
        #     )
        # )
        #
        # self.admin.delete_account(
        #     TEST_ACCOUNT
        # )
        #
        # self.assertNotIn(
        #     TEST_ACCOUNT,
        #     self.admin.list_accounts()
        # )

    def test_list_accounts(self):
        self.assertIsInstance(
            self.client_admin.list_accounts(),
            list
        )

    def test_list_roles(self):
        pass
        # self.admin.create_account(
        #     TEST_ACCOUNT,
        #     TEST_ACCOUNT_PASSWORD
        # )
        #
        # self.assertIsInstance(
        #     self.admin.list_roles(TEST_ACCOUNT),
        #     list
        # )
        #
        # self.admin.delete_account(
        #     TEST_ACCOUNT
        # )
