from django.db.models.query_utils import Q
from graphql import GraphQLError
from django.conf import settings
from vidhya.models import User, Announcement, Chapter, Chat, ChatMessage, Course, CourseSection, Exercise, ExerciseKey, ExerciseSubmission, Group, Institution, Issue, Project, Report, UserRole

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
    "GROUP": "GROUP",
    "EXERCISE_KEY": "EXERCISE_KEY",
    "EXERCISE_SUBMISSION": "EXERCISE_SUBMISSION",
    "REPORT": "REPORT",
    "PROJECT": "PROJECT",
    "ISSUE": "ISSUE",
    "OWN_PROFILE": "OWN_PROFILE",
    "CHAT": "CHAT",
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


def rows_accessible(user, RESOURCE_TYPE, record=None, method=None, options={}):
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

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["INSTITUTION"]:
        admin_user = is_admin_user(user)

        if admin_user:
            # if the user is super user then they
            qs = Institution.objects.all().filter(active=True).order_by("-id")
        else:
            # If the user is not a super user, we filter the users by institution
            qs = Institution.objects.all().filter(
                active=True, pk=user.institution.id).order_by("-id")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs
            
    if RESOURCE_TYPE == RESOURCES["USER_ROLE"]:
        current_user_role = UserRole.objects.all().get(name=user.role, active=True)
        current_user_role_priority = current_user_role.priority
        qs = UserRole.objects.all().filter(priority__gte=current_user_role_priority, active=True).order_by("-priority")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(name=record.name).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["ANNOUNCEMENT"]:
        admin = is_admin_user(user)
        if admin:
            qs = Announcement.objects.all().order_by("-id")
        else:
            groups = rows_accessible(user, RESOURCES["GROUP"])
            
            qs = Announcement.objects.all().filter(Q(recipients_global=True) | (Q(recipients_institution=True) & Q(institution_id=user.institution_id)) | Q(groups__in=groups)).order_by("-id")
            
        if method == DELETE_METHOD:
            qs = qs.filter(active=False)
        else:
            qs = qs.filter(active=True)


        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["GROUP"]:
        admin_user = is_admin_user(user)
        if admin_user:
            qs = Group.objects.all().filter(active=True).order_by("-id")
        else:
            qs = Group.objects.all().filter(
                Q(members__in=[user]) | Q(admins__in=[user]), active=True).distinct().order_by("-id")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(name=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["PROJECT"]:
        qs = Project.objects.filter(active=True)
        author_id = options["author_id"]
        if author_id is not None:
            qs = Project.objects.filter(author_id=author_id, active=True)
        if author_id is not user.id:
            qs = qs.filter(public=True)
        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["COURSE"]:
        PUBLISHED = Course.StatusChoices.PUBLISHED
        if has_access(user, RESOURCES["COURSE"], ACTIONS["CREATE"]):
            qs = Course.objects.all().filter(
                Q(participants__in=[user]) | Q(instructor_id=user.id), active=True).distinct().order_by("-id")
        else:
            qs = Course.objects.all().filter(
                Q(participants__in=[user]) | Q(instructor_id=user.id), status=PUBLISHED, active=True).distinct().order_by("-id")
        
        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["CHAPTER"]:
        course_id = options["course_id"]
        PUBLISHED = Course.StatusChoices.PUBLISHED
        if has_access(user, RESOURCES["CHAPTER"], ACTIONS["CREATE"]):
            qs = Chapter.objects.all().filter(active=True).order_by("index")
        else:
            qs = Chapter.objects.all().filter(active=True, status=PUBLISHED).order_by("index")

        
        if course_id is not None:
            try:
                course = Course.objects.get( Q(status=PUBLISHED) | Q(instructor_id=user.id),pk=course_id, active=True )
            except:
                raise GraphQLError("Course unavailable")            
            filter = (
                Q(course_id=course_id)
            )
            qs = qs.filter(filter)
            
        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["EXERCISE"]:
        chapter_id = options["chapter_id"]
        try:
            chapter = Chapter.objects.get(pk=chapter_id, active=True)
        except Chapter.DoesNotExist:
            return None
        status = Course.StatusChoices.PUBLISHED
        if chapter.status != status:
            has_access(user,RESOURCES["CHAPTER"], ACTIONS["CREATE"], False)
        else:
            pass
            
        qs = Exercise.objects.all().filter(
            chapter_id=chapter_id, active=True).order_by("index")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["EXERCISE_SUBMISSION"]:
        grader = has_access(user, RESOURCES["EXERCISE_SUBMISSION"], ACTIONS["LIST"])
        if grader == True:
            qs = ExerciseSubmission.objects.all().order_by("-id")
        else:
            qs = ExerciseSubmission.objects.all().filter(participant_id=user.id).order_by("-id")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["REPORT"]:
        admin_user = is_admin_user(user)
        if admin_user:
            qs = Report.objects.all().order_by("-completed")
        else:
            report_list = has_access(user, RESOURCES["REPORT"], ACTIONS["LIST"])
            if report_list == True:
                qs = Report.objects.all(institution_id=user.institution.id).order_by("-completed")
            else:
                qs = []

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["EXERCISE_KEY"]:
        grader = has_access(user, RESOURCES["EXERCISE_SUBMISSION"], ACTIONS["LIST"])
        if grader == True:
            qs = ExerciseKey.objects.all().order_by("id")
        else:
            qs = []

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["CHAT"]:
        qs = Chat.objects.all().filter(active=True, chat_type="IL")
        qs = qs.filter(Q(individual_member_one=user.id) | Q(
            individual_member_two=user.id))

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs
        
    if RESOURCE_TYPE == RESOURCES["CHAT_MESSAGE"]:
        chat_id = options["chat_id"]
        accessible_chat_ids = rows_accessible(user, RESOURCES["CHAT"]).values_list("id", flat=True)
        if chat_id is None:
            qs = ChatMessage.objects.all().filter(Q(chat_id__in=accessible_chat_ids), active=True).order_by("-id")
        elif chat_id in accessible_chat_ids:
            qs = ChatMessage.objects.all().filter(chat=chat_id, active=True).order_by("-id")
        else:
            qs = []

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs

    if RESOURCE_TYPE == RESOURCES["ISSUE"]:
        admin_user = is_admin_user(user)
        if admin_user:
            # if the user is super user then they gbet to see all issues
            qs = Issue.objects.filter(active=True).order_by("-id")
        else:
            # If the user is not a super user, we filter issues pertaining to their institution and users in their institution
            qs = Issue.objects.filter(institution_id=user.institution.id).order_by("-id")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs        
    if RESOURCE_TYPE == RESOURCES["CRITERION"]:
        accessible_exercise_ids = rows_accessible(user, RESOURCES["COURSE"]).values_list("id",flat=True)
        qs = CourseSection.objects.all().filter(Q(exercise_id__in=accessible_exercise_ids)).order_by("index")

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs        
    # if RESOURCE_TYPE == RESOURCES["CRITERION_RESPONSE"]:
    if RESOURCE_TYPE == RESOURCES["COURSE_SECTION"]:
        course_id = options["course_id"]
        if course_id is not None:
            try:
                course = Course.objects.get(Q(status=Course.StatusChoices.PUBLISHED) | Q(instructor_id=user.id), pk=course_id, active=True, )
            except:
                raise GraphQLError("Course unavailable")
            qs = CourseSection.objects.all().filter(
                active=True, course_id=course_id).order_by("index")
        else:
            qs = []

        if method == DELETE_METHOD:
            qs.filter(active=False)
        else:
            qs.filter(active=True)

        if record is not None:
            return qs.filter(id=record.id).exists()
        else:
            return qs


    