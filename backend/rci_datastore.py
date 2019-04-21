import sqlite3
import os.path

_database = None


class DbTransaction:
    """
    Simplifies creating a database transaction 
    
    This is done by using a python context manager to place all the boiler
    plate code in one location.

    A check is performed to see if an existing connection exists.
    If it does not, it is created.

    When the context manager is used, it returns a cursor object.

    When the context manager is existed, it executes the commit() method
    """

    def __init__(self, connection_string=None, row_factory=None):
        if not connection_string:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'rci.db')

            connection_string = db_path 


        if not row_factory:
            row_factory = dict_factory

        self.connection_string = connection_string
        self.row_factory = row_factory
        
        global _database

        if _database is None:
            _database = sqlite3.connect(self.connection_string)
            _database.row_factory = self.row_factory

    def __enter__(self):
        cursor = _database.cursor()

        # Sqlite3 doesn't enable foreign keys by default.
        # See 2nd secion of the following link:
        # https://sqlite.org/foreignkeys.html
        cursor.execute('pragma foreign_keys = ON')

        return _database.cursor()

    def __exit__(self, *args):
        _database.commit()


# Free form querying 
def query(sql, sql_params):
    """
    Execute an SQL Query and returns the results.

    Be mindful of performance. If you have a huge table, avoid fetching the
    entire thing if it possible to limit the rows in some way.
    """
    with DbTransaction() as conn:
        if not sql_params:
            conn.execute(sql)
        else:
            conn.execute(sql, sql_params)

        return conn.fetchall()


def execute_script(sql_script):
    with DbTransaction() as conn:
        return conn.executescript(sql_script)


# Convenience methods 

# insert methods 
# naming convention: `def insert_{singularized_table_name}

def insert_user(user_id, username, salt, password, access_control):
    with DbTransaction() as conn:
        conn.execute('insert into users values (?,?,?,?,?);',
                     (user_id, username, salt, password, access_control))

def insert_role(role_id, role_name, access_control):
    with DbTransaction() as conn:
        conn.execute('insert into roles '
                     'values (?,?,?);',
                     (role_id, role_name, access_control))

def insert_role_assignment(user_id, role_id):
    with DbTransaction() as conn:
        conn.execute('insert into role_assignments '
                     '(user_id, role_id) '
                     'values (?,?);',
                     (user_id, role_id))

def insert_session(session_id, user_id, created_at, expires_at):
    with DbTransaction() as conn:
        conn.execute('insert into sessions '
                     'values (?,?,?,?);',
                     (session_id, user_id, created_at, expires_at))

def insert_rci_document(rci_document_id, user_id, access_control):
    with DbTransaction() as conn:
        conn.execute('insert into rci_documents '
                     'values (?,?,?);',
                     (rci_document_id, user_id, access_control))

def insert_user_acl_owner(user_id, acl_owner_id):
    with DbTransaction() as conn:
        conn.execute('insert into user_acl_owners '
                     '(user_id, acl_owner_id) '
                     'values (?,?);',
                     (user_id, acl_owner_id))

def insert_user_acl_group(user_id, acl_group_id):
    with DbTransaction() as conn:
        conn.execute('insert into user_acl_groups '
                    '(user_id, acl_group_id) '
                    'values (?,?);',
                    (user_id, acl_group_id))


def insert_role_acl_owner(role_id, acl_owner_id):
    with DbTransaction() as conn:
        conn.execute('insert into role_acl_owners '
                     '(role_id, acl_owner_id) '
                     'values (?,?);',
                     (role_id, acl_owner_id))

def insert_role_acl_group(role_id, acl_group_id):
    with DbTransaction() as conn:
        conn.execute('insert into role_acl_groups '
                    '(role_id, acl_group_id) '
                    'values (?,?);',
                    (role_id, acl_group_id))

def insert_rci_document_acl_owner(rci_document_id, acl_owner_id):
    with DbTransaction() as conn:
        conn.execute('insert into rci_document_acl_owners '
                     '(rci_document_id, acl_owner_id) '
                     'values (?,?);',
                     (rci_document_id, acl_owner_id))

def inser_rci_document_acl_group(rci_document_id, acl_group_id):
    with DbTransaction() as conn:
        conn.exeute('insert into rci_document_acl_groups '
                    '(rci_document_id , acl_group_id) '
                    'values (?,?);',
                    (rci_document_id, acl_group_id))

def insert_event_log():
    pass


# Simple 1-record SELECT methods 
# NAMING CONVENTION `def select_{singularized_table_name}`

select_stmt = ('select *'
               'from {0}'
               'where {1} = ?'
               'limit 1')

def select_user(user_id):
    with DbTransaction() as conn:
        conn.execute(select_stmt.format('users', 'user_id'),
                     (user_id,))

def select_role(role_id):
    with DbTransaction() as conn:
        conn.execute(select_stmt.format('roles', 'role_id'),
                     (role_id,))

def select_session(session_id):
    with DbTransaction() as conn:
        conn.execute(select_stmt.format('sessions', 'session_id'),
                     (session_id,))

def select_rci_document(rci_document_id):
    with DbTransaction() as conn:
        conn.execute(select_stmt.format('rci_documents', 'rci_document_id'),
                     (rci_document_id,))

def select_event_log():
    pass


# Sqlite's Row factory works well, however, I REALLY
# want to return my records as plain dictionaries.
# Makes it easier to handle in any modules that use 
# this module.
# See https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

