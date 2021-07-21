
import graphene
from graphene_django.types import ObjectType
from graphql_jwt.decorators import login_required
from vidhya.models import Institution, User, UserRole, Group, Announcement, Course, Assignment, Chat, ChatMessage
from django.db.models import Q
from .gqTypes import AnnouncementType, AssignmentType, ChatMessageType, ChatSearchModel, ChatSearchType, CourseType, InstitutionType, UserType, UserRoleType, GroupType, ChatType


class ActiveChats(graphene.ObjectType):
    chats = graphene.List(ChatType)
    groups = graphene.List(GroupType)


class ChatSearchResults(graphene.ObjectType):
    users = graphene.List(UserType)
    groups = graphene.List(GroupType)
    chat_messages = graphene.List(ChatMessageType)


class Query(ObjectType):
    institution_by_invitecode = graphene.Field(
        InstitutionType, invitecode=graphene.String())
    institution = graphene.Field(InstitutionType, id=graphene.ID())
    institutions = graphene.List(
        InstitutionType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    user = graphene.Field(UserType, id=graphene.ID())
    users = graphene.List(
        UserType, searchField=graphene.String(), membership_status_not=graphene.String(), role_name=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    user_role = graphene.Field(UserRoleType, id=graphene.ID())
    user_roles = graphene.List(
        UserRoleType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    group = graphene.Field(GroupType, id=graphene.ID())
    groups = graphene.List(
        GroupType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    announcement = graphene.Field(AnnouncementType, id=graphene.ID())
    announcements = graphene.List(
        AnnouncementType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    course = graphene.Field(CourseType, id=graphene.ID())
    courses = graphene.List(
        CourseType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    assignment = graphene.Field(AssignmentType, id=graphene.ID())
    assignments = graphene.List(
        AssignmentType, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    chat = graphene.Field(ChatType, id=graphene.ID())
    chats = graphene.Field(
        ActiveChats, searchField=graphene.String(), limit=graphene.Int(), offset=graphene.Int())

    chat_search = graphene.Field(ChatSearchResults, query=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    chat_message = graphene.Field(ChatMessageType, id=graphene.ID())
    chat_messages = graphene.List(ChatMessageType, chat_id=graphene.ID(), searchField=graphene.String(
    ), limit=graphene.Int(), offset=graphene.Int())

    @login_required
    def resolve_institution_by_invitecode(root, info, invitecode, **kwargs):
        institution_instance = Institution.objects.get(
            invitecode=invitecode, active=True)
        if institution_instance is not None:
            return institution_instance
        else:
            return None

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
    def resolve_users(root, info, searchField=None, membership_status_not=None, role_name=None, limit=None, offset=None, **kwargs):
        qs = User.objects.all().filter(active=True).order_by('-id')
        print('searchField', searchField, 'membership_status_not',
              membership_status_not, 'role', role_name)
        if searchField is not None:
            filter = (
                Q(searchField__icontains=searchField)
            )
            qs = qs.filter(filter)

        if membership_status_not is not None:
            qs = qs.exclude(membership_status=membership_status_not)

        if role_name is not None:
            try:
                role = UserRole.objects.get(active=True, name=role_name)
                print('role with role_name', role)
                qs = qs.filter(role=role)
            except UserRole.DoesNotExist:
                pass

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]
        return qs

    @login_required
    def resolve_user_role(root, info, id, **kwargs):
        user_role_instance = UserRole.objects.get(pk=id, active=True)
        if user_role_instance is not None:
            return user_role_instance
        else:
            return None

    @login_required
    def resolve_user_roles(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = UserRole.objects.all().filter(active=True).order_by('-id')

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
        current_user = info.context.user
        qs = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True).order_by('-id')

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
        current_user = info.context.user
        groups = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True).order_by('-id')

        announcement_instance = Announcement.objects.get(
            pk=id, active=True, groups__in=groups)
        if announcement_instance is not None:
            return announcement_instance
        else:
            return None

    @login_required
    def resolve_announcements(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user
        groups = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True).order_by('-id')

        qs = Announcement.objects.all().filter(
            active=True, groups__in=groups).order_by('-id')

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
    def resolve_course(root, info, id, **kwargs):
        course_instance = Course.objects.get(pk=id, active=True)
        if course_instance is not None:
            return course_instance
        else:
            return None

    @login_required
    def resolve_courses(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = Course.objects.all().filter(active=True).order_by('-id')

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
    def resolve_assignment(root, info, id, **kwargs):
        assignment_instance = Assignment.objects.get(pk=id, active=True)
        if assignment_instance is not None:
            return assignment_instance
        else:
            return None

    @login_required
    def resolve_assignments(root, info, searchField=None, limit=None, offset=None, **kwargs):
        qs = Assignment.objects.all().filter(active=True).order_by('-id')

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
    def resolve_chat(root, info, id, **kwargs):
        chat_instance = Chat.objects.get(pk=id, active=True)
        if chat_instance is not None:
            return chat_instance
        else:
            return None

    @login_required
    def resolve_chats(root, info, searchField=None, limit=None, offset=None, **kwargs):
        current_user = info.context.user

        groups = Group.objects.all().filter(
            Q(members__in=[current_user]) | Q(admins__in=[current_user]), active=True)

        chats = Chat.objects.all().filter(active=True, chat_type='IL')
        chats = chats.filter(Q(individual_member_one=current_user.id) | Q(
            individual_member_two=current_user.id))

        print('from resolve_chats => chats =>', chats, 'groups => ', groups)

        if offset is not None:
            chats = chats[offset:]
            groups = groups[offset:]

        if limit is not None:
            chats = chats[:limit]
            groups = groups[:limit]

        return ActiveChats(chats=chats, groups=groups)

    @login_required
    def resolve_chat_search(root, info, query=None, offset=None, limit=None, **kwargs):
        current_user = info.context.user

        # print('Got the users ', users)

        groups = Group.objects.all()

        print('Got the gropus', groups)

        group_ids = groups.values_list('id')

        print('Group Ids =>', group_ids)

        if query is not None:
            # "~Q(id=user_id)" is meant to exclude the current user from the results
            users = User.objects.all().filter(
                ~Q(id=current_user.id), Q(searchField__icontains=query), active=True,).order_by('-id')

            groups = Group.objects.all().filter(Q(name__icontains=query))
            groups = groups.filter(
                Q(members__in=[current_user]) | Q(admins__in=[current_user]))

            chat_messages = ChatMessage.objects.all().filter(
                Q(message__icontains=query), active=True, author=current_user.id)

            qs = ChatSearchResults(users=users, groups=groups,
                                   chat_messages=chat_messages)
            # qs.save()
            if offset is not None:
                qs = qs[offset:]

            if limit is not None:
                qs = qs[:limit]
            print('Gathered search result => ', qs)
            return qs
        else:
            return None

    @login_required
    def resolve_chat_message(root, info, id, **kwargs):
        chat_message_instance = ChatMessage.objects.get(pk=id, active=True)
        if chat_message_instance is not None:
            return chat_message_instance
        else:
            return None

    @login_required
    def resolve_chat_messages(root, info, chat_id=None, searchField=None, limit=None, offset=None, **kwargs):
        if chat_id is None:
            qs = ChatMessage.objects.all().filter(active=True).order_by('-id')
        else:
            qs = ChatMessage.objects.all().filter(chat=chat_id, active=True).order_by('-id')

        if searchField is not None:
            filter = (
                Q(message__icontains=searchField)
            )
            qs = qs.filter(filter)

        if offset is not None:
            qs = qs[offset:]

        if limit is not None:
            qs = qs[:limit]

        return qs
