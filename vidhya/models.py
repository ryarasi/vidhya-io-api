from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True, null=True)
    institution = models.ForeignKey('Institution', on_delete=models.PROTECT)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)


class Institution(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    logo = models.CharField(max_length=250, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)

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
