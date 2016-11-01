import couchdb
import re
import urllib.parse


class AccountsAdmin(object):
    """ Supports management of TractDB accounts.
    """

    def __init__(self, couchdb_url, couchdb_admin, couchdb_admin_password):
        """ Create an admin object.
        """
        self._couchdb_url = couchdb_url
        self._couchdb_admin = couchdb_admin
        self._couchdb_admin_password = couchdb_admin_password

    def add_role(self, account, role):
        """ Add a role to a user.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)

        # Confirm the user does exist
        if docid_user not in database_users:
            raise Exception('User "{:s}" not exists.'.format(account))

        # Get the existing document
        doc_user = database_users[docid_user]

        # Confirm role does not exists
        existing_roles = doc_user['roles']
        if role in existing_roles:
            raise Exception('role "{}" does exist.'.format(role))

        # Add the role
        existing_roles.append(role)

        # get the rev
        rev = doc_user["_rev"]

        # Update the user
        doc_updated_user = {
            'type': 'user',
            '_id': docid_user,
            'name': account,
            'roles': existing_roles,
            "_rev": rev
        }
        database_users.save(doc_updated_user)

    def delete_role(self, account, role):
        """ Delete a role.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Get the existing document
        doc_user = database_users[docid_user]

        # Confirm role exists
        existing_roles = doc_user['roles']
        if role not in existing_roles:
            raise Exception('role "{:s}" does not exist.'.format(role))

        # Delete it
        existing_roles.remove(role)

        # get the rev
        rev = doc_user["_rev"]

        # Update the user
        doc_updated_user = {
            'type': 'user',
            '_id': docid_user,
            'name': account,
            'roles': existing_roles,
            "_rev": rev
        }
        database_users.save(doc_updated_user)



    # def list_accounts(self):
    #     """ List our accounts.
    #     """
    #     couchdb_users = self._couchdb_users
    #     couchdb_databases = self._couchdb_databases
    #
    #     # Keep only users who have a corresponding database
    #     users = []
    #     for user_current in couchdb_users:
    #         # Our databases are defined by the user name plus the suffix '_tractdb'
    #         dbname = '{:s}_tractdb'.format(user_current)
    #
    #         if dbname in couchdb_databases:
    #             users.append(user_current)
    #
    #     return users
    #
    # def reset_password(self, account, account_password):
    #     """ Reset an account password.
    #     """
    #     server = self._couchdb_server
    #
    #     # Our databases are defined by the user name plus the suffix '_tractdb'
    #     dbname = '{:s}_tractdb'.format(account)
    #
    #     # Directly manipulate users database, since it's not meaningfully wrapped
    #     database_users = server['_users']
    #     docid_user = 'org.couchdb.user:{:s}'.format(account)
    #
    #     # Confirm the database exists
    #     if dbname not in server:
    #         raise Exception('Database "{:s}" does not exist.'.format(dbname))
    #
    #     # Confirm the user exists
    #     if docid_user not in database_users:
    #         raise Exception('User "{:s}" does not exist.'.format(account))
    #
    #     # Get the existing document
    #     doc_user = database_users[docid_user]
    #
    #     # Change the password and put it back
    #     doc_user['password'] = account_password
    #     database_users.update([doc_user])

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
    def _couchdb_databases(self):
        """ List what CouchDB databases exist.
        """
        server = self._couchdb_server

        # Our databases are defined by the user name plus the suffix '_tractdb'
        pattern = re.compile('.*_tractdb')
        dbnames = [dbname for dbname in server if pattern.match(dbname)]

        return dbnames

    @property
    def _couchdb_users(self):
        """ List what CouchDB users exist.
        """
        server = self._couchdb_server

        # Directly manipulate users database, since it's not meaningfully wrapped
        database_users = server['_users']

        # This is our docid pattern
        pattern = re.compile('org\.couchdb\.user:(.*)')

        # Keep only the users that match our pattern, extracting the user
        users = []
        for docid in database_users:
            match = pattern.match(docid)
            if match:
                account_user = match.group(1)
                users.append(account_user)

        return users

    @property
    def _couchdb_server(self):
        return couchdb.Server(self._format_server_url())
