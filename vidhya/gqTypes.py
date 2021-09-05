from django.db.models.deletion import DO_NOTHING
import graphene
from graphene.types import generic
from graphene_django.types import DjangoObjectType
from vidhya.models import CompletedChapters, CompletedCourses, MandatoryChapters, MandatoryRequiredCourses, User, UserRole, Institution, Group, Announcement, Course, CourseSection, Chapter, Exercise, ExerciseKey, ExerciseSubmission, Report, Chat, ChatMessage
from django.db import models

##############
# Query Types
##############


class InstitutionType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Institution.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Institution


class UserType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = User.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = User


class UserRoleType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = UserRole.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = UserRole


class GroupType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Group.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Group


class AnnouncementType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Announcement.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Announcement


class CourseType(DjangoObjectType):
    total_count = graphene.Int()
    locked = graphene.Boolean()

    def resolve_total_count(self, info):
        count = Course.objects.all().filter(active=True).count()
        return count

    def resolve_locked(self, info):
        locked = False
        user = info.context.user
        # Checking if the user is the author of the course
        if self.instructor.id == user.id:
            # If yes, we mark it as unlocked
            locked = False
            return locked        
        completed_courses = CompletedCourses.objects.all().filter(participant_id=user.id)
        required_courses = MandatoryRequiredCourses.objects.all().filter(course_id=self.id)
        required_course_ids = required_courses.values_list('requirement_id',flat=True)
        completed_course_ids = completed_courses.values_list('course_id',flat=True)

        if required_course_ids:
            if not set(required_course_ids).issubset(set(completed_course_ids)):
                locked = True
        return locked

    class Meta:
        model = Course


class CourseSectionType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = CourseSection.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = CourseSection


class ChapterType(DjangoObjectType):
    total_count = graphene.Int()
    locked = graphene.Boolean()

    def resolve_total_count(self, info):
        count = Chapter.objects.all().filter(active=True).count()
        return count

    def resolve_locked(self, info):
        locked = False
        user = info.context.user
        # Checking if the user is the author of the course
        if self.course.instructor.id == user.id:
            # If yes, we mark it as unlocked
            locked = False
            return locked

        course_locked = CourseType.resolve_locked(self.course, info) # Checking if this belongs to a course that is locked
        if course_locked:
            # If the course is locked, we immediately return locked is true
            locked = True
            return True
        completed_chapters = CompletedChapters.objects.all().filter(participant_id=user.id)
        required_chapters = MandatoryChapters.objects.all().filter(chapter_id=self.id)
        required_chapter_ids = required_chapters.values_list('requirement_id',flat=True)
        completed_chapter_ids = completed_chapters.values_list('chapter_id',flat=True)

        if required_chapter_ids:
            if not set(required_chapter_ids).issubset(set(completed_chapter_ids)):
                locked = True
        return locked        

    class Meta:
        model = Chapter


class ExerciseType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Exercise.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Exercise

class ExerciseKeyType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = ExerciseKey.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = ExerciseKey

class ExerciseSubmissionType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = ExerciseSubmission.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = ExerciseSubmission


class ReportType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Report.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Report


class ChatType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Chat.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Chat


class ChatMessageType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = ChatMessage.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = ChatMessage


class ChatSearchModel(models.Model):
    users = models.ForeignKey(User, on_delete=DO_NOTHING)
    groups = models.ForeignKey(Group, on_delete=DO_NOTHING)
    chats = models.ForeignKey(Chat, on_delete=DO_NOTHING)
    chat_messages = models.ForeignKey(ChatMessage, on_delete=DO_NOTHING)


class ChatSearchType(DjangoObjectType):

    class Meta:
        model = ChatSearchModel

##############
# Mutation Types
##############



class InstitutionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    location = graphene.String(required=True)
    city = graphene.String(required=True)
    website = graphene.String()
    phone = graphene.String()
    logo = graphene.String()
    bio = graphene.String()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    nick_name = graphene.String()
    email = graphene.String()
    avatar = graphene.String()
    institution_id = graphene.Int(name="institution")
    title = graphene.String()
    bio = graphene.String()
    role_id = graphene.ID(name="role")


class UserRoleInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    priority = graphene.Int(required=True)
    permissions = generic.GenericScalar()


class GroupInput(graphene.InputObjectType):
    id = graphene.ID()
    avatar = graphene.String()
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    group_type = graphene.String(required=True)
    institution_id = graphene.Int(name="institution", required=True)
    admin_ids = graphene.List(graphene.Int, name="admins")
    member_ids = graphene.List(graphene.Int, name="members")


class AnnouncementInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    author_id = graphene.ID(name="author", required=True)
    message = graphene.String(required=True)
    institution_id = graphene.Int(name="institution", required=True)
    recipients_global = graphene.Boolean()
    recipients_institution = graphene.Boolean()
    group_ids = graphene.List(graphene.Int, name="groups", required=True)


class CourseInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    blurb = graphene.String(required=True)
    description = graphene.String(required=True)
    instructor_id = graphene.ID(name="instructor", required=True)
    institution_ids = graphene.List(
        graphene.ID, name="institutions")
    participant_ids = graphene.List(graphene.ID, name="participants")
    mandatory_prerequisite_ids = graphene.List(
        graphene.ID, name="mandatoryPrerequisites")
    recommended_prerequisite_ids = graphene.List(
        graphene.ID, name="recommendedPrerequisites")
    start_date = graphene.String()
    end_date = graphene.String()
    credit_hours = graphene.Int()
    status = graphene.String()


class CourseSectionInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    index = graphene.Int(required=True)
    course_id = graphene.ID(name="course", required=True)


class ChapterInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    index = graphene.Int()    
    instructions = graphene.String(required=True)
    course_id = graphene.ID(name="course", required=True)
    section_id = graphene.ID(name="section")
    prerequisite_ids = graphene.List(graphene.ID, name="prerequisites")
    due_date = graphene.String()
    points = graphene.Int()
    status = graphene.String()

class ExerciseInput(graphene.InputObjectType):
    id = graphene.ID()
    prompt = graphene.String(required=True)
    index = graphene.Int()
    chapter_id = graphene.ID(name="chapter", required=True)
    course_id = graphene.ID(name="course", required=True)
    question_type = graphene.String(required=True)
    required = graphene.Boolean(required=True)
    options = graphene.List(graphene.String)
    points = graphene.Int()
    valid_option = graphene.String()
    valid_answers = graphene.List(graphene.String)
    reference_link = graphene.String()
    reference_images = graphene.List(graphene.String)
    remarks=graphene.String()

class ExerciseKeyInput(graphene.InputObjectType):
    id = graphene.ID()
    exercise_id = graphene.ID(name="exercise", required=True) 
    chapter_id = graphene.ID(name="chapter", required=True)
    course_id = graphene.ID(name="course", required=True)       
    valid_option = graphene.String()
    valid_answers = graphene.List(graphene.String)
    reference_link = graphene.String()
    reference_images = graphene.List(graphene.String)    
    remarks = graphene.String()

class ExerciseSubmissionInput(graphene.InputObjectType):
    id = graphene.ID()
    exercise_id = graphene.ID(name="exercise", required=True)
    chapter_id = graphene.ID(name="chapter", required=True)
    course_id = graphene.ID(name="course", required=True) 
    participant_id = graphene.ID(name="participant", required=True)
    option = graphene.String()
    answer = graphene.String()
    link = graphene.String()
    images = graphene.List(graphene.String)
    points = graphene.Decimal()
    percentage = graphene.Int()
    status = graphene.String()
    remarks = graphene.String()

class ReportInput(graphene.InputObjectType):
    id = graphene.ID()
    participant_id = graphene.ID(name="participant", required=True)
    institution_id = graphene.ID(name="institution", required=True)
    course_id = graphene.ID(name="course", required=True)
    completed = graphene.Int(required=True)
    score = graphene.Int(required=True)


class ChatMessageInput(graphene.InputObjectType):
    id = graphene.ID()
    chat_id = graphene.ID(name="chat")
    message = graphene.String(required=True)
    author_id = graphene.ID(name="author", required=True)

class IndexListInputType(graphene.InputObjectType):
    id = graphene.ID()
    index = graphene.Int()