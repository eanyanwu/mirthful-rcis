import rci_datastore as db

import uuid

# Execute the reset_db.sql script to create the tables
sql = ''

with open('./sql/reset_db.sql', 'r') as f:
    sql = f.read()

db.execute_script(sql)


# Create Test Data

users = [
    {
        'user_id': str(uuid.uuid4()),
        'username': 'ava',
        'salt': '1',
        'password': 'password',
        'access_control': 'o:r_;g:rw;w__'
    },
    {
        'user_id': str(uuid.uuid4()),
        'username': 'geraint',
        'salt': '1',
        'password': 'password',
        'access_control': 'o:r_;g:rw;w__'
    },
    {
        'user_id': str(uuid.uuid4()),
        'username': 'jeremias',
        'salt': '1',
        'password': 'password',
        'access_control': 'o:r_;g:rw;w__'
    }
]

roles = [
    {
        'role_id': str(uuid.uuid4()),
        'role_name': 'student',
        'access_control': 'o:rw;g:rw;w__'
    },
    {
        'role_id': str(uuid.uuid4()),
        'role_name': 'staff',
        'access_control': 'o:rw;g:rw;w__'
    },
    {
        'role_id': str(uuid.uuid4()),
        'role_name': 'admin',
        'access_control': 'o:rw;g:rw;w__'
    }
]

role_assignments = [
    {
        'user_id': users[0]['user_id'],
        'role_id': roles[0]['role_id']
    },
    {
        'user_id': users[1]['user_id'],
        'role_id': roles[1]['role_id']
    },
    {
        'user_id': users[2]['user_id'],
        'role_id': roles[2]['role_id']
    }
]

user_acl_owners = [
    {
        'user_id': users[0]['user_id'],
        'acl_owner_id': users[0]['user_id'],
    },
    {
        'user_id': users[1]['user_id'],
        'acl_owner_id': users[1]['user_id'],
    },
    {
        'user_id': users[2]['user_id'],
        'acl_owner_id': users[2]['user_id'],
    }
]

user_acl_groups = [
    {
        'user_id': users[0]['user_id'],
        'acl_group_id': roles[2]['role_id']
    },
    {
        'user_id': users[1]['user_id'],
        'acl_group_id': roles[2]['role_id']
    },
    {
        'user_id': users[2]['user_id'],
        'acl_group_id': roles[2]['role_id']
    }
]

role_acl_owners = [
    {
        'role_id': roles[0]['role_id'],
        'acl_owner_id': users[2]['user_id']
    },
    {
        'role_id': roles[1]['role_id'],
        'acl_owner_id': users[2]['user_id']
    },
    {
        'role_id': roles[2]['role_id'],
        'acl_owner_id': users[2]['user_id']
    }
]

role_acl_groups = [
    {
        'role_id': roles[0]['role_id'],
        'acl_group_id': roles[2]['role_id'],
    },
    {
        'role_id': roles[1]['role_id'],
        'acl_group_id': roles[2]['role_id'],
    },
    {
        'role_id': roles[2]['role_id'],
        'acl_group_id': roles[2]['role_id'],
    }
]

# Insert the records
for user in users:
    db.insert_user(**user)

for role in roles:
    db.insert_role(**role)

for role_assignment in role_assignments:
    db.insert_role_assignment(**role_assignment)

for uao in user_acl_owners:
    db.insert_user_acl_owner(**uao)

for uag in user_acl_groups:
    db.insert_user_acl_group(**uag)

for rao in role_acl_owners:
    db.insert_role_acl_owner(**rao)

for rag in role_acl_groups:
    db.insert_role_acl_group(**rag)

