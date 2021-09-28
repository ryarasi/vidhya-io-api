from django.contrib.auth.models import AnonymousUser
import graphene
from graphene_django.types import ObjectType
from graphql_jwt.decorators import login_required, user_passes_test
from vidhya.models import Institution, User, UserRole, Group, Announcement, Course, CourseSection, Chapter, Exercise, ExerciseSubmission, ExerciseKey, Report, Chat, ChatMessage
from django.db.models import Q
from .gqTypes import AnnouncementType, ChapterType, ExerciseType, ExerciseSubmissionType, ExerciseKeyType, ReportType, ChatMessageType,  CourseSectionType, CourseType, InstitutionType, UserType, UserRoleType, GroupType, ChatType
from common.authorization import USER_ROLES_NAMES, has_access, RESOURCES, ACTIONS
from django.conf import settings
from graphql import GraphQLError

class Users(graphene.ObjectType):
    records = graphene.List(UserType)
    total = graphene.Int()

class UserRoles(graphene.ObjectType):
    records = graphene.List(UserRoleType)
    total = graphene.Int()

class Institutions(graphene.ObjectType):
    records = graphene.List(InstitutionType)
    total = graphene.Int()

class ActiveChats(graphene.ObjectType):
    chats = graphene.List(ChatType)
    groups = graphene.List(GroupType)


class ChatSearchResults(graphene.ObjectType):
    users = graphene.List(UserType)
    groups = graphene.List(GroupType)
    chat_messages = graphene.List(ChatMessageType)

class ExerciseAndSubmissionType(graphene.ObjectType):
    exercises = graphene.List(ExerciseType)
    submissions = graphene.List(ExerciseSubmissionType)

class ExerciseSubmissionGroup(graphene.ObjectType):
    id = graphene.ID()
    type = graphene.String()
    title = graphene.String()
    subtitle = graphene.String()
    count = graphene.Int()

class AssignmentType(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    course = graphene.String()
    section = graphene.String()
    status = graphene.String()
    dueDate = graphene.String()
    exerciseCount = graphene.Int()    
    submittedCount = graphene.Int()    
    gradedCount = graphene.Int()    
    pointsScored = graphene.Int()    
    percentage = graphene.Int()
    totalPoints = graphene.Int()    

class PublicUserType(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    name = graphene.String()
    title = graphene.String()
    bio = graphene.String()
    avatar = graphene.String()
    institution = graphene.Field(InstitutionType)
    courses = graphene.List(ReportType)
    score = graphene.Int()


class PublicUsers(graphene.ObjectType):
    records = graphene.List(PublicUserType)
    total = graphene.Int()

class Query(ObjectType):
    institution_by_invitecode = graphene.Field(
        InstitutionType, invitecode=graphene.String())
    institution = graphene.Field(InstitutionType, id=graphene.ID())
    institutions = graphene.Field(
        Institutions, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    user = graphene.Field(UserType, id=graphene.ID())
    user_by_username = graphene.Field(PublicUserType, username=graphene.String())
    users = graphene.Field(
        Users, searchField=graphene.String(), membership_status_not=graphene.List(graphene.String), membership_status_is=graphene.List(graphene.String), roles=graphene.List(graphene.String), limit=graphene.Int(), offset=graphene.Int())

    public_users = graphene.Field(
        PublicUsers, searchField=graphene.String(), membership_status_not=graphene.List(graphene.String), membership_status_is=graphene.List(graphene.String), roles=graphene.List(graphene.String), limit=graphene.Int(), offset=graphene.Int())

    user_role = graphene.Field(UserRoleType, role_name=graphene.String())
    user_roles = graphene.Field(
        UserRoles, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    group = graphene.Field(GroupType, id=graphene.ID())
    groups = graphene.List(
        GroupType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())
    admin_groups = graphene.List(
        GroupType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())        

    announcement = graphene.Field(AnnouncementType, id=graphene.ID())
    announcements = graphene.List(
        AnnouncementType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    course = graphene.Field(CourseType, id=graphene.ID())
    courses = graphene.List(
        CourseType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    course_section = graphene.Field(CourseSectionType, id=graphene.ID())
    course_sections = graphene.List(CourseSectionType, course_id=graphene.ID(required=True), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    chapter = graphene.Field(ChapterType, id=graphene.ID())
    chapters = graphene.List(
        ChapterType, course_id=graphene.ID(), searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    exercise = graphene.Field(ExerciseType, id=graphene.ID())
    exercises = graphene.Field(ExerciseAndSubmissionType, chapter_id=graphene.ID(required=True), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    exercise_submission = graphene.Field(
        ExerciseSubmissionType, id=graphene.ID())
    exercise_submissions = graphene.List(ExerciseSubmissionType, exercise_id=graphene.ID(), chapter_id=graphene.ID(), course_id=graphene.ID(), participant_id=graphene.ID(), status=graphene.String(), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    exercise_submission_groups = graphene.List(ExerciseSubmissionGroup, group_by=graphene.String(required=True), status=graphene.String(required=True), searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())
    assignments = graphene.List(AssignmentType, status=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    exercise_key = graphene.Field(
        ExerciseKeyType, exercise_id=graphene.ID())
    exercise_keys = graphene.List(ExerciseKeyType, exercise_id=graphene.ID(), chapter_id=graphene.ID(), course_id=graphene.ID(), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    report = graphene.Field(ReportType, id=graphene.ID())
    reports = graphene.List(ReportType, participant_id=graphene.ID(), course_id=graphene.ID(), institution_id=graphene.ID(), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    chat = graphene.Field(ChatType, id=graphene.ID())
    chats = graphene.Field(
        ActiveChats, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    chat_search = graphene.Field(ChatSearchResults, query=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    chat_message = graphene.Field(ChatMessageType, id=graphene.ID())
    chat_messages = graphene.List(ChatMessageType, chat_id=graphene.ID(), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    @login_required
    def resolve_institution_by_invitecode(root, info, invitecode, **kwargs):
        institution_instance = Institution.objects.get(
            invitecode=invitecode, active=True)
        if institution_instance is not None:
            return institution_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['INSTITUTION'], ACTIONS['GET']))
    def resolve_institution(root, info, id, **kwargs):
        institution_instance = Institution.objects.get(pk=id, active=True)
        if institution_instance is not None:
            return institution_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['INSTITUTION'], ACTIONS['LIST']))
    def resolve_institutions(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        current_user_role_name = current_user.role.name
        admin_user = current_user_role_name == USER_ROLES_NAMES["SUPER_ADMIN"]

        if admin_user:
            # if the user is super user then they
            qs = Institution.objects.all().filter(active=True).order_by('-id')
        else:
            # If the user is not a super user, we filter the users by institution
            qs = Institution.objects.all().filter(
                active=True, pk=current_user.institution.id).order_by('-id')        

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)
        total = len(qs)


        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        
        results = Institutions(records=qs, total=total)
        return results

    @login_required
    def resolve_user(root, info, id, **kwargs):
        user_instance = User.objects.get(pk=id, active=True)
        if user_instance is not None:
            return user_instance
        else:
            return None


    def resolve_user_by_username(root, info, username, **kwargs):
        user = None
        try:
            user = User.objects.get(username=username, active=True)
        except:
            raise GraphQLError('User does not exist!')
        courses = Report.objects.filter(active=True, participant_id=user.id)
        if user is not None:
            new_user = PublicUserType(id=user.id, username=user.username, name=user.name, title=user.title, bio=user.bio, avatar=user.avatar,institution=user.institution, courses=courses)
            return new_user      
        else:
            return None

    def process_users(root, info, searchField=None, all_institutions=False, membership_status_not=[], membership_status_is=[], roles=[], limit=None, offset=None, **kwargs):
        current_user = info.context.user
        institution_id = None
        print('Current user ', current_user)
        if current_user.is_anonymous:
            admin_user = False            
            print('current user is anonymous')
        else:
            institution_id = current_user.institution.id
            current_user_role_name = current_user.role.name
            admin_user = current_user_role_name == USER_ROLES_NAMES["SUPER_ADMIN"]

        if admin_user or all_institutions == True:
            # if the user is super user then they
            qs = User.objects.all().filter(active=True).order_by('-id')
        else:
            # If the user is not a super user, we filter the users by institution
            qs = User.objects.all().filter(
                active=True, institution_id=institution_id).order_by('-id')


        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower()) | Q(username__icontains=searchField.lower()) | Q(email__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if membership_status_not:
            qs = qs.exclude(membership_status__in=membership_status_not)

        if membership_status_is:
            qs = qs.filter(membership_status__in=membership_status_is)
        if roles:
            qs = qs.filter(role__in=roles)

        redacted_qs = []
        if admin_user:
            redacted_qs = qs
        else:
            # Replacing the user avatar if the requesting user is not of the same institution and is not a super admin
            for user in qs:
                if user.institution_id != institution_id:
                    user.avatar = settings.DEFAULT_AVATARS['USER']
                redacted_qs.append(user)
        
        pending = []
        uninitialized = []
        others = []
        for user in redacted_qs:
            if user.membership_status == User.StatusChoices.PENDINIG:
                pending.append(user)
            elif user.membership_status == User.StatusChoices.UNINITIALIZED:
                uninitialized.append(user)
            else:
                others.append(user)
        
        sorted_qs = pending + uninitialized + others
        
        total = len(sorted_qs)

        if offset is not None:
            sorted_qs = sorted_qs[offset:]

        if limit is not None:
            sorted_qs = sorted_qs[:limit]
        
        results = Users(records=sorted_qs, total=total)
        return results

    @login_required
    def resolve_users(root, info, searchField=None, membership_status_not=[], membership_status_is=[], roles=[], limit=None, offset=None, **kwargs):
        all_institutions=False
        qs = Query.process_users(root, info, searchField, all_institutions, membership_status_not, membership_status_is, roles, limit, offset, **kwargs)
        return qs

    def resolve_public_users(root, info, searchField=None, membership_status_not=[], membership_status_is=[], roles=[], limit=None, offset=None, **kwargs):   
        all_institutions=True
        results = Query.process_users(root, info, searchField, all_institutions, membership_status_not, membership_status_is, roles, limit, offset, **kwargs)

        records = results.records
        total = results.total

        public_users = []
        # This is to limit the fields in the User model that we are exposing in this GraphQL query
        for user in records:
            courses = Report.objects.filter(active=True, participant_id=user.id)
            score = 0
            for course in courses:
                score += course.completed * course.percentage
            new_user = PublicUserType(id=user.id, username=user.username, name=user.name, title=user.title, bio=user.bio, avatar=user.avatar,institution=user.institution, score=score)
            public_users.append(new_user)
        results = PublicUsers(records=public_users, total=total)
        return results

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['USER_ROLE'], ACTIONS['GET']))
    def resolve_user_role(root, info, role_name, **kwargs):
        user_role_instance = UserRole.objects.get(pk=role_name, active=True)
        if user_role_instance is not None:
            return user_role_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['USER_ROLE'], ACTIONS['LIST']))
    def resolve_user_roles(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        current_user_role = UserRole.objects.all().get(name=current_user.role, active=True)
        current_user_role_priority = current_user_role.priority
        qs = UserRole.objects.all().filter(priority__gte=current_user_role_priority, active=True).order_by('-name')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        total = len(qs)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        
        results = UserRoles(records=qs, total=total)
        return results

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['GET']))
    def resolve_group(root, info, id, **kwargs):
        current_user = info.context.user
        group_instance = Group.objects.get(pk=id, active=True)
        # Checking if the user requesting the group is not a member or an admin
        if current_user.id not in group_instance.members.values_list('id',flat=True) and current_user.id not in group_instance.admins.values_list('id',flat=True):
            group_instance = None
            
        return group_instance

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['LIST']))
    def resolve_groups(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        qs = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True).distinct().order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['LIST']))
    def resolve_admin_groups(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        qs = Group.objects.all().filter(
             Q(admins__in=[current_user]), active=True).distinct().order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['GET']))
    def resolve_announcement(root, info, id, **kwargs):
        current_user = info.context.user
        groups = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True).order_by('-id')

        announcement_instance = Announcement.objects.get(
            Q(recipients_global=True) | (Q(recipients_institution=True) & Q(institution_id=current_user.institution_id)) | Q(groups__in=groups),pk=id, active=True)
        if announcement_instance is not None:
            return announcement_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['LIST']))
    def resolve_announcements(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        groups = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True).order_by('-id')

        qs = Announcement.objects.all().filter(Q(recipients_global=True) | (Q(recipients_institution=True) & Q(institution_id=current_user.institution_id)) | Q(groups__in=groups),active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['GET']))
    def resolve_course(root, info, id, **kwargs):
        course_instance = Course.objects.get(pk=id, active=True)
        # locked = CourseType.resolve_locked(course_instance, info)
        # if locked:
        #     raise GraphQLError('This course is locked for you. Please complete the prerequisites.')

        if course_instance is not None:
            return course_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['LIST']))
    def resolve_courses(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        status = Course.StatusChoices.PUBLISHED
        if has_access(current_user, RESOURCES['COURSE'], ACTIONS['CREATE']):
            qs = Course.objects.all().filter(
                Q(participants__in=[current_user]) | Q(instructor_id=current_user.id), active=True).distinct().order_by('-id')
        else:
            qs = Course.objects.all().filter(
                Q(participants__in=[current_user]) | Q(instructor_id=current_user.id), status=status, active=True).distinct().order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['GET']))
    def resolve_course_section(root, info, id, **kwargs):
        course_instance = CourseSection.objects.get(pk=id, active=True)
        if course_instance is not None:
            return course_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['LIST']))
    def resolve_course_sections(root, info, course_id=None, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        if course_id is not None:
            try:
                course = Course.objects.get(Q(status=Course.StatusChoices.PUBLISHED) | Q(instructor_id=current_user.id), pk=course_id, active=True, )
            except:
                raise GraphQLError('Course unavailable')
            qs = CourseSection.objects.all().filter(
                active=True, course_id=course_id).order_by('index')

            if searchField is not None:
                filter = (
                    Q(searchField__icontains=searchField.lower())
                )
                qs = qs.filter(filter)

            if offset is not None:
                qs = qs[offset:]

            if limit is not None:
                qs = qs[:limit]

            return qs
        return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['GET']))
    def resolve_chapter(root, info, id, **kwargs):
        chapter_instance = Chapter.objects.get(pk=id, active=True)
        locked = ChapterType.resolve_locked(chapter_instance, info)
        if locked:
            raise GraphQLError('The chapter you requested is locked for you. Please complete the prerequisites.')
        if chapter_instance is not None:
            return chapter_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['LIST']))
    def resolve_chapters(root, info, course_id=None, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        status = Course.StatusChoices.PUBLISHED
        if has_access(current_user, RESOURCES['CHAPTER'], ACTIONS['CREATE']):
            qs = Chapter.objects.all().filter(active=True).order_by('index')
        else:
            qs = Chapter.objects.all().filter(active=True, status=status).order_by('index')

        
        if course_id is not None:
            try:
                course = Course.objects.get( Q(status=Course.StatusChoices.PUBLISHED) | Q(instructor_id=current_user.id),pk=course_id, active=True )
            except:
                raise GraphQLError('Course unavailable')            
            filter = (
                Q(course_id=course_id)
            )
            qs = qs.filter(filter)

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['GET']))
    def resolve_exercise(root, info, id, **kwargs):
        exercise_instance = Exercise.objects.get(pk=id, active=True)
        if exercise_instance is not None:
            return exercise_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['LIST']))
    def resolve_exercises(root, info, chapter_id=None, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
    
        if chapter_id is not None:
            try:
                chapter = Chapter.objects.get(pk=chapter_id, active=True)
            except Chapter.DoesNotExist:
                return None
            status = Course.StatusChoices.PUBLISHED
            if chapter.status != status:
                has_access(current_user,RESOURCES['CHAPTER'], ACTIONS['CREATE'], False)
            else:
                pass
             
            qs = Exercise.objects.all().filter(
                chapter_id=chapter_id, active=True).order_by('index')

            submissions = ExerciseSubmission.objects.all().filter(chapter_id = chapter_id, participant_id = current_user.id, active=True)

            if searchField is not None:
                filter = (
                    Q(searchField__icontains=searchField.lower())
                )
                qs = qs.filter(filter)

            if offset is not None:
                qs = qs[offset:]
                submissions = submissions[offset:]

            if limit is not None:
                qs = qs[:limit]
                submissions = submissions[:limit]

            return ExerciseAndSubmissionType(exercises=qs, submissions=submissions)
        return None


    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['GET']))
    def resolve_exercise_submission(root, info, id, **kwargs):
        exercise_submission_instance = ExerciseSubmission.objects.get(
            pk=id, active=True)
        if exercise_submission_instance is not None:
            return exercise_submission_instance
        else:
            return None   

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['LIST']))
    def resolve_exercise_submissions(root, info, exercise_id=None, chapter_id=None, course_id=None, participant_id=None, status=None, searchField=None, limit=None, offset=None, **kwargs):
        qs = ExerciseSubmission.objects.all().filter(active=True).order_by('-id')

        if exercise_id is not None:
            filter = (
                Q(exercise_id=exercise_id)
            )
            qs = qs.filter(filter)

        if participant_id is not None:
            filter = (
                Q(participant_id=participant_id)
            )
            qs = qs.filter(filter)

        if chapter_id is not None:
            filter = (
                Q(chapter_id=chapter_id)
            )
            qs = qs.filter(filter)

        if course_id is not None:
            filter = (
                Q(course_id=course_id)
            )
            qs = qs.filter(filter)

        if status is not None:
            filter = (
                Q(status=status)
            )
            qs = qs.filter(filter)

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['LIST']))    
    def resolve_exercise_submission_groups(root, info, group_by=None, status=None, searchField=None, limit=None, offset=None, **kwargs):
        groups = []

        if group_by == RESOURCES['EXERCISE_SUBMISSION']:
            unique_exercises = ExerciseSubmission.objects.filter(status=status ).values_list('exercise', flat=True).distinct().order_by()
            if searchField is not None:
                filter=Q(searchField__icontains=searchField.lower())
                unique_exercises = unique_exercises.filter(filter)
            for exercise_id in unique_exercises:
                exercise = Exercise.objects.get(pk=exercise_id)
                submissions = ExerciseSubmission.objects.all().filter(exercise=exercise, status=status)
                if searchField is not None:
                    filter=Q(searchField__icontains=searchField.lower())
                    submissions = submissions.filter(filter)
                count = submissions.count()                                
                card = ExerciseSubmissionGroup(id=exercise_id, type=group_by, title=exercise.prompt, subtitle=exercise.course.title, count=count)
                groups.append(card)
        
        if group_by == RESOURCES['CHAPTER']:
            unique_chapters = ExerciseSubmission.objects.filter(status=status).values_list('chapter', flat=True).distinct().order_by()
            if searchField is not None:
                filter=Q(searchField__icontains=searchField.lower())
                unique_chapters = unique_chapters.filter(filter)                   
            for chapter_id in unique_chapters:
                chapter = Chapter.objects.get(pk=chapter_id)
                submissions = ExerciseSubmission.objects.all().filter(chapter=chapter, status=status)
                if searchField is not None:
                    filter=Q(searchField__icontains=searchField.lower())
                    submissions = submissions.filter(filter)
                count = submissions.count()                
                card = ExerciseSubmissionGroup(id=chapter_id, type=group_by, title=chapter.title, subtitle=chapter.course.title, count=count)
                groups.append(card)        

        if group_by == RESOURCES['COURSE']:
            unique_courses = ExerciseSubmission.objects.filter(status=status).values_list('course', flat=True).distinct().order_by()
            if searchField is not None:
                filter=Q(searchField__icontains=searchField.lower())
                unique_courses = unique_courses.filter(filter)                                  
            for course_id in unique_courses:
                course = Course.objects.get(pk=course_id)
                submissions = ExerciseSubmission.objects.all().filter(course=course, status=status)
                if searchField is not None:
                    filter=Q(searchField__icontains=searchField.lower())
                    submissions = submissions.filter(filter)
                count = submissions.count()
                card = ExerciseSubmissionGroup(id=course_id, type=group_by, title=course.title, subtitle=course.blurb, count=count)
                groups.append(card)

        if offset is not None:
            groups = groups[offset:]

        if limit is not None:
            groups = groups[:limit]

        return groups   

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['CREATE']))    
    def resolve_assignments(root, info, status=None, limit=None, offset=None, **kwargs):
        assignments = []

        current_user = info.context.user

        courses = Course.objects.filter(participants__in=[current_user.id], active=True)

        course_ids = courses.values_list('id')

        chapters = []
        for course_id in course_ids:
            course_chapters = Chapter.objects.filter(course__in=[course_id], status=Chapter.StatusChoices.PUBLISHED, active=True).order_by('-id')
            for course_chapter in course_chapters:
                if not ChapterType.resolve_locked(course_chapter, info) and course_chapter.points > 0:
                    chapters.append(course_chapter)
       
        for chapter in chapters:
            chapter = Chapter.objects.get(pk=chapter.id)
            course = chapter.course.title 
            section = chapter.section.title if chapter.section is not None else None
            dueDate = chapter.due_date
            exerciseCount = Exercise.objects.all().filter(chapter_id=chapter.id,active=True).count()
            submittedCount = ExerciseSubmission.objects.all().filter(participant_id=current_user.id, chapter_id=chapter.id, status=ExerciseSubmission.StatusChoices.SUBMITTED,active=True).count()
            gradedCount = ExerciseSubmission.objects.all().filter(participant_id=current_user.id, chapter_id=chapter.id, status=ExerciseSubmission.StatusChoices.GRADED,active=True).count()
            totalPoints = chapter.points
            pointsScored = 0
            percentage = 0
            exercises = Exercise.objects.all().filter(chapter_id=chapter.id, active=True)
            # exercise_submissions = ExerciseSubmission.objects.all().filter(participant_id=current_user.id, chapter_id=chapter.id, status=ExerciseSubmission.StatusChoices.GRADED, active=True)
            chapter_status = ExerciseSubmission.StatusChoices.PENDING
            for exercise in exercises:
                try:
                    submission = ExerciseSubmission.objects.all().get(participant_id=current_user.id, exercise_id=exercise.id,active=True)
                    if submission.points is not None:
                        pointsScored += submission.points
                    if submission.percentage is not None:
                        percentage  += submission.percentage
                    if submission.status == ExerciseSubmission.StatusChoices.RETURNED:
                        chapter_status = ExerciseSubmission.StatusChoices.RETURNED                    
                except:
                    pass
            
            percentageCount = gradedCount + submittedCount
            percentage = percentage/percentageCount if percentageCount > 0 else 0
            percentage = percentage if exerciseCount > 0 else 100 # Giving them 100% if there are no exercises in the chapter
            if submittedCount == exerciseCount - gradedCount:
                chapter_status = ExerciseSubmission.StatusChoices.SUBMITTED
            if gradedCount == exerciseCount:
                chapter_status = ExerciseSubmission.StatusChoices.GRADED

            card = AssignmentType(id=chapter.id, title=chapter.title, course=course, section=section, status=chapter_status, dueDate=dueDate, exerciseCount=exerciseCount, submittedCount=submittedCount, gradedCount=gradedCount, totalPoints = totalPoints, percentage=percentage,pointsScored=pointsScored)
            assignments.append(card)        

        if status is not None:
            assignments = [assignment for assignment in assignments if assignment.status == status]

        # Sorting them
        pending = [assignment for assignment in assignments if assignment.status == ExerciseSubmission.StatusChoices.PENDING]
        returned = [assignment for assignment in assignments if assignment.status == ExerciseSubmission.StatusChoices.RETURNED]
        submitted = [assignment for assignment in assignments if assignment.status == ExerciseSubmission.StatusChoices.SUBMITTED]
        graded = [assignment for assignment in assignments if assignment.status == ExerciseSubmission.StatusChoices.GRADED]

        assignments = pending + returned + submitted + graded

        if offset is not None:
            assignments = assignments[offset:]

        if limit is not None:
            assignments = assignments[:limit]

       
        return assignments   

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_KEY'], ACTIONS['GET']))
    def resolve_exercise_key(root, info, exercise_id, **kwargs):
        exercise_key_instance = ExerciseKey.objects.get(
            exercise=exercise_id, active=True)
        if exercise_key_instance is not None:
            return exercise_key_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_KEY'], ACTIONS['LIST']))
    def resolve_exercise_keys(root, info, exercise_id=None, chapter_id=None, course_id=None, searchField=None, limit=None, offset=None, **kwargs):
        qs = ExerciseKey.objects.all().filter(active=True).order_by('id')

        if exercise_id is not None:
            filter = (
                Q(exercise_id=exercise_id)
            )
            qs = qs.filter(filter)

        if chapter_id is not None:
            filter = (
                Q(chapter_id=chapter_id)
            )
            qs = qs.filter(filter)

        if course_id is not None:
            filter = (
                Q(course_id=course_id)
            )
            qs = qs.filter(filter)


        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['GET']))
    def resolve_report(root, info, id, **kwargs):
        report_instance = Report.objects.get(pk=id, active=True)
        if report_instance is not None:
            return report_instance
        else:
            return None

    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['LIST']))
    def resolve_reports(root, info, participant_id=None, course_id=None, institution_id=None, searchField=None, limit=None, offset=None, **kwargs):

        qs = Report.objects.all().filter(active=True).order_by('-id')

        if participant_id is not None:
            filter = (
                Q(participant_id=participant_id)
            )
            qs = qs.filter(filter)

        if course_id is not None:
            filter = (
                Q(course_id=course_id)
            )
            qs = qs.filter(filter)

        if institution_id is not None:
            filter = (
                Q(institution_id=institution_id)
            )
            qs = qs.filter(filter)

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs

    @login_required
    def resolve_chat(root, info, id, **kwargs):
        chat_instance = Chat.objects.get(pk=id, active=True)
        if chat_instance is not None:
            return chat_instance
        else:
            return None

    @login_required
    def resolve_chats(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user

        groups = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True)

        chats = Chat.objects.all().filter(active=True, chat_type='IL')
        chats = chats.filter(Q(individual_member_one=current_user.id) | Q(
            individual_member_two=current_user.id))

        if offset is not None:
            chats = chats[offset:]
            groups = groups[offset:]

        if limit is not None:
            chats = chats[:limit]
            groups = groups[:limit]

        return ActiveChats(chats=chats, groups=groups)

    @login_required
    def resolve_chat_search(root, info, query=None, offset=None, limit=None, **kwargs):
        current_user = info.context.user

        groups = Group.objects.all()

        group_ids = groups.values_list('id')

        if query is not None:
            # "~Q(id=user_id)" is meant to exclude the current user from the results
            users = User.objects.all().filter(
                ~Q(id=current_user.id), Q(searchField__icontains=query), active=True,).order_by('-id')

            groups = Group.objects.all().filter(Q(name__icontains=query))
            groups = groups.filter(
                Q(members__in=[current_user]) | Q(admins__in=[current_user]))

            chat_messages = ChatMessage.objects.all().filter(
                Q(message__icontains=query), active=True, author=current_user.id)

            qs = ChatSearchResults(users=users, groups=groups,
                                   chat_messages=chat_messages)
            # qs.save()
            if offset is not None:
                qs = qs[offset:]

            if limit is not None:
                qs = qs[:limit]
            return qs
        else:
            return None

    @login_required
    def resolve_chat_message(root, info, id, **kwargs):
        chat_message_instance = ChatMessage.objects.get(pk=id, active=True)
        if chat_message_instance is not None:
            return chat_message_instance
        else:
            return None

    @login_required
    def resolve_chat_messages(root, info, chat_id=None, searchField=None, limit=None, offset=None, **kwargs):
        if chat_id is None:
            qs = ChatMessage.objects.all().filter(active=True).order_by('-id')
        else:
            qs = ChatMessage.objects.all().filter(chat=chat_id, active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(message__icontains=searchField.lower())
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs
