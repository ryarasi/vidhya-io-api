
import graphene
from graphene_django.types import ObjectType
from graphql_jwt.decorators import login_required
from vidhya.models import Institution, User, Group, Announcement
from django.db.models import Q
from .gqTypes import AnnouncementType, InstitutionType, UserType, GroupType
# Create a GraphQL type for the Institution model


class Query(ObjectType):
    institution = graphene.Field(InstitutionType, id=graphene.Int())
    institutions = graphene.List(
        InstitutionType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(
        UserType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    group = graphene.Field(GroupType, id=graphene.Int())
    groups = graphene.List(
        GroupType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    announcement = graphene.Field(AnnouncementType, id=graphene.Int())
    announcements = graphene.List(
        AnnouncementType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    @login_required
    def resolve_institution(root, info, id, **kwargs):
        return Institution.objects.get(pk=id)

    @login_required
    def resolve_institutions(root, info, searchField, limit, offset, **kwargs):
        qs = Institution.objects.all().order_by('-id')

        if searchField:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)
        if limit:
            qs = qs[:limit]
        if offset:
            qs = qs[offset:]
        return qs

    @login_required
    def resolve_user(root, info, id, **kwargs):
        return User.objects.get(pk=id)

    @login_required
    def resolve_users(root, info, searchField, limit, offset, **kwargs):
        qs = User.objects.all().order_by('-id')

        if searchField:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)
        if limit:
            qs = qs[:limit]
        if offset:
            qs = qs[offset:]
        return qs

    @login_required
    def resolve_group(root, info, id, **kwargs):
        return Group.objects.get(pk=id)

    @login_required
    def resolve_groups(root, info, searchField, limit, offset, **kwargs):
        qs = Group.objects.all().order_by('-id')

        if searchField:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)
        if limit:
            qs = qs[:limit]
        if offset:
            qs = qs[offset:]
        return qs

    @login_required
    def resolve_announcement(root, info, id, **kwargs):
        return Announcement.objects.get(pk=id)

    @login_required
    def resolve_announcements(root, info, searchField, limit, offset, **kwargs):
        qs = Announcement.objects.all().order_by('-id')

        if searchField:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)
        if limit:
            qs = qs[:limit]
        if offset:
            qs = qs[offset:]
        return qs
