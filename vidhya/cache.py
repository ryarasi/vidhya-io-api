
from tkinter import N
from django.core.cache import cache

separator = '-'
limit_label = 'limit'
offset_label = 'offset'
searchField_label = 'searchField'
status_label = 'status'

CACHE_ENTITIES = {
    'INSTITUTIONS': 'INSTITUTION',
    'PUBLIC_INSTITUTIONS': 'PUBLIC_INSTITUTION',
    'USERS': 'USERS',
    'PUBLIC_USERS': 'PUBLIC_USERS',
    'USER_ROLES': 'USER_ROLES',
    'GROUPS': 'GROUPS',
    'ADMIN_GROUPS': 'ADMIN_GROUPS',
    'ANNOUNCEMENTS': 'ANNOUNCEMENTS',
    'PUBLIC_ANNOUNCEMENTS': 'PUBLIC_ANNOUNCEMENTS',
    'PROJECTS': 'PROJECTS',
    'COURSES': 'COURSES',
    'CHAPTERS': 'CHAPTERS',
    'EXERCISES': 'EXERCISES',
    'EXERCISE_KEYS': 'EXERCISE_KEYS',
    'EXERCISE_SUBMISSIONS': 'EXERCISE_SUBMISSIONS',
    'SUBMISSION_GROUPS': 'SUBMISSION_GROUPS',
    'ASSIGNMENTS': 'ASSIGNMENTS',
    'REPORTS': 'REPORTS'
}


def sanitize_cache_key(key):
    return key.replace(" ", separator)

def generate_public_institutions_cache_key(entity, searchField, limit, offset):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_institutions_cache_key(entity, searchField, limit, offset):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_users_cache_key(entity=None, searchField=None, all_institutions=None, membership_status_not=None, membership_status_is=None, roles=None, unpaginated=None, limit=None, offset=None):
    membership_status_not_str = ''.join(map(str, membership_status_not))
    membership_status_is_str = ''.join(map(str, membership_status_is))
    roles_str = ''.join(map(str, roles))
    cache_key =  str(entity) + separator + searchField_label + str(searchField) + 'all_institutions' + str(all_institutions) + 'membership_status_not' + str(membership_status_not_str) + 'membership_status_is' + str(membership_status_is_str) + 'roles' + str(roles_str) + 'unpaginated' + str(unpaginated) + limit_label + str(limit) + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_public_users_cache_key(entity, searchField=None, membership_status_not=None, membership_status_is=None, roles=None, limit=None, offset=None):
    cache_key =  str(entity) + separator + searchField_label + str(searchField) +  'membership_status_not' + str(membership_status_not) + 'membership_status_is' + str(membership_status_is) + 'roles' + str(roles) + limit_label + str(limit) + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_user_roles_cache_key(entity, searchField, limit, offset):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_groups_cache_key(entity, searchField,limit,offset,current_user):
    cache_key = str(current_user.id) + separator + str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_admin_groups_cache_key(entity, searchField, limit, offset, current_user):
    cache_key = str(current_user.id) + separator + str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_announcements_cache_key(entity, searchField, limit, offset, current_user):
    cache_key = str(current_user.id) + separator + str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)    

def generate_public_announcements_cache_key(entity, searchField,limit,offset):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_projects_cache_key(entity, searchField=None, limit=None, offset=None, author_id=None, user=None):
    cache_key = str(user.id) + str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'author_id' + str(author_id)
    return sanitize_cache_key(cache_key)

def generate_courses_cache_key(entity, searchField=None, limit=None, offset=None, user=None):
    cache_key = str(user.id) + str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset)
    return sanitize_cache_key(cache_key)

def generate_chapters_cache_key(entity, searchField, limit, offset, course_id, current_user):
    cache_key = str(current_user.id) + str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'course_id' + str(course_id)
    return sanitize_cache_key(cache_key)

def generate_exercises_cache_key(entity, searchField=None, limit=None, offset=None, chapter_id=None, user=None):
    cache_key = str(user.id) + str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'chapter_id' + str(chapter_id)
    return sanitize_cache_key(cache_key)

def generate_exercise_keys_cache_key(entity, searchField=None, limit=None, offset=None, exercise_id=None, chapter_id=None, course_id=None):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'exercise_id' + str(exercise_id) + 'chapter_id' + str(chapter_id) + 'course_id' + str(course_id)
    return sanitize_cache_key(cache_key)    

def generate_submissions_cache_key(entity, searchField=None, limit=None, offset=None, exercise_id=None, chapter_id=None, course_id=None, participant_id=None, submission_id=None, status=None, flagged=None):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'exercise_id' + str(exercise_id) + 'chapter_id' + str(chapter_id) + 'course_id' + str(course_id) + 'participant_id' + str(participant_id) + 'submission_id' + str(submission_id) + status_label + str(status) + 'flagged' + str(flagged)
    return sanitize_cache_key(cache_key)    

def generate_submission_groups_cache_key(entity, searchField=None, limit=None, offset=None, group_by=None, status=None, flagged=None, cutoff_date=None):
    cache_key = str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'group_by' + str(group_by) + status_label + str(status) + 'flagged' + str(flagged) + 'cutoff_date'+ str(cutoff_date)
    return sanitize_cache_key(cache_key)

def generate_assignments_cache_key(entity, limit, offset, status, current_user):
    cache_key = str(current_user.id) + str(entity) + separator + limit_label + str(limit) + offset_label + str(offset) + status_label + str(status)
    return sanitize_cache_key(cache_key) 

def generate_reports_cache_key(entity, searchField=None, limit=None, offset=None, participant_id=None, course_id=None, institution_id=None, user=None):
    cache_key = str(user.id) + str(entity) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'participant_id' + str(participant_id) + 'course_id' + str(course_id) + 'institution_id' + str(institution_id)
    return sanitize_cache_key(cache_key)


def fetch_cache(entity, key):
    print('Fetching cache => ', entity, ' key => ', key)
    cached_response = None
    cached_item = cache.get(entity)
    if cached_item:
        try:
            cached_response = cached_item[key]
        except:
            pass
    print('cached response => ', cached_response)
    return cached_response

# Set cache method

def set_cache(entity, key, response):
    print('Setting cache => ', entity, 'key => ', key, ' response => ', response)
    cached_entity = cache.get(entity)
    if not cached_entity:
        cached_entity = {}
    cached_entity[key] = response
    cache.set(entity, cached_entity, timeout=None)


# Cache Invalidation Methods

def invalidate_cache(entity):
    cache.delete(entity)

def invalidate_cache_with_keyword(entity, keyword):
    cached_entity = cache.get(entity)
    for item in cached_entity.keys():
        if keyword in item:
            del cached_entity[item]
    cache.set(entity, cached_entity)

def invalidate_user_specific_cache(entity, user):
    cached_entity = cache.get(entity)
    for item in cached_entity.keys():
        if item.startswith(str(user.id)):
            del cached_entity[item]
    cache.set(entity, cached_entity)


# Specific methods to invalidate certain entities

def institutions_modified():
    invalidate_cache(CACHE_ENTITIES['INSTITUTIONS'])
    invalidate_cache(CACHE_ENTITIES['PUBLIC_INSTITUTIONS'])

def users_modified():
    invalidate_cache(CACHE_ENTITIES['USERS'])
    invalidate_cache(CACHE_ENTITIES['PUBLIC_USERS'])

def user_roles_modified():
    invalidate_cache(CACHE_ENTITIES['USER_ROLES'])

def groups_modified():
    invalidate_cache(CACHE_ENTITIES['GROUPS'])
    invalidate_cache(CACHE_ENTITIES['ADMIN_GROUPS'])

def public_announcements_modified():
    invalidate_cache(CACHE_ENTITIES['PUBLIC_ANNOUNCEMENTS'])

def private_announcements_modified():
    invalidate_cache(CACHE_ENTITIES['ANNOUNCEMENTS'])

def announcements_modified(announcement):
    if announcement.public == True:
        public_announcements_modified()
    else:
        private_announcements_modified()

def user_announcements_modified(user):
    invalidate_user_specific_cache(CACHE_ENTITIES['ANNOUNCEMENTS'], user)

def projects_modified():
    invalidate_cache(CACHE_ENTITIES['PROJECTS'])

def courses_modified():
    invalidate_cache(CACHE_ENTITIES['COURSES'])

def chapters_modified():
    invalidate_cache(CACHE_ENTITIES['CHAPTERS'])

def exercises_modified():
    invalidate_cache(CACHE_ENTITIES['EXERCISES'])

def exercise_submission_submitted():
    invalidate_cache(CACHE_ENTITIES['EXERCISE_SUBMISSIONS'])
    invalidate_cache(CACHE_ENTITIES['ASSIGNMENTS'])
    invalidate_cache(CACHE_ENTITIES['REPORTS'])

def exercise_submission_graded():
    invalidate_cache(CACHE_ENTITIES['EXERCISE_SUBMISSIONS'])
    invalidate_cache(CACHE_ENTITIES['ASSIGNMENTS'])
    invalidate_cache(CACHE_ENTITIES['PUBLIC_USERS'])
    invalidate_cache(CACHE_ENTITIES['REPORTS'])    