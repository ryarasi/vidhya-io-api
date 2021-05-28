from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True,
                              null=True, default="https://i.imgur.com/XDZCq2b.png")
    institution = models.ForeignKey(
        'Institution', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

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
    invitecode = models.IntegerField(blank=True, null=True)
    searchField = models.CharField(max_length=900, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    searchField = models.CharField(max_length=400, blank=True, null=True)
    active = models.BooleanField(default=True)

    # Type Choices
    class TypeChoices(models.TextChoices):
        CLASS = "CL", _('Class')
        TEAM = "TE", _('Team')
        COORDINATiON = "CO", _('Coordination')
    # End of Type Choices

    group_type = models.CharField(
        max_length=2, choices=TypeChoices.choices, default=TypeChoices.TEAM)
    members = models.ManyToManyField(
        User, through='GroupMember', through_fields=('group', 'member'))

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    # Role Choices
    class MemberRole(models.TextChoices):
        ADMIN = "AD", _('Admin')
        LEADER = "LE", _('Leader')
        MEMBER = "ME", _('Member')
        GUEST = "GU", _('Guest')
    # End of Role Choices

    role = models.CharField(
        max_length=2, choices=MemberRole.choices, default=MemberRole.MEMBER)

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name
