import graphene
from graphene_django.types import DjangoObjectType
from vidhya.models import User, Institution, Group, Announcement, Course, Assignment


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

    def resolve_total_count(self, info):
        count = Course.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Course


class AssignmentType(DjangoObjectType):
    total_count = graphene.Int()

    def resolve_total_count(self, info):
        count = Assignment.objects.all().filter(active=True).count()
        return count

    class Meta:
        model = Assignment

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


class GroupInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    group_type = graphene.String(required=True)
    institution_id = graphene.Int(name="institution", required=True)
    admin_ids = graphene.List(graphene.Int, name="admins", required=True)
    member_ids = graphene.List(graphene.Int, name="members", )


class AnnouncementInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    author_id = graphene.ID(name="author", required=True)
    message = graphene.String(required=True)
    institution_id = graphene.Int(name="institution", required=True)
    group_ids = graphene.List(graphene.Int, name="groups", required=True)


class CourseInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    instructor_id = graphene.ID(name="instructor", required=True)
    institution_ids = graphene.List(
        graphene.ID, name="institutions", required=True)


class AssignmentInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String(required=True)
    instructions = graphene.String(required=True)
    course_id = graphene.ID(name="course", required=True)
