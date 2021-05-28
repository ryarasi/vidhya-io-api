from graphene_django.types import ObjectType
from .gqTypes import InstitutionType, UserType, UserListType, GroupType
from graphene_django_extras import DjangoObjectField, DjangoFilterPaginateListField, LimitOffsetGraphqlPagination

# Create a GraphQL type for the Institution model


class Query(ObjectType):
    institution = DjangoObjectField(
        InstitutionType, description='Single User query')
    user = DjangoObjectField(UserType, description='Single User query')
    group = DjangoObjectField(GroupType, description='Single User query')
    institutions = DjangoFilterPaginateListField(
        InstitutionType, pagination=LimitOffsetGraphqlPagination())
    users = DjangoFilterPaginateListField(
        UserType, pagination=LimitOffsetGraphqlPagination())
    groups = DjangoFilterPaginateListField(
        GroupType, pagination=LimitOffsetGraphqlPagination())
