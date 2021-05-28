
import graphene
from graphene_django.types import DjangoObjectType
from vidhya.models import User, Institution, Group
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from graphene_django_extras import DjangoInputObjectType, DjangoListObjectType, DjangoSerializerType
from .serializers import UserSerializer, InstitutionSerializer, GroupSerializer


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
        description = "Type type definition for a single Institution"
        serializer_class = InstitutionSerializer
        filter_fields = {
            "id": ("exact", ),
            "searchField": ("icontains", "iexact"),
        }


class InstitutionModelType(DjangoSerializerType):
    """ With this type definition it't necessary a mutation definition for user's model """

    class Meta:
        description = " Institution model type definition "
        serializer_class = InstitutionSerializer
        # ordering can be: string, tuple or list
        pagination = LimitOffsetGraphqlPagination(
            default_limit=25, ordering="-name")
        filter_fields = {
            "id": ("exact", ),
            "searchField": ("icontains", "iexact"),
        }


class UserType(DjangoObjectType):
    total_count = graphene.Int()  # shows total number of records in table

    def resolve_total_count(self, info):
        count = User.objects.count()
        return count

    class Meta:
        model = User
        description = "Type type definition for a single User"
        filter_fields = {
            "id": ("exact", ),
            "searchField": ("icontains", "iexact"),
        }


class UserModelType(DjangoSerializerType):
    """ With this type definition it't necessary a mutation definition for user's model """

    class Meta:
        description = " User model type definition "
        serializer_class = UserSerializer
        # ordering can be: string, tuple or list
        pagination = LimitOffsetGraphqlPagination(
            default_limit=25, ordering="-last_login")
        filter_fields = {
            "id": ("exact", ),
            "searchField": ("icontains", "iexact"),
        }


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        description = "Type type definition for a single Group"
        filter_fields = {
            "id": ("exact", ),
            "searchField": ("icontains", "iexact"),
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
