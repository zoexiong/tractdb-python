import couchdb
import re
import urllib.parse


class RolesAdmin(object):
    """ Supports management of roles of TractDB accounts.
    """

    def __init__(self, couchdb_url, couchdb_admin, couchdb_admin_password):
        """ Create an admin object.
        """
        self._couchdb_url = couchdb_url
        self._couchdb_admin = couchdb_admin
        self._couchdb_admin_password = couchdb_admin_password

    def add_role(self, account, role):
        """ Add a role to an account.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Get the existing user document
        doc_user = database_users[docid_user]

        # Confirm the role does not already exist
        if role in doc_user['roles']:
            raise Exception('Role "{:s}" already exists.'.format(role))

        # Add the role and put it back
        doc_user['roles'].append(role)
        doc_user['roles'] = sorted(doc_user['roles'])
        database_users.update([doc_user])

    def delete_role(self, account, role):
        """ Delete a role from an account.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Get the existing user document
        doc_user = database_users[docid_user]

        # Confirm the role exists
        if role not in doc_user['roles']:
            raise Exception('Role "{:s}" does not exist.'.format(role))

        # Delete the role and put it back
        doc_user['roles'].remove(role)
        database_users.update([doc_user])

    def list_roles(self, account):
        """ Get the roles of an account.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Get the existing user document
        doc_user = database_users[docid_user]

        # Return the roles
        return doc_user['roles']

    def _format_server_url(self):
        """ Format the base URL we use for connecting to the server.
        """
        return '{}://{:s}:{:s}@{:s}'.format(
            urllib.parse.urlparse(self._couchdb_url).scheme,
            self._couchdb_admin,
            self._couchdb_admin_password,
            self._couchdb_url[
                len(urllib.parse.urlparse(self._couchdb_url).scheme) + len('://')
                :
            ]
        )

    @property
    def _couchdb_server(self):
        return couchdb.Server(self._format_server_url())
