from django.db.models.deletion import DO_NOTHING
import graphene
from graphene.types import generic
from graphene_django.types import DjangoObjectType
from django.db.models import Q
from vidhya.models import AnnouncementsSeen, CompletedChapters, CompletedCourses, Criterion, CriterionResponse, Issue, MandatoryChapters, MandatoryRequiredCourses, Project, User, UserRole, Institution, Group, Announcement, Course, CourseSection, Chapter, Exercise, ExerciseKey, ExerciseSubmission, SubmissionHistory, Report, Chat, ChatMessage
from django.db import models
from vidhya.authorization import USER_ROLES_NAMES

##############
# Query Types
##############


class InstitutionType(DjangoObjectType):

    class Meta:
        model = Institution


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserRoleType(DjangoObjectType):
    class Meta:
        model = UserRole


class GroupType(DjangoObjectType):
    adminCount=graphene.Int()
    memberCount=graphene.Int()

    def resolve_adminCount(self, info):
        return self.admins.count()

    def resolve_memberCount(self, info):
        return self.members.count()

    class Meta:
        model = Group


class AnnouncementType(DjangoObjectType):
    seen = graphene.Boolean()

    def resolve_seen(self, info):
        seen = False
        user = info.context.user  
        announcements_seen = AnnouncementsSeen.objects.all().filter(user_id=user.id)
        announcements_seen_ids = announcements_seen.values_list('announcement_id',flat=True)

        if self.id in announcements_seen_ids:
            seen = True
        return seen

    class Meta:
        model = Announcement

class ProjectType(DjangoObjectType):

    class Meta:
        model = Project    

class IssueType(DjangoObjectType):
    title = graphene.String()
    subtitle = graphene.String()

    def get_issue_resource(input):
        resource=None
        if input.resource_type == Issue.ResourceTypeChoices.CHAPTER:
            try:
                resource=Chapter.objects.get(pk=input.resource_id,active=True)
            except:
                pass
        elif input.resource_type == Issue.ResourceTypeChoices.COURSE:
            try:
                resource=Course.objects.get(pk=input.resource_id,active=True)
            except:
                pass
        elif input.resource_type == Issue.ResourceTypeChoices.INSTITUTION:
            try:
                resource=Institution.objects.get(code=input.resource_id,active=True)
            except:
                pass
        elif input.resource_type == Issue.ResourceTypeChoices.PROJECT:
            try:
                resource=Project.objects.get(pk=input.resource_id,active=True)
            except:
                pass
        elif input.resource_type == Issue.ResourceTypeChoices.SUBMISSION:
            try:
                resource=Project.objects.get(pk=input.resource_id,active=True)
            except:
                pass
        
        elif input.resource_type == Issue.ResourceTypeChoices.USER:
            try:
                resource=User.objects.get(username=input.resource_id,active=True)
            except:
                pass
        return resource     

    def resolve_title(self, info):
        title = None
        resource = IssueType.get_issue_resource(self)
        if resource is not None:
            if self.resource_type == Issue.ResourceTypeChoices.CHAPTER:
                title = resource.title
            elif self.resource_type == Issue.ResourceTypeChoices.COURSE:
                title = resource.title
            elif self.resource_type == Issue.ResourceTypeChoices.INSTITUTION:
                title = resource.name
            elif self.resource_type == Issue.ResourceTypeChoices.PROJECT:
                title = resource.title
            elif self.resource_type == Issue.ResourceTypeChoices.SUBMISSION:
                title = resource.participant.name + "'s exercise submission"
            elif self.resource_type == Issue.ResourceTypeChoices.USER:
                title = resource.name     
        return title

    def resolve_subtitle(self, info):
        subtitle = None
        resource = IssueType.get_issue_resource(self)

        if resource is not None:
            if self.resource_type == Issue.ResourceTypeChoices.CHAPTER:
                subtitle = "Chapter in " + resource.course.title
            elif self.resource_type == Issue.ResourceTypeChoices.COURSE:
                subtitle = "Course taught by " + resource.author.name
            elif self.resource_type == Issue.ResourceTypeChoices.INSTITUTION:
                subtitle = "Institution located in " + resource.location
            elif self.resource_type == Issue.ResourceTypeChoices.PROJECT:
                subtitle = "Project by " + resource.author.name
            elif self.resource_type == Issue.ResourceTypeChoices.SUBMISSION:
                subtitle = "For "+ resource.chapter.title+' in ' + resource.course.title
            elif self.resource_type == Issue.ResourceTypeChoices.USER:
                subtitle = resource.role.name + ', ' + resource.institution.name
        return subtitle

    class Meta:
        model = Issue

class ReportType(DjangoObjectType):

    class Meta:
        model = Report

class CourseType(DjangoObjectType):
    completed = graphene.Boolean()
    report = graphene.Field(ReportType)
    locked = graphene.Boolean()

    def resolve_completed(self, info):
        user = info.context.user
        completed = CompletedCourses.objects.filter(participant_id=user.id, course_id=self.id).exists()
        return completed

    def resolve_report(self, info):
        report = None
        try:
            report = Report.objects.get(participant_id=info.context.user.id, course_id=self.id, active=True)
        except:
            pass
        return report

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

    class Meta:
        model = CourseSection


class ChapterType(DjangoObjectType):
    completed = graphene.Boolean()
    completion_status = graphene.String()
    locked = graphene.String()

    def resolve_completed(self, info):
        user = info.context.user
        completed = CompletedChapters.objects.filter(participant_id=user.id, chapter_id=self.id).exists()
        return completed


    def resolve_completion_status(self, info):
        user = info.context.user
        status = ExerciseSubmission.StatusChoices.PENDING
        try:
            completed = CompletedChapters.objects.get(participant_id=user.id, chapter_id=self.id)
            status = completed.status
        except:
            pass
        return status      

    def resolve_locked(self, info):
        locked = None
        user = info.context.user

        # Letting the user see it if they are a grader
        user_role = user.role.name;
        grader = user_role == USER_ROLES_NAMES['GRADER']

        # Checking if the user is the author of the course or a grader
        if self.course.instructor.id == user.id or grader:
            # If yes, we mark it as unlocked
            return locked

        course_locked = CourseType.resolve_locked(self.course, info) # Checking if this belongs to a course that is locked
        if course_locked:
            # If the course is locked, we immediately return locked is true
            locked = 'This course is locked for you'
            return locked

        # If the course is unlocked we 
        completed_chapters = CompletedChapters.objects.all().filter(participant_id=user.id)
        required_chapters = MandatoryChapters.objects.all().filter(chapter_id=self.id)
        required_chapter_ids = required_chapters.values_list('requirement_id',flat=True)
        completed_chapter_ids = completed_chapters.values_list('chapter_id',flat=True)
        pending_chapter_ids = []
        for id in required_chapter_ids:
            if id not in completed_chapter_ids:
                pending_chapter_ids.append(id)
        if pending_chapter_ids:
            locked= 'To participate in this course, you must have completed '
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

    class Meta:
        model = Chapter

class CriterionType(DjangoObjectType):

    class Meta:
        model = Criterion

class CriterionResponseType(DjangoObjectType):

    class Meta:
        model = CriterionResponse

class ExerciseType(DjangoObjectType):
    rubric = graphene.List(CriterionType)

    def resolve_rubric(self, info):
        rubric = Criterion.objects.filter(exercise_id=self.id, active=True).order_by('id')
        return rubric        

    class Meta:
        model = Exercise


class ExerciseKeyType(DjangoObjectType):

    class Meta:
        model = ExerciseKey

class ExerciseSubmissionType(DjangoObjectType):
    rubric = graphene.List(CriterionResponseType)

    def resolve_rubric(self, info):
        rubric = CriterionResponse.objects.filter(exercise_id=self.exercise.id, participant_id=self.participant.id, active=True).order_by('id')
        return rubric        
    class Meta:
        model = ExerciseSubmission

class SubmissionHistoryType(DjangoObjectType):

    class Meta:
        model = SubmissionHistory

class ChatType(DjangoObjectType):

    class Meta:
        model = Chat


class ChatMessageType(DjangoObjectType):
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
    code = graphene.String(required=True)
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

class ProjectInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    author_id=graphene.ID(name="author", required=True)
    course_id=graphene.ID(name="course")
    description = graphene.String(required=True)
    link = graphene.String()
    public = graphene.Boolean(required=True)


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
    pass_score_percentage = graphene.Int()
    pass_completion_percentage = graphene.Int()
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

class CriterionInput(graphene.InputObjectType):
    id = graphene.ID()
    exercise_id = graphene.ID(name="exercise")
    description = graphene.String(required=True)
    points = graphene.Int(required=True)
    active = graphene.Boolean()

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
    remarks= graphene.String()
    rubric= graphene.List(CriterionInput)


class CriterionResponseInput(graphene.InputObjectType):
    id = graphene.ID()
    criterion_id = graphene.ID(name="criterion", required=True)
    exercise_id = graphene.ID(name="exercise")
    participant_id = graphene.ID(name="participant")
    remarker_id = graphene.ID(name="remarker")
    score = graphene.Int()
    remarks = graphene.String()


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
    rubric = graphene.List(CriterionResponseInput)
    percentage = graphene.Int()
    status = graphene.String()
    remarks = graphene.String()
    flagged = graphene.Boolean()
    grader = graphene.ID()
    createdAt = graphene.String()
    updatedAt = graphene.String()

class ReportInput(graphene.InputObjectType):
    id = graphene.ID()
    participant_id = graphene.ID(name="participant", required=True)
    institution_id = graphene.ID(name="institution", required=True)
    course_id = graphene.ID(name="course", required=True)
    completed = graphene.Int(required=True)
    score = graphene.Int(required=True)

class IssueInput(graphene.InputObjectType):
    id = graphene.ID()
    link = graphene.String(required=True)
    description= graphene.String(required=True)
    resource_id = graphene.String(required=True)
    resource_type = graphene.String(required=True)
    reporter_id = graphene.ID(name="reporter")
    guest_name=graphene.String()
    guest_email=graphene.String()
    screenshot=graphene.String()
    status=graphene.String()
    remarks=graphene.String()

class ChatMessageInput(graphene.InputObjectType):
    id = graphene.ID()
    chat_id = graphene.ID(name="chat")
    message = graphene.String(required=True)
    author_id = graphene.ID(name="author", required=True)

class IndexListInputType(graphene.InputObjectType):
    id = graphene.ID()
    index = graphene.Int()