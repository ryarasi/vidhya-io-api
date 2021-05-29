from graphene_django.types import ObjectType
from .gqTypes import AnnouncementType, InstitutionType, UserType, GroupType
from graphene_django_extras import DjangoObjectField, DjangoFilterPaginateListField, LimitOffsetGraphqlPagination

# Create a GraphQL type for the Institution model


class Query(ObjectType):
    institution = DjangoObjectField(
        InstitutionType, description='Single Institution query')
    institutions = DjangoFilterPaginateListField(
        InstitutionType, pagination=LimitOffsetGraphqlPagination())
    user = DjangoObjectField(UserType, description='Single User query')
    users = DjangoFilterPaginateListField(
        UserType, pagination=LimitOffsetGraphqlPagination())
    group = DjangoObjectField(GroupType, description='Single Group query')
    groups = DjangoFilterPaginateListField(
        GroupType, pagination=LimitOffsetGraphqlPagination())
    announcement = DjangoObjectField(
        AnnouncementType, description='Single Group query')
    announcements = DjangoFilterPaginateListField(
        AnnouncementType, pagination=LimitOffsetGraphqlPagination())
