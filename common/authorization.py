from graphql import GraphQLError
from django.conf import settings

# whever changes are made below to the User role names, Resources and actions
# need to be reflected in the UI too.

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
    'PROJECT': 'PROJECT',
    'ISSUE': 'ISSUE',
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

def is_admin_user(info):
    current_user = info.context.user
    admin_user = False

    try:
        if not current_user.is_anonymous:
            current_user_role_name = current_user.role.name
            admin_user = current_user_role_name == USER_ROLES_NAMES["SUPER_ADMIN"]
    except:
        admin_user = False
        pass

    return admin_user
def redact_user(root, info, user):
    current_user = info.context.user
    redact = True

    if not current_user.is_anonymous:
        admin_user = is_admin_user(info)
        if admin_user:
            redact = False # We never redact for the super admin user
        if current_user.institution:
            if user.institution_id == current_user.institution.id:
                redact = False # We redact the user's info if the current user is not of the same institution
            
    if redact == True:
        user.avatar = settings.DEFAULT_AVATARS['USER']

    return user

