from django.contrib.auth import login
import graphene
from graphql import GraphQLError
from vidhya.models import User, UserRole, Institution, Group, Announcement, Course, Chapter, Chat, ChatMessage
from graphql_jwt.decorators import login_required, user_passes_test
from .gqTypes import AnnouncementInput, AnnouncementType, AnnouncementType, ChapterInput, ChapterType, CourseInput, CourseType, GroupInput, InstitutionInput,  InstitutionType, UserInput, UserRoleInput,  UserType, UserRoleType, GroupType, ChatType, ChatMessageType, ChatMessageInput
from .gqSubscriptions import NotifyInstitution, NotifyUser, NotifyUserRole, NotifyGroup, NotifyAnnouncement, NotifyCourse, NotifyChapter, NotifyChat, NotifyChatMessage
from common.authorization import has_access, RESOURCES, ACTIONS

CREATE_METHOD = 'CREATE'
UPDATE_METHOD = 'UPDATE'
DELETE_METHOD = 'DELETE'


class CreateInstitution(graphene.Mutation):
    class Meta:
        description = "Mutation to create new a Institution"

    class Arguments:
        input = InstitutionInput(required=True)

    ok = graphene.Boolean()
    institution = graphene.Field(InstitutionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['INSTITUTION'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
            # raise GraphQLError('Name is a required field')
        if input.location is None:
            error += "Location is a required field<br />"
            # raise GraphQLError('Location is a required field')
        if input.city is None:
            error += "City is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)

        searchField = input.name
        searchField += input.location if input.location is not None else ""
        searchField += input.city if input.city is not None else ""
        searchField += input.website if input.website is not None else ""
        searchField += input.bio if input.bio is not None else ""
        searchField = searchField.lower()

        institution_instance = Institution(name=input.name, location=input.location, city=input.city,
                                           website=input.website, phone=input.phone, logo=input.logo, bio=input.bio, searchField=searchField)
        institution_instance.save()

        payload = {"institution": institution_instance,
                   "method": CREATE_METHOD}
        NotifyInstitution.broadcast(
            payload=payload)

        return CreateInstitution(ok=ok, institution=institution_instance)


class UpdateInstitution(graphene.Mutation):
    class Meta:
        description = "Mutation to update an Institution"

    class Arguments:
        id = graphene.ID(required=True)
        input = InstitutionInput(required=True)

    ok = graphene.Boolean()
    institution = graphene.Field(InstitutionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['INSTITUTION'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        institution = Institution.objects.get(pk=id, active=True)
        institution_instance = institution
        if institution_instance:
            ok = True
            institution_instance.name = input.name if input.name is not None else institution.name
            institution_instance.location = input.location if input.location is not None else institution.location
            institution_instance.city = input.city if input.city is not None else institution.city
            institution_instance.website = input.website if input.website is not None else institution.website
            institution_instance.phone = input.phone if input.phone is not None else institution.phone
            institution_instance.logo = input.logo if input.logo is not None else institution.logo
            institution_instance.bio = input.bio if input.bio is not None else institution.bio

            searchField = institution_instance.name if institution_instance.name is not None else ""
            searchField += institution_instance.location if institution_instance.location is not None else ""
            searchField += institution_instance.city if institution_instance.city is not None else ""
            searchField += institution_instance.website if institution_instance.website is not None else ""
            searchField += institution_instance.bio if institution_instance.bio is not None else ""

            institution_instance.searchField = searchField.lower()

            institution_instance.save()
            payload = {"institution": institution_instance,
                       "method": UPDATE_METHOD}
            NotifyInstitution.broadcast(
                payload=payload)
            return UpdateInstitution(ok=ok, institution=institution_instance)
        return UpdateInstitution(ok=ok, institution=None)


class DeleteInstitution(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Institution as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    institution = graphene.Field(InstitutionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['INSTITUTION'], ACTIONS['DELETE']))
    def mutate(root, info, id, input=None):
        ok = False
        institution = Institution.objects.get(pk=id, active=True)
        institution_instance = institution
        if institution_instance:
            ok = True
            institution_instance.active = False

            institution_instance.save()
            payload = {"institution": institution_instance,
                       "method": DELETE_METHOD}
            NotifyInstitution.broadcast(
                payload=payload)
            return DeleteInstitution(ok=ok, institution=institution_instance)
        return DeleteInstitution(ok=ok, institution=None)


class VerifyInvitecode(graphene.Mutation):
    class Meta:
        descriptioin = "Mutation to add the invitecode that the user used to register"

    class Arguments:
        invitecode = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, invitecode, input=None):
        ok = False
        institution = Institution.objects.get(
            invitecode=invitecode, active=True)
        if institution:
            ok = True
            return VerifyInvitecode(ok=ok)
        else:
            return VerifyInvitecode(ok=ok)


class AddInvitecode(graphene.Mutation):
    class Meta:
        descriptioin = "Mutation to add the invitecode that the user used to register"

    class Arguments:
        invitecode = graphene.String(required=True)
        email = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, invitecode, email, input=None):
        ok = False
        institution = Institution.objects.get(
            invitecode=invitecode, active=True)
        institution_instance = institution
        if institution_instance is None:
            raise GraphQLError(
                "You've provided an invalid invitation code. Please check and try again.")
        user_instance = User.objects.get(email=email, active=True)
        if user_instance and institution_instance:
            ok = True
            user_instance.invitecode = invitecode
            user_instance.save()
        return AddInvitecode(ok=ok,)


# class CreateUser(graphene.Mutation):
#     class Meta:
#         description = "Mutation to create a new User"

#     class Arguments:
#         user = UserInput(required=True)

#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)

#     @staticmethod
#     @login_required
#     def mutate(root, info, input=None):
#         ok = True
#         error = ""

#         searchField = input.first_name + \
#             input.last_name if input.first_name and input.last_name else ""
#         searchField += input.title if input.title is not None else ""
#         searchField += input.bio if input.bio is not None else ""
#         searchField = searchField.lower()

#         user_instance = User(user_id=input.user_id, title=input.title, bio=input.bio,
#                              institution_id=input.institution_id, searchField=searchField)
#         user_instance.save()

#         payload = {"user": user_instance,
#                    "method": CREATE_METHOD}
#         NotifyUser.broadcast(
#             payload=payload)
#         return CreateUser(ok=ok, user=user_instance)


class UpdateUser(graphene.Mutation):
    class Meta:
        description = "Mutation to update a User"

    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        ok = False
        current_user = info.context.user
        user = User.objects.get(pk=current_user.id, active=True)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.first_name = input.first_name if input.first_name is not None else user.first_name
            user_instance.last_name = input.last_name if input.last_name is not None else user.last_name
            user_instance.avatar = input.avatar if input.avatar is not None else user.avatar
            user_instance.institution_id = input.institution_id if input.institution_id is not None else user.institution_id
            user_instance.role_id = input.role_id if input.role_id is not None else user.role_id
            user_instance.title = input.title if input.title is not None else user.title
            user_instance.bio = input.bio if input.bio is not None else user.bio

            # Updatiing the membership status to Pending if the user is currently Uninitialized and
            # they provide first name, last name and institution to set up their profile
            if user_instance.membership_status == 'UI':
                if len(user_instance.first_name) > 0 and len(user_instance.last_name) > 0 and user_instance.institution_id is not None:
                    user_instance.membership_status = 'PE'

            searchField = user_instance.first_name if user_instance.first_name is not None else ""
            searchField += user_instance.last_name if user_instance.last_name is not None else ""
            searchField += user_instance.title if user_instance.title is not None else ""
            searchField += user_instance.bio if user_instance.bio is not None else ""
            user_instance.searchField = searchField.lower()

            user_instance.save()

            payload = {"user": user_instance,
                       "method": UPDATE_METHOD}
            NotifyUser.broadcast(
                payload=payload)

            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class DeleteUser(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a User as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        ok = False
        user = User.objects.get(pk=id, active=True)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.active = False

            user_instance.save()
            payload = {"user": user_instance,
                       "method": DELETE_METHOD}
            NotifyUser.broadcast(
                payload=payload)
            return DeleteUser(ok=ok, user=user_instance)
        return DeleteUser(ok=ok, user=None)


class ApproveUser(graphene.Mutation):
    class Meta:
        description = "Mutation to approve user"

    class Arguments:
        user_id = graphene.ID(required=True)
        role_name = graphene.ID(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['MODERATION'], ACTIONS['UPDATE']))
    def mutate(root, info, user_id, role_name):
        ok = False
        user = User.objects.get(pk=user_id, active=True)
        user_instance = user
        role = UserRole.objects.get(pk=role_name, active=True)
        if user_instance and role:
            ok = True
            user_instance.role = role
            user_instance.membership_status = 'AP'

            user_instance.save()
            payload = {"user": user_instance,
                       "method": DELETE_METHOD}
            NotifyUser.broadcast(
                payload=payload)
            return ApproveUser(ok=ok, user=user_instance)
        return ApproveUser(ok=ok, user=None)


class SuspendUser(graphene.Mutation):
    class Meta:
        description = "Mutation to suspend user"

    class Arguments:
        user_id = graphene.ID(required=True)
        remarks = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['MODERATION'], ACTIONS['UPDATE']))
    def mutate(root, info, user_id, remarks):
        ok = False
        user = User.objects.get(pk=user_id, active=True)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.bio = remarks
            user_instance.membership_status = 'SU'

            user_instance.save()
            payload = {"user": user_instance,
                       "method": UPDATE_METHOD}
            NotifyUser.broadcast(
                payload=payload)
            return SuspendUser(ok=ok, user=user_instance)
        return SuspendUser(ok=ok, user=None)


class CreateUserRole(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new User Role"

    class Arguments:
        input = UserRoleInput(required=True)

    ok = graphene.Boolean()
    user_role = graphene.Field(UserRoleType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['USER_ROLE'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.permissions is None:
            error += "permissions is a required field<br />"
        if input.priority is None:
            error += "priority is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.name
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        user_role_instance = UserRole(name=input.name, description=input.description,
                                      permissions=input.permissions, priority=input.priority, searchField=searchField)
        user_role_instance.save()

        payload = {"user_role": user_role_instance,
                   "method": CREATE_METHOD}
        NotifyUserRole.broadcast(
            payload=payload)
        return CreateUserRole(ok=ok, user_role=user_role_instance)


class UpdateUserRole(graphene.Mutation):
    class Meta:
        description = "Mutation to update a User Role"

    class Arguments:
        role_name = graphene.ID(required=True)
        input = UserRoleInput(required=True)

    ok = graphene.Boolean()
    user_role = graphene.Field(UserRoleType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['USER_ROLE'], ACTIONS['UPDATE']))
    def mutate(root, info, role_name, input=None):
        ok = False
        user_role_instance = UserRole.objects.get(pk=role_name, active=True)
        if user_role_instance:
            ok = True
            user_role_instance.name = input.name if input.name is not None else user_role_instance.name
            user_role_instance.description = input.description if input.description is not None else user_role_instance.description
            user_role_instance.permissions = input.permissions if input.permissions is not None else user_role_instance.permissions
            user_role_instance.priority = input.priority if input.priority is not None else user_role_instance.priority

            searchField = input.name
            searchField += input.description if input.description is not None else ""
            searchField = searchField.lower()

            user_role_instance.save()
            payload = {"user_role": user_role_instance,
                       "method": UPDATE_METHOD}
            NotifyUserRole.broadcast(
                payload=payload)
            return UpdateUserRole(ok=ok, user_role=user_role_instance)
        return UpdateUserRole(ok=ok, user_role=None)


class DeleteUserRole(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a User Role as inactive"

    class Arguments:
        role_name = graphene.ID(required=True)

    ok = graphene.Boolean()
    user_role = graphene.Field(UserRoleType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['USER_ROLE'], ACTIONS['DELETE']))
    def mutate(root, info, role_name):
        ok = False
        user_role_instance = UserRole.objects.get(pk=role_name, active=True)
        if user_role_instance:
            ok = True
            user_role_instance.active = False

            user_role_instance.save()
            payload = {"user_role": user_role_instance,
                       "method": DELETE_METHOD}
            NotifyUserRole.broadcast(
                payload=payload)
            return DeleteUserRole(ok=ok, user_role=user_role_instance)
        return DeleteUserRole(ok=ok, user_role=None)


class CreateGroup(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Group"

    class Arguments:
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        current_user = info.context.user
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.institution_id is None:
            error += "institution is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.name

        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        group_instance = Group(name=input.name, avatar=input.avatar, description=input.description,
                               institution_id=input.institution_id, searchField=searchField)
        group_instance.save()

        if input.member_ids is not None:
            group_instance.members.add(*input.member_ids)
        if input.admin_ids is not None:
            group_instance.admins.add(*input.admin_ids)

        # Adding the creator of the group as an admin

        group_instance.admins.set([current_user.id])

        # Creating a Group chat automatically

        chat_instance = Chat(
            group=group_instance, chat_type='GP')
        chat_instance.save()

        payload = {"group": group_instance,
                   "method": CREATE_METHOD}
        NotifyGroup.broadcast(
            payload=payload)

        return CreateGroup(ok=ok, group=group_instance)


class UpdateGroup(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Group"

    class Arguments:
        id = graphene.ID(required=True)
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        current_user = info.context.user
        ok = False
        group = Group.objects.get(pk=id, active=True)
        group_instance = group
        if group_instance:
            ok = True
            group_instance.name = input.name if input.name is not None else group.name
            group_instance.description = input.description if input.description is not None else group.description
            group_instance.institution_id = input.institution_id if input.institution_id is not None else group.institution_id
            group_instance.avatar = input.avatar if input.avatar is not None else group.avatar

            searchField = group_instance.name if group_instance.name is not None else ""
            searchField += group_instance.description if group_instance.description is not None else ""
            group_instance.searchField = searchField.lower()

            group_instance.save()

            if input.member_ids is not None:
                group_instance.members.clear()
                group_instance.members.add(*input.member_ids)
            if input.admin_ids is not None:
                group_instance.admins.clear()
                group_instance.admins.add(*input.admin_ids)

            # Adding the creator of the group as an admin
            group_instance.admins.set([current_user.id])
            payload = {"group": group_instance,
                       "method": UPDATE_METHOD}
            NotifyGroup.broadcast(
                payload=payload)
            return UpdateGroup(ok=ok, group=group_instance)
        return UpdateGroup(ok=ok, group=None)


class DeleteGroup(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a Group as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        group = Group.objects.get(pk=id, active=True)
        group_instance = group
        if group_instance:
            ok = True
            group_instance.active = False
            chat_instance = Chat.objects.get(
                group=group_instance.id, active=True)
            if chat_instance:
                chat_instance.active = False
                chat_instance.save()

            group_instance.save()

            payload = {"group": group_instance,
                       "method": DELETE_METHOD}
            NotifyGroup.broadcast(
                payload=payload)

            return DeleteGroup(ok=ok, group=group_instance)
        return DeleteGroup(ok=ok, group=None)


class CreateAnnouncement(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Announcement"

    class Arguments:
        input = AnnouncementInput(required=True)

    ok = graphene.Boolean()
    announcement = graphene.Field(AnnouncementType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        current_user = info.context.user
        ok = True
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.author_id is None:
            error += "Author is a required field<br />"
        if input.message is None:
            error += "Message is a required field<br />"
        if input.group_ids is None:
            error += "Group(s) is a required field<br />"
        if input.institution_id is None:
            error += "Institution is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.message if input.message is not None else ""
        searchField = searchField.lower()

        announcement_instance = Announcement(title=input.title, author_id=input.author_id, message=input.message,
                                             institution_id=input.institution_id, searchField=searchField)
        announcement_instance.save()

        if input.group_ids is not None:
            announcement_instance.groups.add(*input.group_ids)

        payload = {"announcement": announcement_instance,
                   "method": CREATE_METHOD}
        NotifyAnnouncement.broadcast(
            payload=payload)

        return CreateAnnouncement(ok=ok, announcement=announcement_instance)


class UpdateAnnouncement(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Announcement"

    class Arguments:
        id = graphene.ID(required=True)
        input = AnnouncementInput(required=True)

    ok = graphene.Boolean()
    announcement = graphene.Field(AnnouncementType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        announcement = Announcement.objects.get(pk=id, active=True)
        announcement_instance = announcement
        if announcement_instance:
            ok = True
            announcement_instance.title = input.title if input.title is not None else announcement.title
            announcement_instance.author_id = input.author if input.author is not None else announcement.author
            announcement_instance.institution_id = input.institution_id if input.institution_id is not None else announcement.institution_id

            searchField = input.title
            searchField += input.message if input.message is not None else ""
            announcement_instance.searchField = searchField.lower()

            announcement_instance.save()

            if input.group_ids is not None:
                announcement_instance.groups.clear()
                announcement_instance.groups.add(*input.group_ids)

            payload = {"announcement": announcement_instance,
                       "method": UPDATE_METHOD}
            NotifyAnnouncement.broadcast(
                payload=payload)
            return UpdateAnnouncement(ok=ok, announcement=announcement_instance)
        return UpdateAnnouncement(ok=ok, announcement=None)


class DeleteAnnouncement(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Announcement as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    announcement = graphene.Field(AnnouncementType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['DELETE']))
    def mutate(root, info, id, input=None):
        ok = False
        announcement = Announcement.objects.get(pk=id, active=True)
        announcement_instance = announcement
        if announcement_instance:
            ok = True
            announcement_instance.active = False

            announcement_instance.save()
            payload = {"announcement": announcement_instance,
                       "method": DELETE_METHOD}
            NotifyAnnouncement.broadcast(
                payload=payload)
            return DeleteAnnouncement(ok=ok, announcement=announcement_instance)
        return DeleteAnnouncement(ok=ok, announcement=None)


class CreateCourse(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Course"

    class Arguments:
        input = CourseInput(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.blurb is None:
            error += "Blurb is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.instructor_id is None:
            error += "Instructor is a required field<br />"
        if input.institution_ids is None:
            error += "Institution(s) is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.blurb if input.blurb is not None else ""
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        course_instance = Course(title=input.title, blurb=input.blurb, description=input.description,
                                 instructor_id=input.instructor_id, start_date=input.start_date, end_date=input.end_date, credit_hours=input.credit_hours, searchField=searchField)
        course_instance.save()

        if input.institution_ids is not None:
            course_instance.institutions.add(*input.institution_ids)

        if input.participant_ids is not None:
            course_instance.participants.add(*input.participant_ids)

        if input.mandatory_prerequisite_ids is not None:
            course_instance.mandatory_prerequisites.add(
                *input.mandatory_prerequisite_ids)

        if input.recommended_prerequisite_ids is not None:
            course_instance.recommended_prerequisites.add(
                *input.recommended_prerequisite_ids)

        payload = {"course": course_instance,
                   "method": CREATE_METHOD}
        NotifyCourse.broadcast(
            payload=payload)

        return CreateCourse(ok=ok, course=course_instance)


class UpdateCourse(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Course"

    class Arguments:
        id = graphene.ID(required=True)
        input = CourseInput(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        course = Course.objects.get(pk=id, active=True)
        course_instance = course
        if course_instance:
            ok = True
            course_instance.title = input.title if input.title is not None else course.title
            course_instance.blurb = input.blurb if input.blurb is not None else course.blurb
            course_instance.description = input.description if input.description is not None else course.description
            course_instance.instructor_id = input.instructor_id if input.instructor_id is not None else course.instructor_id
            course_instance.start_date = input.start_date if input.start_date is not None else course.start_date
            course_instance.end_date = input.end_date if input.end_date is not None else course.end_date
            course_instance.credit_hours = input.credit_hours if input.credit_hours is not None else course.credit_hours

            searchField = input.title
            searchField += input.blurb if input.blurb is not None else ""
            searchField += input.description if input.description is not None else ""
            searchField = searchField.lower()

            course_instance.save()

            if input.institution_ids is not None:
                course_instance.institutions.clear()
                course_instance.institutions.add(*input.institution_ids)

            if input.participant_ids is not None:
                course_instance.participants.clear()
                course_instance.participants.add(*input.participant_ids)

            if input.mandatory_prerequisite_ids is not None:
                course_instance.mandatory_prerequisites.clear()
                course_instance.mandatory_prerequisites.add(
                    *input.mandatory_prerequisite_ids)

            if input.recommended_prerequisite_ids is not None:
                course_instance.recommended_prerequisites.clear()
                course_instance.recommended_prerequisites.add(
                    *input.recommended_prerequisite_ids)

            payload = {"course": course_instance,
                       "method": UPDATE_METHOD}
            NotifyCourse.broadcast(
                payload=payload)

            return UpdateCourse(ok=ok, course=course_instance)
        return UpdateCourse(ok=ok, course=None)


class DeleteCourse(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Course as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['DELETE']))
    def mutate(root, info, id, input=None):
        ok = False
        course = Course.objects.get(pk=id, active=True)
        course_instance = course
        if course_instance:
            ok = True
            course_instance.active = False

            course_instance.save()

            payload = {"course": course_instance,
                       "method": DELETE_METHOD}
            NotifyCourse.broadcast(
                payload=payload)

            return DeleteCourse(ok=ok, course=course_instance)
        return DeleteCourse(ok=ok, course=None)


class CreateChapter(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Chapter"

    class Arguments:
        input = ChapterInput(required=True)

    ok = graphene.Boolean()
    chapter = graphene.Field(ChapterType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.instructions is None:
            error += "Instructions is a required field<br />"
        if input.course_id is None:
            error += "Course is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.instructions if input.instructions is not None else ""
        searchField = searchField.lower()

        chapter_instance = Chapter(title=input.title, instructions=input.instructions,
                                   course_id=input.course_id, section_id=input.section_id, due_date=input.due_date, points=input.points, searchField=searchField)
        chapter_instance.save()

        if input.prerequisite_ids is not None:
            chapter_instance.prerequisites.add(
                *input.prerequisite_ids)

        payload = {"chapter": chapter_instance,
                   "method": CREATE_METHOD}
        NotifyChapter.broadcast(
            payload=payload)

        return CreateChapter(ok=ok, chapter=chapter_instance)


class UpdateChapter(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Chapter"

    class Arguments:
        id = graphene.ID(required=True)
        input = ChapterInput(required=True)

    ok = graphene.Boolean()
    chapter = graphene.Field(ChapterType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        chapter = Chapter.objects.get(pk=id, active=True)
        chapter_instance = chapter
        if chapter_instance:
            ok = True
            chapter_instance.title = input.title if input.title is not None else chapter.title
            chapter_instance.instructions = input.instructions if input.instructions is not None else chapter.instructions
            chapter_instance.course_id = input.course_id if input.course_id is not None else chapter.course_id
            chapter_instance.section_id = input.section_id if input.section_id is not None else chapter.section_id
            chapter_instance.due_date = input.due_date if input.due_date is not None else chapter.due_date
            chapter_instance.points = input.points if input.points is not None else chapter.points

            searchField = input.title
            searchField += input.instructions if input.instructions is not None else ""
            chapter_instance.searchField = searchField.lower()

            chapter_instance.save()

            if input.prerequisite_ids is not None:
                chapter.prerequisites.clear()
                chapter_instance.prerequisites.add(
                    *input.prerequisite_ids)

            payload = {"chapter": chapter_instance,
                       "method": UPDATE_METHOD}
            NotifyChapter.broadcast(
                payload=payload)
            return UpdateChapter(ok=ok, chapter=chapter_instance)
        return UpdateChapter(ok=ok, chapter=None)


class DeleteChapter(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Chapter as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    chapter = graphene.Field(ChapterType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        chapter = Chapter.objects.get(pk=id, active=True)
        chapter_instance = chapter
        if chapter_instance:
            ok = True
            chapter_instance.active = False

            chapter_instance.save()

            payload = {"chapter": chapter_instance,
                       "method": DELETE_METHOD}
            NotifyChapter.broadcast(
                payload=payload)

            return DeleteChapter(ok=ok, chapter=chapter_instance)
        return DeleteChapter(ok=ok, chapter=None)


class ChatWithMember(graphene.Mutation):

    class Meta:
        description = "Mutation to get into a Chat"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    chat = graphene.Field(ChatType)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        ok = True
        current_user = info.context.user
        member = User.objects.get(pk=id)
        print('current_user => ', current_user, 'member => ', member)
        if member is None:
            print('There is no member with id ', id, 'member =>', member)
            return ChatWithMember(ok=False, chat=None)
        try:
            first_possibility = Chat.objects.get(
                individual_member_one=current_user.id, individual_member_two=member.id)
            return ChatWithMember(ok=ok, chat=first_possibility)
        except Chat.DoesNotExist:
            try:
                second_possibility = Chat.objects.get(
                    individual_member_one=member.id, individual_member_two=current_user.id)
                return ChatWithMember(ok=ok, chat=second_possibility)
            except:
                pass

            chat_instance = Chat(
                individual_member_one=current_user, individual_member_two=member)
            chat_instance.save()

            return ChatWithMember(ok=ok, chat=chat_instance)


class DeleteChat(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Chat as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    chat = graphene.Field(ChatType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        chat = Chat.objects.get(pk=id, active=True)
        chat_instance = chat
        if chat_instance:
            ok = True
            chat_instance.active = False

            chat_instance.save()

            payload = {"chat": chat_instance,
                       "method": DELETE_METHOD}
            NotifyChat.broadcast(
                payload=payload)

            return DeleteChat(ok=ok, chat=chat_instance)
        return DeleteChat(ok=ok, chat=None)


class CreateChatMessage(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new ChatMessage"

    class Arguments:
        chat = graphene.ID(required=True)
        message = graphene.String(required=True)
        author = graphene.ID(required=True)

    ok = graphene.Boolean()
    chat_message = graphene.Field(ChatMessageType)

    @staticmethod
    @login_required
    def mutate(root, info, chat, message, author):
        author_instance = User.objects.get(pk=author)
        ok = True
        chat_message_instance = ChatMessage(
            chat_id=chat, message=message, author=author_instance)
        chat_message_instance.save()

        payload = {"chat_message": chat_message_instance,
                   "method": CREATE_METHOD}
        NotifyChatMessage.broadcast(
            payload=payload)

        return CreateChatMessage(ok=ok, chat_message=chat_message_instance)


class UpdateChatMessage(graphene.Mutation):
    class Meta:
        description = "Mutation to update a ChatMessage"

    class Arguments:
        id = graphene.ID(required=True)
        input = ChatMessageInput(required=True)

    ok = graphene.Boolean()
    chat_message = graphene.Field(ChatMessageType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        ok = False
        chat_message = ChatMessage.objects.get(pk=id, active=True)
        chat_message_instance = chat_message
        if chat_message_instance:
            ok = True
            chat_message_instance.message = input.message if input.messagae is not None else chat_message_instance.message
            searchField = chat_message_instance.message
            chat_message_instance.searchField = searchField.lower()

            chat_message_instance.save()

            payload = {"chat_message": chat_message_instance,
                       "method": UPDATE_METHOD}
            NotifyChatMessage.broadcast(
                payload=payload)

            return UpdateChatMessage(ok=ok, chat_message=chat_message_instance)
        return UpdateChatMessage(ok=ok, chat_message=None)


class DeleteChatMessage(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an ChatMessage as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    chat_message = graphene.Field(ChatMessageType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        chat_message = ChatMessage.objects.get(pk=id, active=True)
        chat_message_instance = chat_message
        if chat_message_instance:
            ok = True
            chat_message_instance.active = False

            chat_message_instance.save()

            payload = {"chat_": chat_message_instance,
                       "method": DELETE_METHOD}
            NotifyChatMessage.broadcast(
                payload=payload)

            return DeleteChatMessage(ok=ok, chat_message=chat_message_instance)
        return DeleteChatMessage(ok=ok, chat_message=None)


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()

    add_invitecode = AddInvitecode.Field()
    verify_invitecode = VerifyInvitecode.Field()

    # create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    approve_user = ApproveUser.Field()
    suspend_user = SuspendUser.Field()

    create_user_role = CreateUserRole.Field()
    update_user_role = UpdateUserRole.Field()
    delete_user_role = DeleteUserRole.Field()

    create_group = CreateGroup.Field()
    update_group = UpdateGroup.Field()
    delete_group = DeleteGroup.Field()

    create_announcement = CreateAnnouncement.Field()
    update_announcement = UpdateAnnouncement.Field()
    delete_announcement = DeleteAnnouncement.Field()

    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()

    create_chapter = CreateChapter.Field()
    update_chapter = UpdateChapter.Field()
    delete_chapter = DeleteChapter.Field()

    delete_chat = DeleteChat.Field()
    chat_with_member = ChatWithMember.Field()

    create_chat_message = CreateChatMessage.Field()
    update_chat_message = UpdateChatMessage.Field()
    delete_chat_message = DeleteChatMessage.Field()
