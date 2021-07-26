from django.contrib.postgres.fields import ArrayField
from common.utils import random_number_with_N_digits
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import IntegerField
from django.db.models.deletion import CASCADE
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, AbstractUser
from django.db import models
# from django.db.models import JSONField


class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True,
                              null=True, default="https://i.imgur.com/KHtECqa.png")
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
    searchField = models.CharField(max_length=600, blank=True, null=True)
    last_active = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username


class UserRole(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=500,)
    priority = models.IntegerField()

    def default_permissions():
        return {}
    permissions = JSONField(default=default_permissions)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    logo = models.CharField(
        max_length=250, blank=True, null=True, default="https://i.imgur.com/dPO1MlY.png")
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
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    avatar = models.CharField(
        max_length=250, blank=True, null=True, default="https://i.imgur.com/hNdMk4c.png")
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
        return self.name


class GroupAdmin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.group


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.group


class Announcement(models.Model):
    title = models.CharField(max_length=80)
    author = models.ForeignKey(
        User, related_name="announcementAuthor", on_delete=models.PROTECT)
    message = models.CharField(max_length=1000)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    groups = models.ManyToManyField(Group, through="AnnouncementGroup", through_fields=(
        'announcement', 'group'), blank=True)
    searchField = models.CharField(max_length=1200, blank=True, null=True)

    seenBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="announcementSeenBy", blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AnnouncementGroup(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.announcement


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
        'Course', related_name="required", blank=True)
    recommended_prerequisites = models.ManyToManyField(
        'Course', related_name="optional", blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    credit_hours = models.IntegerField(blank=True, null=True)
    searchField = models.CharField(max_length=1200, blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseInstitution(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.course


class CourseParticipant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.course


class CourseSection(models.Model):
    title = models.CharField(max_length=80)
    index = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=80)
    instructions = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(
        CourseSection, on_delete=models.DO_NOTHING, blank=True, null=True)
    prerequisites = models.ManyToManyField(
        'Chapter', related_name="required", blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    searchField = models.CharField(max_length=1200, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    prompt = models.CharField(max_length=300)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    class QuestionTypeChoices(models.TextChoices):
        OPTIONS = 'OP', _('OPTIONS')
        DESCRIPTION = "DE", _('DESCRIPTION')
        FILE = "FL", _('FILE')
    # End of Type Choices

    question_type = models.CharField(
        max_length=2, choices=QuestionTypeChoices.choices, default=QuestionTypeChoices.OPTIONS)
    options = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExerciseFileAttachment(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=CASCADE)
    participant = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExerciseSubmission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=CASCADE)
    option = models.CharField(
        max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=500, blank=True, null=True)
    files = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True)

    class StatusChoices(models.TextChoices):
        DRAFT = 'DR', _('DRAFT')
        SUBMITTED = "CO", _('SUBMITTED')
        GRADED = "GR", _('GRADED')
        RETURNED = "RE", _('RETURNED')
    # End of Type Choices

    staus = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):
    participant = models.ForeignKey(User, on_delete=CASCADE)
    course = models.ForeignKey(Course, on_delete=CASCADE)
    # This will be calculated on grading by dividing the number of graded exercise submissions by required exercises * 100
    completed = models.IntegerField(default=0)
    score = models.IntegerField(default=0)


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

    def __str__(self):
        return self.chat_type


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
        return self.message

# For file uploads


class File(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name
