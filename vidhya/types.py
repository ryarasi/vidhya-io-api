
from graphene_django.types import DjangoObjectType
from vidhya.models import User, Institution, Group
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from graphene_django_extras import DjangoInputObjectType, DjangoListObjectType

##############
# Query Types
##############


class InstitutionType(DjangoObjectType):
    class Meta:
        model = Institution
        description = "Type type definition for a single Institution"
        filter_fields = {
            "id": ("exact"),
            "searchField": ("icontains", "iexact"),
            "active": ("exact")
        }


class InstitutionListType(DjangoListObjectType):
    class Meta:
        description = "Type definition for user list"
        model = Institution
        pagination = LimitOffsetGraphqlPagination(
            default_limit=25, ordering="-last_login")


class UserType(DjangoObjectType):
    class Meta:
        model = User
        description = "Type type definition for a single User"
        filter_fields = {
            "id": ("exact"),
            "searchField": ("icontains", "iexact"),
            "active": ("exact")
        }


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        description = "Type type definition for a single Group"
        filter_fields = {
            "id": ("exact"),
            "searchField": ("icontains", "iexact"),
            "active": ("exact")
        }


################
# Mutation Types
################

class UserInput(DjangoInputObjectType):
    class Meta:
        description = " User InputType definition to use as input on an Arguments class on traditional Mutations "
        model = User


class InstitutionInput(DjangoInputObjectType):
    class Meta:
        description = " Institution InputType definition to use as input on an Arguments class on traditional Mutations "
        model = Institution
