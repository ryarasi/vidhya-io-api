import graphene
from graphql import GraphQLError
from graphene_django.types import ObjectType
from vidhya.models import User, Institution, Group
from .types import InstitutionType, UserType, GroupType

# Create a GraphQL type for the Institution model


class Query(ObjectType):
    institution = graphene.Field(InstitutionType, id=graphene.Int())
    user = graphene.Field(UserType, id=graphene.Int())
    group = graphene.Field(GroupType, id=graphene.Int())
    institutions = graphene.List(InstitutionType)
    users = graphene.List(UserType)
    groups = graphene.List(GroupType)

    def resolve_institution(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            institution = Institution.objects.get(pk=id, active=True)
            if not institution:
                raise GraphQLError('Institution not found!')
            return institution

        return None

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            user = User.objects.get(pk=id, active=True)
            if not user:
                raise GraphQLError('User not found!')
            return user

        return None

    def resolve_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            group = Group.objects.get(pk=id, active=True)
            if not group:
                raise GraphQLError('Group not found!')
            return group

        return None

    def resolve_institutions(self, info, **kwargs):
        return Institution.objects.filter(active=True)

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(active=True)

    def resolve_groups(self, info, **kwargs):
        return Group.objects.filter(active=True)
