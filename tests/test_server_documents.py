import tests.docker_base as docker_base
import tractdb.server.accounts
import tractdb.server.documents
import unittest


TEST_ACCOUNT = 'test-account'
TEST_ACCOUNT_PASSWORD = 'test-account-password'
TEST_ROLE = 'test-role'
TEST_DOC = {"user_id": "001", "content":"some content", "date":"03/20/2017"}
TEST_DOC_ID = "docid_test"


def setup():
    pass


def teardown():
    pass


class TestServerDocuments(unittest.TestCase):
    @property
    def accountAdmin(self):
        return tractdb.server.accounts.AccountsAdmin(
            couchdb_url='http://{}:5984'.format(
                docker_base.ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    @property
    def admin(self):
        return tractdb.server.documents.DocumentsAdmin(
            couchdb_url='http://{}:5984'.format(
                docker_base.ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    def setUp(self):
        if TEST_ACCOUNT not in self.accountAdmin.list_accounts():
            self.accountAdmin.create_account(TEST_ACCOUNT, TEST_ACCOUNT_PASSWORD)

    def tearDown(self):
        if TEST_ACCOUNT in self.accountAdmin.list_accounts():
            self.accountAdmin.delete_account(TEST_ACCOUNT)


    def test_create_delete_document(self):
        # ensure doc with given id does not exist
        self.assertNotIn(
            TEST_DOC_ID,
            self.admin.list_documents(TEST_ACCOUNT)
        )

        self.admin.create_doc(
            TEST_DOC,
            TEST_DOC_ID,
            TEST_ACCOUNT
        )

        self.assertIn(
            TEST_DOC_ID,
            self.admin.list_documents(TEST_ACCOUNT)
        )

        self.admin.delete_doc(
            TEST_DOC_ID,
            TEST_ACCOUNT
        )

        self.assertNotIn(
            TEST_DOC_ID,
            self.admin.list_documents(TEST_ACCOUNT)
        )

    # def test_add_delete_role(self):
    #     self.assertNotIn(
    #         TEST_ACCOUNT,
    #         self.admin.list_accounts()
    #     )
    #
    #     self.admin.create_account(
    #         TEST_ACCOUNT,
    #         TEST_ACCOUNT_PASSWORD
    #     )
    #
    #     self.assertIn(
    #         TEST_ACCOUNT,
    #         self.admin.list_accounts()
    #     )
    #
    #     self.assertNotIn(
    #         TEST_ROLE,
    #         self.admin.list_roles(
    #             TEST_ACCOUNT
    #         )
    #     )
    #
    #     self.admin.add_role(
    #         TEST_ACCOUNT,
    #         TEST_ROLE
    #     )
    #
    #     self.assertIn(
    #         TEST_ROLE,
    #         self.admin.list_roles(
    #             TEST_ACCOUNT
    #         )
    #     )
    #
    #     self.admin.delete_role(
    #         TEST_ACCOUNT,
    #         TEST_ROLE
    #     )
    #
    #     self.assertNotIn(
    #         TEST_ROLE,
    #         self.admin.list_roles(
    #             TEST_ACCOUNT
    #         )
    #     )
    #
    #     self.admin.delete_account(
    #         TEST_ACCOUNT
    #     )
    #
    #     self.assertNotIn(
    #         TEST_ACCOUNT,
    #         self.admin.list_accounts()
    #     )
    #
    # def test_list_accounts(self):
    #     self.assertIsInstance(
    #         self.admin.list_accounts(),
    #         list
    #     )
    #
    # def test_list_roles(self):
    #     self.admin.create_account(
    #         TEST_ACCOUNT,
    #         TEST_ACCOUNT_PASSWORD
    #     )
    #
    #     self.assertIsInstance(
    #         self.admin.list_roles(TEST_ACCOUNT),
    #         list
    #     )
    #
    #     self.admin.delete_account(
    #         TEST_ACCOUNT
    #     )