from graphql import GraphQLError

USER_ROLES_NAMES = {
    'SUPER_ADMIN': 'Super Admin',
    'INSTITUTION_ADMIN': 'Institution Admin',
    'CLASS_ADMIN': 'Class Admin',
    'LEARNER': 'Learner',
}

RESOURCES = {
    'MODERATION': 'MODERATION',
    'USER_ROLE': 'USER_ROLE',
    'MEMBER': 'MEMBER',
    'INSTITUTION_ADMIN': 'INSTITUTION_ADMIN',
    'CLASS_ADMIN': 'CLASS_ADMIN',
    'LEARNER': 'LEARNER',
    'INSTITUTION': 'INSTITUTION',
    'ANNOUNCEMENT': 'ANNOUNCEMENT',
    'ASSIGNMENT': 'ASSIGNMENT',
    'COURSE': 'COURSE',
    'GROUP': 'GROUP',
    'REPORT': 'REPORT',
    'OWN_PROFILE': 'OWN_PROFILE',
}

ACTIONS = {
    'LIST': 'LIST',
    'GET': 'GET',
    'CREATE': 'CREATE',
    'UPDATE': 'UPDATE',
    'DELETE': 'DELETE',
}


def has_access(user=None, resource=None, action=None):
    print('From has_access', user, resource, action)
    result = False
    if user:
        user_permissions = user.role.permissions
        if user_permissions and resource is not None and action is not None:
            result = user_permissions[resource][action]

    if result is True:
        return result

    # raise GraphQLError('You are not authorized for this resource')
    return False
