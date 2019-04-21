from authorization import parse_access_control
from authorization import authorize
from authorization import AuthorizationError

import pytest
import uuid

# Authorize tests 

def test_authorize_user_id_is_none():
    with pytest.raises(ValueError):
        authorize(mode='r',
                  acs='o:rw;g:rw;a:rw',
                  user_id=None,
                  user_roles=[],
                  resource_acl_owners=[],
                  resource_acl_groups=[])

def test_authorize_mode_is_none():
    with pytest.raises(ValueError):
        authorize(mode='invalid mode',
                  acs='o:rw;g:rw;a:rw',
                  user_id=str(uuid.uuid4()),
                  user_roles=[],
                  resource_acl_owners=[],
                  resource_acl_groups=[])

def test_authorize_acs_is_none():
    with pytest.raises(AuthorizationError, match='not publicly accessible'):
        authorize(mode='r',
                  acs=None,
                  user_id=str(uuid.uuid4()),
                  user_roles=[],
                  resource_acl_owners=[],
                  resource_acl_groups=[])

# Remember that the authorize function doesn't retun anything.
# If anything goes wrong, an exception is thrown.
# If you are indeed authorized, you can go on your merry way
def test_authorize_success_mode_r_world_can_read():
    authorize(mode='r',
              acs='o:__;g:__;w:r_',
              user_id=str(uuid.uuid4()),
              user_roles=[],
              resource_acl_owners=[],
              resource_acl_groups=[])

def test_authorize_success_mode_w_world_can_write():
    authorize(mode='w',
              acs='o:__;g:__;w:_w',
              user_id=str(uuid.uuid4()),
              user_roles=[],
              resource_acl_owners=[],
              resource_acl_groups=[])

def test_authorize_success_mode_rw_world_can_read_and_write():
    authorize(mode='rw',
              acs='o:__;g:__;w:rw',
              user_id=str(uuid.uuid4()),
              user_roles=[],
              resource_acl_owners=[],
              resource_acl_groups=[])

def test_authorize_failure_mode_r_world_can_only_write():
    with pytest.raises(AuthorizationError, match='sufficient permissions'):
        authorize(mode='r',
                  acs='o:rw;g:rw;w:__',
                  user_id=str(uuid.uuid4()),
                  user_roles=[],
                  resource_acl_owners=[],
                  resource_acl_groups=[])

def test_authorize_success_mode_r_group_can_read():
    authorize(mode='r',
              acs='o:__;g:r_;w:__',
              user_id=str(uuid.uuid4()),
              user_roles=[ 'staff' ],
              resource_acl_owners=[],
              resource_acl_groups=[ 'staff' , 'student' ])


def test_authorize_mode_w_group_can_write():
    authorize(mode='w',
              acs='o:__;g:_w;w:__',
              user_id=str(uuid.uuid4()),
              user_roles=[ 'staff' ],
              resource_acl_owners=[],
              resource_acl_groups=[ 'staff' ])

def test_authorize_mode_rw_group_can_read_and_write():
    authorize(mode='rw',
              acs='o:__;g:rw;w:__',
              user_id=str(uuid.uuid4()),
              user_roles=['staff'],
              resource_acl_owners=[],
              resource_acl_groups=['staff'])


def test_authorize_mode_rw_group_can_only_read():
    with pytest.raises(AuthorizationError, match='sufficient permission'):
        authorize(mode='rw',
                  acs='o:__;g:r_;w:__',
                  user_id=str(uuid.uuid4()),
                  user_roles=['staff'],
                  resource_acl_owners=[],
                  resource_acl_groups=['staff'])

def test_authorize_mode_r_group_can_read_but_user_not_in_right_group():
    with pytest.raises(AuthorizationError, match='sufficient permission'):
        authorize(mode='r',
                  acs='o:__;g:r_;w:__',
                  user_id=str(uuid.uuid4()),
                  user_roles=['student'],
                  resource_acl_owners=[],
                  resource_acl_groups=['staff'])

def test_authorize_mode_r_owner_can_read():
    user_id = str(uuid.uuid4())

    authorize(mode='r',
              acs='o:r_;g:__;w:__',
              user_id=user_id,
              user_roles=[],
              resource_acl_owners=[user_id],
              resource_acl_groups=[])

def test_authorize_mode_w_owner_can_write():
    user_id = str(uuid.uuid4())

    authorize(mode='w',
              acs='o:_w;g:__;w:__',
              user_id=user_id,
              user_roles=[],
              resource_acl_owners=[user_id],
              resource_acl_groups=[])

def test_authorize_mode_rw_owner_can_read_and_write():
    user_id = str(uuid.uuid4())

    authorize(mode='rw',
              acs='o:rw;g:__;w:__',
              user_id=user_id,
              user_roles=[],
              resource_acl_owners=[user_id],
              resource_acl_groups=[])


def test_authorize_mode_r_owner_can_only_write():
    user_id = str(uuid.uuid4())
    
    with pytest.raises(AuthorizationError, match='sufficient permissions'):
        authorize(mode='r',
                  acs='o:_w;g:__;w:__',
                  user_id=user_id,
                  user_roles=[],
                  resource_acl_owners=[user_id],
                  resource_acl_groups=[])

def test_authorize_mode_r_owner_can_read_but_user_not_part_of_user_list():
    user_id = str(uuid.uuid4())
    
    with pytest.raises(AuthorizationError, match='sufficient permissions'):
        authorize(mode='r',
                  acs='o:rw;g:__;w:__',
                  user_id=user_id,
                  user_roles=[],
                  resource_acl_owners=[str(uuid.uuid4())],
                  resource_acl_groups=[])

# Parse Access Control Tests

def test_parse_access_control_list_invalid_strings():
    test_cases = [
        None,
        '',                 # Empty String
        'o;g;w',            # No access strings
        'o:r;g:r;w:r',      # Missing access strings
        'g:rw;o:rw;w:wr'    # Out of order string
    ]

    for test_case in test_cases:
        with pytest.raises(ValueError, match='Invalid access control'):
            parse_access_control(test_case)


def test_parse_access_control_list_success_no_permissions():
    acs = 'o:__;g:__;w:__'
    result = parse_access_control(acs)

    assert result['owner']['r'] == False
    assert result['group']['r'] == False
    assert result['world']['r'] == False

    assert result['owner']['w'] == False
    assert result['group']['w'] == False
    assert result['world']['w'] == False

def test_parse_access_control_list_success_some_permissions():
    acs = 'o:r_;g:rw;w:_w'
    result = parse_access_control(acs)

    assert result['owner']['r'] == True 
    assert result['group']['r'] == True 
    assert result['world']['r'] == False

    assert result['owner']['w'] == False
    assert result['group']['w'] == True 
    assert result['world']['w'] == True 

def test_parse_access_control_list_success_full_permissions():
    acs = 'o:rw;g:rw;w:rw'
    result = parse_access_control(acs)

    assert result['owner']['r'] == True
    assert result['group']['r'] == True
    assert result['world']['r'] == True

    assert result['owner']['w'] == True
    assert result['group']['w'] == True 
    assert result['world']['w'] == True 


