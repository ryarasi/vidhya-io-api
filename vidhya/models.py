from django.contrib.postgres.fields import ArrayField
from common.utils import random_number_with_N_digits
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import IntegerField
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings
# from django.db.models import JSONField

class User(AbstractUser):
    name = models.CharField(max_length=100, default='Uninitialized User')
    email = models.EmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True,
                              null=True, default=settings.DEFAULT_AVATARS['USER'])
    institution = models.ForeignKey(
        'Institution', on_delete=models.PROTECT, blank=True, null=True)
    role = models.ForeignKey(
        'UserRole', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)

    class StatusChoices(models.TextChoices):
        UNINITIALIZED = 'UI', _('UNINITIALIZED')
        PENDINIG = "PE", _('PENDIING')
        APPROVED = "AP", _('APPROVED')
        SUSPENDED = "SU", _('SUSPENDED')
    # End of Type Choices

    membership_status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.UNINITIALIZED)
    invitecode = models.CharField(max_length=10, validators=[
                                  MinLengthValidator(10)], blank=True, null=True)
    chapters = models.ManyToManyField('Chapter', through='CompletedChapters', through_fields=('participant', 'chapter'), blank=True)
    courses = models.ManyToManyField('Course', through='CompletedCourses', through_fields=('participant', 'course'), blank=True)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    last_active = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'{self.name}' 

class CompletedChapters(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.chapter.title}' 

class CompletedCourses(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.title}'

class UserRole(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=500,)
    priority = models.IntegerField() # Lower the number higher the priority

    def default_permissions():
        return {}
    permissions = JSONField(default=default_permissions)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 



class Institution(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    logo = models.CharField(
        max_length=250, blank=True, null=True, default=settings.DEFAULT_AVATARS['INSTITUTION'])
    bio = models.CharField(max_length=300, blank=True, null=True)

    def generate_invitecode():
        return random_number_with_N_digits(10)

    invitecode = models.CharField(max_length=10, validators=[
                                  MinLengthValidator(10)], unique=True, default=generate_invitecode)
    searchField = models.CharField(max_length=900, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    avatar = models.CharField(
        max_length=250, blank=True, null=True, default=settings.DEFAULT_AVATARS['GROUP'])
    searchField = models.CharField(max_length=400, blank=True, null=True)

    # Type Choices
    class TypeChoices(models.TextChoices):
        CLASS = "CL", _('Class')
        TEAM = "TE", _('Team')
        COORDINATiON = "CO", _('Coordination')
    # End of Type Choices

    group_type = models.CharField(
        max_length=2, choices=TypeChoices.choices, default=TypeChoices.TEAM)
    admins = models.ManyToManyField(User, related_name="adminInGroups", through="GroupAdmin", through_fields=(
        'group', 'admin'), blank=True)
    members = models.ManyToManyField(
        User, related_name="memberInGroups", through='GroupMember', through_fields=('group', 'member'), blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 


class GroupAdmin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Group {self.group.name}, member {self.admin.name}' 



class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Group {self.group.name}, member {self.member.name}' 


class Announcement(models.Model):
    title = models.CharField(max_length=80)
    author = models.ForeignKey(
        User, related_name="announcementAuthor", on_delete=models.PROTECT)
    message = models.CharField(max_length=1000)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    recipients_global = models.BooleanField(default=False)
    recipients_institution = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, through="AnnouncementGroup", through_fields=(
        'announcement', 'group'), blank=True)
    searchField = models.CharField(max_length=1200, blank=True, null=True)

    seenBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="announcementSeenBy", blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class AnnouncementGroup(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'Announcement {self.announcement.title}, Group {self.group.name}'


class Course(models.Model):
    title = models.CharField(max_length=80)
    blurb = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)
    institutions = models.ManyToManyField(Institution, through="CourseInstitution", through_fields=(
        'course', 'institution'), blank=True)
    participants = models.ManyToManyField(
        User, through="CourseParticipant", related_name="participants", through_fields=('course', 'participant'), blank=True)
    mandatory_prerequisites = models.ManyToManyField(
        'Course', related_name="required_courses",through='MandatoryRequiredCourses', through_fields=('course', 'requirement'), blank=True)
    recommended_prerequisites = models.ManyToManyField(
        'Course', related_name="optional_courses",through='OptionalRequiredCourses',  through_fields=('course', 'optional'), blank=True)
    start_date = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.CharField(max_length=100, blank=True, null=True)
    credit_hours = models.IntegerField(blank=True, null=True)

    class StatusChoices(models.TextChoices):
        DRAFT = 'DR', _('DRAFT')
        PUBLISHED = "PU", _('PUBLISHED')
        ARCHIVED = "AR", _('ARCHIVED')        
    # End of Type Choices

    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.DRAFT)


    searchField = models.CharField(max_length=1200, blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class MandatoryRequiredCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Course, related_name="requirement", on_delete=models.CASCADE)

class OptionalRequiredCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    optional = models.ForeignKey(Course, related_name="optional", on_delete=models.CASCADE)


class CourseInstitution(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.title}'


class CourseParticipant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Course {self.course.title}, Participant {self.participant.name}'


class CourseSection(models.Model):
    title = models.CharField(max_length=80)
    index = models.IntegerField(default=-1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Chapter(models.Model):
    title = models.CharField(max_length=80)
    instructions = models.CharField(max_length=1000)
    index = models.IntegerField(default=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(
        CourseSection, on_delete=models.DO_NOTHING, blank=True, null=True)
    prerequisites = models.ManyToManyField(
        'Chapter', related_name="required",through='MandatoryChapters', through_fields=('chapter', 'requirement'), blank=True)        
    due_date = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(default=0)

    class StatusChoices(models.TextChoices):
        DRAFT = 'DR', _('DRAFT')
        PUBLISHED = "PU", _('PUBLISHED')     
    # End of Type Choices

    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
        
    searchField = models.CharField(max_length=1200, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

class MandatoryChapters(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Chapter, related_name="requirement", on_delete=models.CASCADE)

class Exercise(models.Model):
    prompt = models.CharField(max_length=300)
    index = models.IntegerField(default=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class QuestionTypeChoices(models.TextChoices):
        OPTIONS = 'OP', _('OPTIONS')
        DESCRIPTION = "DE", _('DESCRIPTION')
        IMAGE = "IM", _('IMAGE')
        LINK = "LI", _('LINK')
    # End of Type Choices

    question_type = models.CharField(
        max_length=2, choices=QuestionTypeChoices.choices, default=QuestionTypeChoices.OPTIONS)
    required = models.BooleanField(default=True)
    options = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.prompt}'


class ExerciseKey(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    valid_option = models.CharField(
        max_length=200, blank=True, null=True)
    valid_answers = ArrayField(models.CharField(max_length=500, blank=True, null=True), blank=True, null=True)
    reference_link = models.CharField(max_length=500, blank=True, null=True)
    reference_images = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ExerciseSubmission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    option = models.CharField(
        max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=500, blank=True, null=True)
    link = models.CharField(max_length=5000, blank=True, null=True)
    images = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)

    class StatusChoices(models.TextChoices):
        PENDING = 'PE', _('PENDING')
        SUBMITTED = "SU", _('SUBMITTED')
        GRADED = "GR", _('GRADED')
        RETURNED = "RE", _('RETURNED')
    # End of Type Choices

    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    # This will be calculated on grading by dividing the number of graded exercise submissions by required exercises * 100
    completed = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, blank=True, null=True)
    individual_member_one = models.ForeignKey(
        User, related_name="chat_member_one", on_delete=models.CASCADE, blank=True, null=True)
    individual_member_two = models.ForeignKey(
        User, related_name="chat_member_two", on_delete=models.CASCADE, blank=True, null=True)

    # Type Choices
    class TypeChoices(models.TextChoices):
        INDIVIDUAL = "IL", _('Individual')
        GROUP = "GP", _('Group')
    # End of Type Choices

    chat_type = models.CharField(
        max_length=2, choices=TypeChoices.choices, default=TypeChoices.INDIVIDUAL)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)
    message = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User, related_name="chatAuthor", on_delete=models.DO_NOTHING)
    seenBy = models.ForeignKey(
        User, related_name="chatSeenBy", on_delete=models.PROTECT, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message}'

# For file uploads


class File(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name
