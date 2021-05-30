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
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = User.objects.count()
        return count

    class Meta:
        model = User


class GroupType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Group.objects.count()
        return count

    class Meta:
        model = Group


class AnnouncementType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Announcement.objects.count()
        return count

    class Meta:
        model = Announcement

##############
# Mutation Types
##############


class InstitutionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    location = graphene.String()
    city = graphene.String()
    website = graphene.String()
    phone = graphene.String()
    logo = graphene.String()
    bio = graphene.String()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    nick_name = graphene.String()
    email = graphene.String()
    avatar = graphene.String()
    institution_id = graphene.Int(name="institution", required=True)
    title = graphene.String()
    bio = graphene.String()


class GroupInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    group_type = graphene.String()
    institution_id = graphene.Int(name="institution", required=True)
    admins = graphene.List(graphene.Int)
    members = graphene.List(graphene.Int)


class AnnouncementInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    author = graphene.ID()
    message = graphene.String()
    institution_id = graphene.Int(name="institution", required=True)
    groups = graphene.List(graphene.Int)
