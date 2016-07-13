import os
import requests
import subprocess
import unittest


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


class TestConnect(unittest.TestCase):
<<<<<<< HEAD
    def test_connect_couchdb(self):
        response = requests.get(
            'http://{}:5984'.format(
=======
    def test_connect(self):
        response = requests.get(
            'http://{}'.format(
>>>>>>> d176b860bf2b937c42dab643394b39acab964344
                BASE_DOCKER_IP
            )
        )

        print(response.content)

        self.assertEqual(
            response.status_code,
            200
        )
<<<<<<< HEAD
=======

>>>>>>> d176b860bf2b937c42dab643394b39acab964344
