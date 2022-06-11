
from django.core.cache import cache

separator = '-'
limit_label = 'limit'
offset_label = 'offset'
searchField_label = 'searchField'
status_label = 'status'


def generate_public_institutions_cache_key(searchField, limit, offset):
    item = 'public_institutions'
    cache_key = str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key

def generate_institutions_cache_key(searchField, limit, offset):
    item = 'institutions'
    cache_key = str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key

def generate_groups_cache_key(searchField,limit,offset,current_user):
    item = 'groups'
    cache_key = str(current_user.id) + separator + str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key

def generate_admin_groups_cache_key(searchField, limit, offset, current_user):
    item = 'admin_groups'
    cache_key = str(current_user.id) + separator + str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key

def generate_announcements_cache_key(searchField, limit, offset, current_user):
    item='announcements'
    cache_key = str(current_user.id) + separator + str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key    

def generate_public_announcements_cache_key(searchField,limit,offset):
    item = 'public_announcements'
    cache_key = str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key

def generate_user_roles_cache_key(searchField, limit, offset):
    item = 'user_roles'
    cache_key = str(item) + separator + searchField_label + str(searchField) + separator + limit_label + str(limit) + separator + offset_label + str(offset)
    return cache_key

def generate_users_cache_key(item=None, searchField=None, all_institutions=None, membership_status_not=None, membership_status_is=None, roles=None, unpaginated=None, limit=None, offset=None):
    cache_key =  str(item) + separator + searchField_label + str(searchField) + 'all_institutions' + str(all_institutions) + 'membership_status_not' + str(membership_status_not) + 'membership_status_is' + str(membership_status_is) + 'roles' + str(roles) + 'unpaginated' + str(unpaginated) + limit_label + str(limit) + offset_label + str(offset)
    return cache_key

def generate_projects_cache_key(item=None, searchField=None, limit=None, offset=None, author_id=None, user=None):
    cache_key = str(user.id) + str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'author_id' + str(author_id)
    return cache_key

def generate_courses_cache_key(item=None, searchField=None, limit=None, offset=None, course_id=None, user=None):
    cache_key = str(user.id) + str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'course_id' + str(course_id)
    return cache_key

def generate_courses_cache_key(searchField, limit, offset, current_user):
    item = 'courses'
    cache_key = str(current_user.id) + str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset)
    return cache_key

def generate_chapters_cache_key(searchField, limit, offset, course_id, current_user):
    item = 'chapters'
    cache_key = str(current_user.id) + str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'course_id' + str(course_id)
    return cache_key

def generate_assignments_cache_key(limit, offset, status, current_user):
    item = 'assignments'
    cache_key = str(current_user.id) + str(item) + separator + limit_label + str(limit) + offset_label + str(offset) + status_label + str(status)
    return cache_key 

def generate_exercises_cache_key(item=None, searchField=None, limit=None, offset=None, chapter_id=None, user=None):
    cache_key = str(user.id) + str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'chapter_id' + str(chapter_id)
    return cache_key

def generate_submissions_cache_key(item=None, searchField=None, limit=None, offset=None, exercise_id=None, chapter_id=None, course_id=None, participant_id=None, submission_id=None, status=None, flagged=None):
    cache_key = str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'exercise_id' + str(exercise_id) + 'chapter_id' + str(chapter_id) + 'course_id' + str(course_id) + 'participant_id' + str(participant_id) + 'submission_id' + str(submission_id) + status_label + str(status) + 'flagged' + str(flagged)
    return cache_key

def generate_exercise_keys_cache_key(item=None, searchField=None, limit=None, offset=None, exercise_id=None, chapter_id=None, course_id=None):
    cache_key = str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'exercise_id' + str(exercise_id) + 'chapter_id' + str(chapter_id) + 'course_id' + str(course_id)
    return cache_key    

def generate_submission_groups_cache_key(item=None, searchField=None, limit=None, offset=None, group_by=None, status=None, flagged=None):
    cache_key = str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'group_by' + str(group_by) + status_label + str(status) + 'flagged' + str(flagged)
    return cache_key

def generate_reports_cache_key(item=None, searchField=None, limit=None, offset=None, participant_id=None, course_id=None, institution_id=None, user=None):
    cache_key = str(user.id) + str(item) + separator + searchField_label + str(searchField) + limit_label + str(limit) + offset_label + str(offset) + 'participant_id' + str(participant_id) + 'course_id' + str(course_id) + 'institution_id' + str(institution_id)
    return cache_key

def invalidate_cache(key):
    if key:
        pattern = '*' + str(key) + '*'
        cache.delete_many(keys=cache.keys(pattern))

def invalidate_users_cache(user, key):
    if user and key:
        pattern = str(user.id)  +  '*' + str(key) + '*'
        cache.delete_many(keys=cache.keys(pattern))