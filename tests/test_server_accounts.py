# import tests.docker_base as docker_base
# import tractdb.server.accounts
# import unittest
#
#
# def setup():
#     pass
#
#
# def teardown():
#     pass
#
#
# class TestTractDBAdmin(unittest.TestCase):
#     @property
#     def admin(self):
#         return tractdb.server.accounts.AccountsAdmin(
#             couchdb_url='http://{}:5984'.format(
#                 docker_base.ip()
#             ),
#             couchdb_admin='docker-couchdb-test-admin',
#             couchdb_admin_password='docker-couchdb-test-admin-password'
#         )
#
#     def test_create_delete_account(self):
#         self.assertNotIn(
#             'test-create-account',
#             self.admin.list_accounts()
#         )
#
#         self.admin.create_account(
#             'test-create-account',
#             'test-create-account-password'
#         )
#
#         self.assertIn(
#             'test-create-account',
#             self.admin.list_accounts()
#         )
#
#         self.admin.delete_account(
#             'test-create-account'
#         )
#
#         self.assertNotIn(
#             'test-create-account',
#             self.admin.list_accounts()
#         )
#
#     def test_list_accounts(self):
#         self.assertIsInstance(
#             self.admin.list_accounts(),
#             list
#         )
