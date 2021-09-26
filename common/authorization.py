from graphql import GraphQLError

USER_ROLES_NAMES = {
    'SUPER_ADMIN': 'Super Admin',
    'INSTITUTION_ADMIN': 'Institution Admin',
    'CLASS_ADMIN': 'Class Admin',
    'LEARNER': 'Learner',
    'CLASS_ADMIN_LEARNER': 'Class Admin Learner',
    'GRADER': 'Grader'
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
    'CHAPTER': 'CHAPTER',
    'COURSE': 'COURSE',
    'GROUP': 'GROUP',
    'EXERCISE_KEY': 'EXERCISE_KEY',
    'EXERCISE_SUBMISSION': 'EXERCISE_SUBMISSION',
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


def has_access(user=None, resource=None, action=None, silent=True):
    result = False
    if user:
        user_permissions = user.role.permissions
        if user_permissions and resource and action:
            result = user_permissions[resource][action]

    if result is False and silent is False:
        raise GraphQLError('You are not authorized to access this resource')
    return result
