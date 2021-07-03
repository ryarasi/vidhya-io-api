import graphene
from graphene.types import generic
from graphene_django.types import DjangoObjectType
from vidhya.models import User, UserRole, Institution, Group, Announcement, Course, Assignment, Chat, ChatMessage


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
    id = graphene.ID()
    name = graphene.String(required=True)
    description = graphene.String(required=True)
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


class ChatMessageInput(graphene.InputObjectType):
    id = graphene.ID()
    chat_id = graphene.ID(name="chat")
    message = graphene.String(required=True)
    author_id = graphene.ID(name="author", required=True)
