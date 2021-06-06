from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinLengthValidator
from common.utils import random_number_with_N_digits


class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True,
                              null=True, default="https://i.imgur.com/XDZCq2b.png")
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
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.name


class UserRole(models.Model):
    name = models.CharField(max_length=50,)
    description = models.CharField(max_length=500,)
    # priority = models.IntegerField()

    def default_permissions():
        return {}
    permissions = JSONField(default=default_permissions)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    logo = models.CharField(
        max_length=250, blank=True, null=True, default="https://i.imgur.com/hB0OXas.png")
    bio = models.CharField(max_length=300, blank=True, null=True)

    def generate_invitecode():
        return random_number_with_N_digits(10)

    invitecode = models.CharField(max_length=10, validators=[
                                  MinLengthValidator(10)], unique=True, default=generate_invitecode)
    searchField = models.CharField(max_length=900, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    chat = models.ForeignKey(
        'Chat', on_delete=models.PROTECT, blank=True, null=True)
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

    def __str__(self):
        return self.name


class GroupAdmin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=80)
    author = models.ForeignKey(
        User, related_name="announcementAuthor", on_delete=models.PROTECT)
    message = models.CharField(max_length=1000)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    groups = models.ManyToManyField(Group, through="AnnouncementGroup", through_fields=(
        'announcement', 'group'), blank=True)
    searchField = models.CharField(max_length=1200, blank=True, null=True)
    created = models.DateTimeField(
        blank=True, null=True)
    seenBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="announcementSeenBy", blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AnnouncementGroup(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)
    institutions = models.ManyToManyField(Institution, through="CourseInstitution", through_fields=(
        'course', 'institution'), blank=True)
    searchField = models.CharField(max_length=1200, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CourseInstitution(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=80)
    instructions = models.CharField(max_length=1000)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    searchField = models.CharField(max_length=1200, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Chat(models.Model):
    name = models.CharField(max_length=100)

    admins = models.ManyToManyField(User, related_name="adminInChats", through="ChatAdmin", through_fields=(
        'chat', 'admin'), blank=True)
    members = models.ManyToManyField(User, related_name="privateChats",
                                     through="ChatMember", through_fields=('chat', 'member'), blank=True)
    created = models.DateTimeField(
        blank=True, null=True)
    active = models.BooleanField(default=True)


class ChatAdmin(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)
    message = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User, related_name="chatAuthor", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(blank=True, null=True)
    seenBy = models.ForeignKey(
        User, related_name="chatSeenBy", on_delete=models.PROTECT, blank=True, null=True)


# For file uploads
class File(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name
