import graphene
from graphene_django.types import DjangoObjectType
from vidhya.models import User, Institution, Group, Announcement


##############
# Query Types
##############


class InstitutionType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Institution.objects.count()
        return count

    class Meta:
        model = Institution


class UserType(DjangoObjectType):
    class Meta:
        model = User


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class AnnouncementType(DjangoObjectType):
    class Meta:
        model = Announcement
