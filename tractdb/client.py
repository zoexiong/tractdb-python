import requests


class TractDBClient(object):
    """ Client for interacting with a TractDB instance.
    """

    def __init__(self, tractdb_url, client_account, client_account_password):
        """ Create an admin object.
        """
        self._tractdb_url = tractdb_url
        self._client_account = client_account
        self._client_account_password = client_account_password

    # def add_role(self, account, role):

    def create_account(self, account, account_password):
        """ Create an account.
        """

        response = requests.post(
            '{}/{}'.format(
                self._tractdb_url,
                'accounts'
            ),
            json={
                'account': account,
                'password': account_password
            }
        )

    def delete_account(self, account):
        """ Delete an account.
        """

        response = requests.delete(
            '{}/{}/{}'.format(
                self._tractdb_url,
                'account',
                account
            )
        )

        print(response)

    # def delete_role(self, account, role):

    def list_accounts(self):
        """ List our accounts.
        """

        response = requests.get(
            '{}/{}'.format(
                self._tractdb_url,
                'accounts'
            )
        )

        json = response.json()

        return json['accounts']

    # def list_roles(self, account):
