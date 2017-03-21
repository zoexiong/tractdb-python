import couchdb
import re
import urllib.parse


class DocumentsAdmin(object):
    """ Supports management of TractDB documents.
    """

    def __init__(self, couchdb_url, couchdb_admin, couchdb_admin_password):
        """ Create an admin object.
        """
        self._couchdb_url = couchdb_url
        self._couchdb_admin = couchdb_admin
        self._couchdb_admin_password = couchdb_admin_password

    def create_doc(self, doc, doc_id, account):
        """ Add a doc to a database.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)
        dbname = '{:s}_tractdb'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        # Get the database for the user
        database = server[dbname]
        # Set id for the doc
        doc.id = doc_id
        # Create and save the doc
        database.save(doc)

    def read_doc(self, doc_id, account):
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)
        dbname = '{:s}_tractdb'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        doc = database[doc_id]

        return doc

    def update_doc(self, updated_doc, doc_id, account):
        """ Update a doc.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)
        dbname = '{:s}_tractdb'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        # Add doc id to the doc in case doc id is not included in the uploaded doc file
        updated_doc.id = doc_id

        database.update([updated_doc])

    def delete_doc(self, doc_id, account):
        """ Delete a doc.
        """
        server = self._couchdb_server
        database_users = server['_users']
        docid_user = 'org.couchdb.user:{:s}'.format(account)
        dbname = '{:s}_tractdb'.format(account)

        # Confirm the user exists
        if docid_user not in database_users:
            raise Exception('User "{:s}" does not exist.'.format(account))

        # Confirm the database exists
        if dbname not in server:
            raise Exception('Database "{:s}" does not exist.'.format(dbname))

        database = server[dbname]

        # Confirm the document exists
        if doc_id not in database:
            raise Exception('Document "{:s}" does not exist.'.format(doc_id))

        # Delete it
        doc = database[doc_id]
        database.delete(doc)

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
