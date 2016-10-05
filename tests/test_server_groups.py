import tests.docker_base as docker_base
import tractdb.server.groups
import unittest


def setup():
    pass


def teardown():
    pass


class TestTractDBAdmin(unittest.TestCase):
    @property
    def admin(self):
        return tractdb.server.groups.GroupsAdmin(
            couchdb_url='http://{}:5984'.format(
                docker_base.ip()
            ),
            couchdb_admin='docker-couchdb-test-admin',
            couchdb_admin_password='docker-couchdb-test-admin-password'
        )

    def test_create_delete_group(self):
        self.assertNotIn(
            'test-create-group',
            self.admin.list_groups()
        )

        self.admin.create_group(
            'test-create-group',
            'test-create-group-admin'
        )

        self.assertIn(
            'test-create-group',
            self.admin.list_groups()
        )

        self.admin.delete_group(
            'test-create-group'
        )

        self.assertNotIn(
            'test-create-group',
            self.admin.list_groups()
        )

    def test_list_groups(self):
        self.assertIsInstance(
            self.admin.list_groups(),
            list
        )
