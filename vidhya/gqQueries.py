
import graphene
from graphene_django.types import ObjectType
from graphql_jwt.decorators import login_required
from vidhya.models import Institution, User, Group, Announcement
from django.db.models import Q
from .gqTypes import AnnouncementType, InstitutionType, UserType, GroupType
# Create a GraphQL type for the Institution model


class Query(ObjectType):
    institution = graphene.Field(InstitutionType, id=graphene.ID())
    institutions = graphene.List(
        InstitutionType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    user = graphene.Field(UserType, id=graphene.ID())
    users = graphene.List(
        UserType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    group = graphene.Field(GroupType, id=graphene.ID())
    groups = graphene.List(
        GroupType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    announcement = graphene.Field(AnnouncementType, id=graphene.ID())
    announcements = graphene.List(
        AnnouncementType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    @login_required
    def resolve_institution(root, info, id, **kwargs):
        institution_instance = Institution.objects.get(pk=id, active=True)
        if institution_instance is not None:
            return institution_instance
        else:
            return None

    @login_required
    def resolve_institutions(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = Institution.objects.all().filter(active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs

    @login_required
    def resolve_user(root, info, id, **kwargs):
        user_instance = User.objects.get(pk=id, active=True)
        if user_instance is not None:
            return user_instance
        else:
            return None

    @login_required
    def resolve_users(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = User.objects.all().filter(active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    def resolve_group(root, info, id, **kwargs):
        group_instance = Group.objects.get(pk=id, active=True)
        if group_instance is not None:
            return group_instance
        else:
            return None

    @login_required
    def resolve_groups(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = Group.objects.all().filter(active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    def resolve_announcement(root, info, id, **kwargs):
        announcement_instance = Announcement.objects.get(pk=id)
        if announcement_instance is not None:
            return announcement_instance
        else:
            return None

    @login_required
    def resolve_announcements(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = Announcement.objects.all().filter(active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs
