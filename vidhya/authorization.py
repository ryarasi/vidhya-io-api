from django.db.models.query_utils import Q
from graphql import GraphQLError
from django.conf import settings
from vidhya.models import CompletedChapters, CompletedCourses, CriterionResponse, MandatoryChapters, MandatoryRequiredCourses, User, Announcement, Chapter, Chat, ChatMessage, Course, CourseSection, Exercise, ExerciseKey, ExerciseSubmission, Group, Institution, Issue, Project, Report, UserRole

SORT_BY_OPTIONS = {'NEW': 'NEW', 'TOP':'TOP'}

UPDATE_METHOD = "UPDATE"
DELETE_METHOD = "DELETE"
CREATE_METHOD = "CREATE"
# whever changes are made below to the User role names, Resources and actions
# need to be reflected in the UI too.

USER_ROLES_NAMES = {
    "SUPER_ADMIN": "Super Admin",
    "INSTITUTION_ADMIN": "Institution Admin",
    "CLASS_ADMIN": "Class Admin",
    "LEARNER": "Learner",
    "CLASS_ADMIN_LEARNER": "Class Admin Learner",
    "GRADER": "Grader"
}


RESOURCES = {
    "MODERATION": "MODERATION",
    "USER_ROLE": "USER_ROLE",
    "MEMBER": "MEMBER",
    "INSTITUTION_ADMIN": "INSTITUTION_ADMIN",
    "CLASS_ADMIN": "CLASS_ADMIN",
    "LEARNER": "LEARNER",
    "INSTITUTION": "INSTITUTION",
    "ANNOUNCEMENT": "ANNOUNCEMENT",
    "CHAPTER": "CHAPTER", # Also handles permissions for Exercise, Criterion
    "COURSE": "COURSE",  # Also handles permissions for Course Sections
    "MEMBER_COURSE": "MEMBER_COURSE",
    "GROUP": "GROUP",
    "EXERCISE_KEY": "EXERCISE_KEY",
    "EXERCISE_SUBMISSION": "EXERCISE_SUBMISSION",
    "REPORT": "REPORT",
    "PROJECT": "PROJECT",
    "ISSUE": "ISSUE",
    "OWN_PROFILE": "OWN_PROFILE",
    "CHAT": "CHAT",
    "EXERCISE": "EXERCISE", # API ONLY, this resource type is defined for use only in the API. May not be found in the UI list of resources
    "CHAT_MESSAGE": "CHAT_MESSAGE", # API ONLY, this resource type is defined for use only in the API. May not be found in the UI list of resources
    "CRITERION":"CRITERION", # API ONLY, this resource type is defined for use only in the API. May not be found in the UI list of resources
    "CRITERION_RESPONSE": "CRITERION_RESPONSE", # API ONLY, this resource type is defined for use only in the API. May not be found in the UI list of resources
    "COURSE_SECTION": "COURSE_SECTION" # API ONLY, this resource type is defined for use only in the API. May not be found in the UI list of resources
}

ACTIONS = {
    "LIST": "LIST",
    "GET": "GET",
    "CREATE": "CREATE",
    "UPDATE": "UPDATE",
    "DELETE": "DELETE",
}


def has_access(user=None, resource=None, action=None, silent=True):
    result = False
    if user:
        user_permissions = user.role.permissions
        if user_permissions and resource and action:
            result = user_permissions[resource][action]

    if result is False and silent is False:
        raise GraphQLError("You are not authorized to access this resource")
    return result

def is_admin_user(user):
    admin_user = False

    try:
        if not user.is_anonymous:
            current_user_role_name = user.role.name
            admin_user = current_user_role_name == USER_ROLES_NAMES["SUPER_ADMIN"]
    except:
        admin_user = False
        pass

    return admin_user

def redact_user(root, info, user):
    current_user = info.context.user
    redact = True

    if not current_user.is_anonymous:
        admin_user = is_admin_user(current_user)
        if admin_user:
            redact = False # We never redact for the super admin user
        if current_user.institution:
            if user.institution_id == current_user.institution.id:
                redact = False # We redact the user"s info if the current user is not of the same institution
            
    if redact == True:
        user.avatar = settings.DEFAULT_AVATARS["USER"]

    return user

def is_course_locked(user, course):
    locked = True
   # objects.filter(email=input.email).exists()
    # Checking if the user is the author of the course
    instructor_ids = course.instructors.values_list('id',flat=True)
    if instructor_ids== user.id:
        # If yes, we mark it as unlocked
        locked = False
        return locked        
    completed_courses = CompletedCourses.objects.all().filter(participant_id=user.id)
    required_courses = MandatoryRequiredCourses.objects.all().filter(course_id=course.id)
    required_course_ids = required_courses.values_list('requirement_id',flat=True)
    completed_course_ids = completed_courses.values_list('course_id',flat=True)

    if required_course_ids:
        # If the course has prerequisites...
        if set(required_course_ids).issubset(set(completed_course_ids)):
            # ...and those prerequisites are met, we mark the course as unlocked
            locked = False
    else:
        # if the course does not have any prerequisites, we mark it as unlocked
        locked = False

    return locked

def is_chapter_locked(user, chapter):
    locked = None

    # Letting the user see it if they are a grader
    user_role = user.role.name;
    grader = user_role == USER_ROLES_NAMES['GRADER']

    # Checking if the user is the author of the course or a grader
    instructor_ids = chapter.course.instructors.values_list('id',flat=True)
    instructor = user.id in instructor_ids

    if grader or instructor:
        # If yes, we mark it as unlocked
        locked = False
        return locked

    course_locked = is_course_locked(user, chapter.course) # Checking if this belongs to a course that is locked
    if course_locked:
        # If the course is locked, we immediately return locked is true
        locked = 'This chapter is locked for you'
        return locked

    # If the course is unlocked we 
    completed_chapters = CompletedChapters.objects.all().filter(participant_id=user.id)
    required_chapters = MandatoryChapters.objects.all().filter(chapter_id=chapter.id)
    required_chapter_ids = required_chapters.values_list('requirement_id',flat=True)
    completed_chapter_ids = completed_chapters.values_list('chapter_id',flat=True)
    pending_chapter_ids = []
    for id in required_chapter_ids:
        if id not in completed_chapter_ids:
            pending_chapter_ids.append(id)
    if pending_chapter_ids:
        locked = 'To view this chapter, you must have completed '
        pending_chapters_list = ''
        for id in pending_chapter_ids:
            try:
                chapter= Chapter.objects.get(pk=id, active=True)
                if pending_chapters_list != '':
                    pending_chapters_list += ', '
                pending_chapters_list += '"' + str(chapter.section.index) +'.'+str(chapter.index)+'. '+chapter.title +'"'
            except:
                pass
        locked += pending_chapters_list
    return locked


def rows_accessible(user, RESOURCE_TYPE, options={}):
    try:
        subscription_method = options['subscription_method']
    except:
        subscription_method = None

    if RESOURCE_TYPE == RESOURCES["MEMBER"]:
        institution_id = None
        try:
            institution_id = user.institution.id
        except:
            pass

        admin_user = is_admin_user(user)
        
        all_institutions = True if options["all_institutions"] == True else False

        if admin_user or all_institutions == True:
            # if the user is super user then they see users from all institutions
            qs = User.objects.all().order_by("-id")
        else:
            # If the user is not a super user, we filter the users by institution
            qs = User.objects.all().filter(institution_id=institution_id).order_by("-id")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["INSTITUTION"]:
        admin_user = is_admin_user(user)

        if admin_user:
            # if the user is super user then they
            qs = Institution.objects.all().order_by("-id")
        else:
            # If the user is not a super user, we filter the users by institution
            qs = Institution.objects.all().filter(pk=user.institution.id).order_by("-id")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs
            
    if RESOURCE_TYPE == RESOURCES["USER_ROLE"]:
        current_user_role = UserRole.objects.all().get(name=user.role)
        current_user_role_priority = current_user_role.priority
        qs = UserRole.objects.all().filter(priority__gte=current_user_role_priority).order_by("-priority")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["ANNOUNCEMENT"]:
        admin = is_admin_user(user)
        if admin:
            qs = Announcement.objects.all().filter(public=False, active=True).order_by("-id")
        else:
            groups = rows_accessible(user, RESOURCES["GROUP"])
            
            qs = Announcement.objects.all().filter(Q(recipients_global=True) | (Q(recipients_institution=True) & Q(institution_id=user.institution_id)) | Q(groups__in=groups), public=False, active=True).order_by("-id")
        
        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["GROUP"]:
        admin_user = is_admin_user(user)
        if admin_user:
            qs = Group.objects.all().order_by("-id")
        else:
            qs = Group.objects.all().filter(
                Q(members__in=[user]) | Q(admins__in=[user])).distinct().order_by("-id")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["PROJECT"]:
        qs = Project.objects.all()
        author_id = None
        try:
            author_id = options["author_id"]
        except:
            pass

        if author_id is not None:
            qs = Project.objects.filter(author_id=author_id)
        if author_id is not user.id:
            qs = qs = qs.filter(public=True)

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["COURSE"]:
        PUBLISHED = Course.StatusChoices.PUBLISHED
        if has_access(user, RESOURCES["COURSE"], ACTIONS["CREATE"]):
            qs = Course.objects.all().filter(
                Q(participants__in=[user]) | Q(instructors__in=[user.id]),status=PUBLISHED).distinct().order_by("-created_at")

        else:
            print('hello2')
            qs = Course.objects.all().filter( status=PUBLISHED).distinct().order_by("-created_at")
            # qs = Course.objects.all().filter(
                # Q(participants__in=[user]) | Q(instructor_id=user.id), status=PUBLISHED).distinct().order_by("index")
        
        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs
    
    if RESOURCE_TYPE == RESOURCES["MEMBER_COURSE"]:
        PUBLISHED = Course.StatusChoices.PUBLISHED
        DRAFT = Course.StatusChoices.DRAFT
        userInstance = User.objects.get(pk=user)  
        admin_user = is_admin_user(userInstance)
        if  admin_user:#if logged user is Super Admin, then fetch all draft courses. Also, fetch published course that are joined or in the try mode
            qs =  Course.objects.filter(Q(status=DRAFT)|Q(courseparticipant__participant=user) & Q(status=PUBLISHED)).distinct()
        else:    #logged user is not Super Admin, then fetch all draft courses which is created by the logged in instructor. Also, fetch published course that are joined or in the try mode
            qs = Course.objects.filter(Q(courseinstructor__instructor=user) & Q(status=DRAFT)|Q(courseparticipant__participant=user) & Q(status=PUBLISHED)).distinct()
        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["CHAPTER"]: 
        course_id = options["course_id"]
        PUBLISHED = Course.StatusChoices.PUBLISHED
        if has_access(user, RESOURCES["CHAPTER"], ACTIONS["CREATE"]):
            qs = Chapter.objects.all().order_by("index")
        else:
            qs = Chapter.objects.all().filter(status=PUBLISHED).order_by("index")

        
        if course_id is not None:
            try:
                course = Course.objects.filter( Q(status=PUBLISHED)| Q(instructors__in=[user.id]),pk=course_id)
            except Course.DoesNotExist:
                print(f"Query: status={PUBLISHED}, user={user}, pk={course_id}")
                raise GraphQLError("Course unavailable")            
            filter = (
                Q(course_id=course_id)
            )
            qs = qs = qs.filter(filter)
            
        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["EXERCISE"]:
        chapter_id = options['chapter_id']
        try:
            chapter = Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist:
            return None

        PUBLISHED = Course.StatusChoices.PUBLISHED
        
        if chapter.status != PUBLISHED:
            has_access(user,RESOURCES["CHAPTER"], ACTIONS["CREATE"], False)
        else:
            pass
            
        qs = Exercise.objects.all().filter(
            chapter_id=chapter_id).order_by("index")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["EXERCISE_SUBMISSION"]:
        grader = has_access(user, RESOURCES["EXERCISE_SUBMISSION"], ACTIONS["LIST"])
        if grader == True:
            qs = ExerciseSubmission.objects.all().order_by("-id")
        else:
            qs = ExerciseSubmission.objects.all().filter(participant_id=user.id).order_by("-id")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["REPORT"]:
        admin_user = is_admin_user(user)
        if admin_user:
            qs = Report.objects.all().order_by("-completed")
        else:
            report_list = has_access(user, RESOURCES["REPORT"], ACTIONS["LIST"])
            if report_list == True:
                qs = Report.objects.all().filter(institution_id=user.institution.id).order_by("-completed")
            else:
                qs = []

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["EXERCISE_KEY"]:
        grader = has_access(user, RESOURCES["EXERCISE_SUBMISSION"], ACTIONS["LIST"])
        if grader == True:
            qs = ExerciseKey.objects.all().order_by("id")
        else:
            qs = []

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["CHAT"]:
        qs = Chat.objects.all().filter(chat_type="IL")
        qs = qs = qs.filter(Q(individual_member_one=user.id) | Q(
            individual_member_two=user.id))

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs
        
    if RESOURCE_TYPE == RESOURCES["CHAT_MESSAGE"]:
        chat_id = options["chat_id"]
        accessible_chat_ids = rows_accessible(user, RESOURCES["CHAT"]).values_list("id", flat=True)
        if chat_id is None:
            qs = ChatMessage.objects.all().filter(Q(chat_id__in=accessible_chat_ids)).order_by("-id")
        elif chat_id in accessible_chat_ids:
            qs = ChatMessage.objects.all().filter(chat=chat_id).order_by("-id")
        else:
            qs = []

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["ISSUE"]:
        admin_user = is_admin_user(user)
        if admin_user:
            # if the user is super user then they gbet to see all issues
            qs = Issue.objects.all().order_by("-id")
        else:
            # If the user is not a super user, we filter issues pertaining to their institution and users in their institution
            qs = Issue.objects.filter(institution_id=user.institution.id).order_by("-id")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["CRITERION"]:
        accessible_exercise_ids = rows_accessible(user, RESOURCES["COURSE"]).values_list("id",flat=True)
        qs = CourseSection.objects.all().filter(Q(exercise_id__in=accessible_exercise_ids)).order_by("index")

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

    if RESOURCE_TYPE == RESOURCES["CRITERION_RESPONSE"]:
        accessible_exercise_submission_ids = rows_accessible(user, RESOURCES['EXERCISE_SUBMISSION']).values_list('id',flat=True)

        qs = CriterionResponse.objects.all().filter(Q(exercise_submission_id__in=accessible_exercise_submission_ids)).order_by("-id")
        
        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs
        
    if RESOURCE_TYPE == RESOURCES["COURSE_SECTION"]:
        course_id = options["course_id"]
        if course_id is not None:
            try:
                course = Course.objects.filter(Q(status=Course.StatusChoices.PUBLISHED) | Q(instructors__in=[user.id]), pk=course_id, active=True, )
            except:
                raise GraphQLError("Course unavailable")
            qs = CourseSection.objects.all().filter(course_id=course_id).order_by("index")
        else:
            qs = []

        if subscription_method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)
        return qs

def is_record_accessible(user, RESOURCE_TYPE, record=None, subscription_method=None, options={}):
    if record is None or user is None or RESOURCE_TYPE is None:
        return False

    default_options = {'subscription_method': subscription_method}

    if RESOURCE_TYPE == RESOURCES["MEMBER"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options )

        allow_access = qs = qs.filter(id=record.id).exists()

        return allow_access

    if RESOURCE_TYPE == RESOURCES["INSTITUTION"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options )

        allow_access = qs = qs.filter(id=record.id).exists()

        return allow_access
            
    if RESOURCE_TYPE == RESOURCES["USER_ROLE"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options )

        allow_access = qs = qs.filter(name=record.name).exists()

        return allow_access            

    if RESOURCE_TYPE == RESOURCES["ANNOUNCEMENT"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options )

        allow_access = qs = qs.filter(id=record.id).exists()

        return allow_access

    if RESOURCE_TYPE == RESOURCES["GROUP"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options )

        allow_access = qs = qs.filter(id=record.id).exists()

        return allow_access

    if RESOURCE_TYPE == RESOURCES["PROJECT"]:
        qs = rows_accessible(user, RESOURCE_TYPE, options )

        allow_access = qs = qs.filter(id=record.id).exists()

        return allow_access

    if RESOURCE_TYPE == RESOURCES["COURSE"]:
        allow_access = not is_course_locked(user, record)

        return allow_access

    if RESOURCE_TYPE == RESOURCES["CHAPTER"]:
        chapter_is_locked = is_chapter_locked(user, record)

        allow_access = chapter_is_locked is None

        return allow_access

    if RESOURCE_TYPE == RESOURCES["EXERCISE"]:
        chapter_is_locked = is_chapter_locked(user, record.chapter)

        allow_access = chapter_is_locked is None

        return allow_access

    if RESOURCE_TYPE == RESOURCES["EXERCISE_SUBMISSION"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()

        return allow_access

    if RESOURCE_TYPE == RESOURCES["REPORT"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access

    if RESOURCE_TYPE == RESOURCES["EXERCISE_KEY"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access

    if RESOURCE_TYPE == RESOURCES["CHAT"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access
        
    if RESOURCE_TYPE == RESOURCES["CHAT_MESSAGE"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access

    if RESOURCE_TYPE == RESOURCES["ISSUE"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access

    if RESOURCE_TYPE == RESOURCES["CRITERION"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access

    if RESOURCE_TYPE == RESOURCES["CRITERION_RESPONSE"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access

    if RESOURCE_TYPE == RESOURCES["COURSE_SECTION"]:
        qs = rows_accessible(user, RESOURCE_TYPE, default_options)

        allow_access = qs = qs.filter(id=record.id).exists()
        
        return allow_access