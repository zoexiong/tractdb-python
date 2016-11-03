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

        # Add the role to the roles list
        existing_roles.append(role)

        # get the rev to make sure we are on the right revision
        rev = doc_user["_rev"]

        # Update the user (type and name are required to update user)
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

        # Delete it from the roles list
        existing_roles.remove(role)

        # get the rev to make sure we are on the right revision
        rev = doc_user["_rev"]

        # Update the user (type and name are required to update user)
        doc_updated_user = {
            'type': 'user',
            '_id': docid_user,
            'name': account,
            'roles': existing_roles,
            "_rev": rev
        }
        database_users.save(doc_updated_user)

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
