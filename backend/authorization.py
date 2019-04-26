from custom_exceptions import Unauthorized

# This should always remain a 'pure' function, devoid of side-effects -- no
# network calls, no database calls, no outside method calls
# Keeping it this way allows for easy-to-write tests

def authorize(mode,
              acs,
              user_id,
              user_roles,
              resource_acl_owners,
              resource_acl_groups):
    """
    Determine if a user can access a certain resource.

    This method does not return any value if the authorization is succcessful.
    If the authorization fails, `Unauthorized` is raised
    """

    # Validate and throw
    if user_id is None:
        raise ValueError('user_id is None')

    valid_modes = ['r', 'w', 'rw']

    if mode not in valid_modes:
        raise ValueError('mode {} is not valid'.format(mode))

    if user_roles is None:
        user_roles = []

    if resource_acl_owners is None:
        resource_acl_owners = []

    if resource_acl_groups is None:
        resource_acl_groups = []


    # Resource has no access_control -> No access
    if acs is None:
        raise Unauthorized('resource is not publicly accessible.')

    # 'ac' menas access control
    ac = parse_access_control(acs)

    # If the world can access the resource in the mode you seek, go ahead
    if ac['world'][mode]:
        return

    # If you belong to one of the roles/groups associated with the resource AND
    # groups can access the resource in the mode you seek, then go ahead
    if (not set(user_roles).isdisjoint(resource_acl_groups) and
            ac['group'][mode]): 
        return

    # If you are one of the owners AND owners can access the resource in the
    # mode you seek, then go ahead.
    if (not { user_id }.isdisjoint(resource_acl_owners) and
            ac['owner'][mode]):
        return

    # If none of the above requirements have been satisfied, you don't have
    # access :/
    raise Unauthorized('you do not have sufficient permissions')


def parse_access_control(acs):
    """
    Parse the access control string into a dictionary
    for easy of use

    acs : Access Control String. Should be in the form:
    `o:##;g:##;w:##'

    where # is a placeholder for 'r', 'w' and '_'
    and the abbreviations are as follows:
    o : owner
    g : group
    a : all
    """

    try:
        owner_section, group_section, world_section = acs.split(';')

        owner, owner_access = owner_section.split(':')
        group, group_access = group_section.split(':') 
        world, world_access = world_section.split(':')

        if owner != 'o' or group != 'g' or world != 'w':
            raise ValueError

        owner_read, owner_write = owner_access
        group_read, group_write = group_access
        world_read, world_write = world_access

        owner_permission = []
        group_permissions = []
        world_permissions = []

        return {
            'owner': {
                'r': owner_read == 'r',
                'w': owner_write == 'w',
                'rw': owner_read == 'r' and owner_write == 'w'
            },
            'group': {
                'r': group_read == 'r',
                'w': group_write == 'w',
                'rw': group_read == 'r' and group_write == 'w'
            },
            'world': {
                'r': world_read == 'r',
                'w': world_write == 'w',
                'rw': world_read == 'r' and world_write == 'w'
            }
        }
    except:
        raise ValueError('Invalid access control {}'.format(acs))

