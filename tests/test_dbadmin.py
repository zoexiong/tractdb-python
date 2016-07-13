import os
import subprocess
import tractdb.admin
import unittest


BASE_DOCKER_IP = None


def setup():
    global BASE_DOCKER_IP

    if 'BASE_DOCKER_ON_TRAVIS' in os.environ:
        BASE_DOCKER_IP = 'localhost'
    else:
        result = subprocess.run(
            ['invoke', 'docker_machine_ip'],
            stdout=subprocess.PIPE
        )

        BASE_DOCKER_IP = result.stdout.decode('utf-8', 'backslashreplace').strip()


def teardown():
    pass


class TestTractDBAdmin(unittest.TestCase):
    @property
    def admin(self):
        return tractdb.admin.TractDBAdmin(
            server_url='http://{}:{}'.format(BASE_DOCKER_IP, 5984),
            server_admin='docker-couchdb-test-admin',
            server_password='docker-couchdb-test-admin-password'
        )

    def test_create_delete_account(self):
        self.assertNotIn(
            'test-create-account',
            self.admin.list_accounts()
        )

        self.admin.create_account(
            'test-create-account',
            'test-create-account-password'
        )

        self.assertIn(
            'test-create-account',
            self.admin.list_accounts()
        )

        self.admin.delete_account(
            'test-create-account'
        )

        self.assertNotIn(
            'test-create-account',
            self.admin.list_accounts()
        )

    def test_list_accounts(self):
        self.assertIsInstance(
            self.admin.list_accounts(),
            list
        )
