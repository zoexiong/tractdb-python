import tests.docker_base as docker_base
import tractdb.server.accounts
import tractdb.server.documents
import unittest


TEST_ACCOUNT = 'test-account'
TEST_ACCOUNT_PASSWORD = 'test-account-password'
TEST_ROLE = 'test-role'
TEST_CONTENT = {"user_id": "001", "text":"some content", "date":"03/20/2017"}
TEST_UPDATED_CONTENT = {"user_id": "001", "text":"some new content added", "date":"03/20/2017"}
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
            TEST_CONTENT,
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

    def test_update_read_document(self):
        # Ensure the doc exists
        self.assertNotIn(
            TEST_DOC_ID,
            self.admin.list_documents(TEST_ACCOUNT)
        )

        self.admin.create_doc(
            TEST_CONTENT,
            TEST_DOC_ID,
            TEST_ACCOUNT
        )

        self.assertIn(
            TEST_DOC_ID,
            self.admin.list_documents(TEST_ACCOUNT)
        )

        # Read the doc
        doc = self.admin.read_doc(
            TEST_DOC_ID,
            TEST_ACCOUNT
        )

        # Ensure we get the right content
        self.assertEquals(
            doc['content'],
            TEST_CONTENT
        )

        # Update the doc
        self.admin.update_doc(TEST_UPDATED_CONTENT, TEST_DOC_ID, TEST_ACCOUNT)

        # Ensure the doc is updated, get the new content
        doc_updated = self.admin.read_doc(
            TEST_DOC_ID,
            TEST_ACCOUNT
        )

        self.assertEquals(
            doc_updated['content'],
            TEST_UPDATED_CONTENT
        )

        # Delete the doc
        self.admin.delete_doc(
            TEST_DOC_ID,
            TEST_ACCOUNT
        )

        self.assertNotIn(
            TEST_DOC_ID,
            self.admin.list_documents(TEST_ACCOUNT)
        )

    def test_list_documents(self):
        self.assertIsInstance(
            self.admin.list_documents(TEST_ACCOUNT),
            list
        )



