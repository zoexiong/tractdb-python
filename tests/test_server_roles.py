import tests.docker_base as docker_base
import tractdb.server.roles
import unittest


def setup():
    pass


def teardown():
    pass

class TestTractDBAdmin(unittest.TestCase):
    @property
    def admin(self):
        return tractdb.server.roles.RolesAdmin(
            couchdb_url='http://{}:5984'.format(
                docker_base.ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    def test_add_role(self):
        self.admin.add_role(
            account="wwww",
            role="users_admin"
        )

    def test_delete_role(self):
        self.admin.delete_role(
            account="wwww",
            role="users_admin"
        )