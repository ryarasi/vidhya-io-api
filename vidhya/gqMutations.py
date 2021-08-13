import graphene
from graphql import GraphQLError
from vidhya.models import User, UserRole, Institution, Group, Announcement, Course, CourseSection, Chapter, Exercise, ExerciseKey, ExerciseSubmission, Report, Chat, ChatMessage
from graphql_jwt.decorators import login_required, user_passes_test
from .gqTypes import AnnouncementInput, AnnouncementType, AnnouncementType, CourseType, CourseSectionType,  ChapterType, ExerciseSubmissionInput, ExerciseType, ExerciseKeyType, ExerciseSubmissionType, ReportType, GroupInput, InstitutionInput,  InstitutionType, UserInput, UserRoleInput,  UserType, UserRoleType, GroupType, CourseInput, CourseSectionInput, ChapterInput, ExerciseInput, ExerciseKeyInput, ExerciseSubmissionInput, ReportInput, ChatType, ChatMessageType, ChatMessageInput
from .gqSubscriptions import NotifyInstitution, NotifyUser, NotifyUserRole, NotifyGroup, NotifyAnnouncement, NotifyCourse, NotifyCourseSection, NotifyChapter, NotifyExercise, NotifyExerciseKey, NotifyExerciseSubmission, NotifyReport, NotifyChat, NotifyChatMessage
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
        role_name = graphene.String(required=True)

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
        role_name = graphene.String(required=True)
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
        if input.status is None:
            error += "Status is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.blurb if input.blurb is not None else ""
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        course_instance = Course(title=input.title, blurb=input.blurb, description=input.description,
                                 instructor_id=input.instructor_id, start_date=input.start_date, end_date=input.end_date, credit_hours=input.credit_hours, status=input.status, searchField=searchField)
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
            course_instance.status = input.status if input.status is not None else course.status

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


class PublishCourse(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Course as published"

    class Arguments:
        id = graphene.ID(required=True)
        publish_chapters = graphene.Boolean(required=True)

    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['UPDATE']))
    def mutate(root, info, id, publish_chapters):
        ok = False
        course = Course.objects.get(pk=id, active=True)
        course_instance = course
        if course_instance:
            ok = True
            course_instance.status = Course.StatusChoices.PUBLISHED
            print('id', id, 'publish_chapters', publish_chapters)
            if publish_chapters==True:
                chapters = Chapter.objects.filter(course=id, active=True)
                for chapter in chapters:
                    chapter.status = Chapter.StatusChoices.PUBLISHED
                    chapter.save()
                # write method to loop through chapters and mark them as published
                pass

            course_instance.save()

            payload = {"course": course_instance,
                       "method": UPDATE_METHOD}
            NotifyCourse.broadcast(
                payload=payload)

            return PublishCourse(ok=ok, course=course_instance)
        return PublishCourse(ok=ok, course=None)


class CreateCourseSection(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new Course Section"

    class Arguments:
        input = CourseSectionInput(required=True)

    ok = graphene.Boolean()
    course_section = graphene.Field(CourseSectionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.course_id is None:
            error += "Course is a required field<br />"

        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField = searchField.lower()

        course_section_instance = CourseSection(title=input.title, index=input.index, course_id=input.course_id,
                                                searchField=searchField)
        course_section_instance.save()

        payload = {"course_section": course_section_instance,
                   "method": CREATE_METHOD}
        NotifyCourseSection.broadcast(
            payload=payload)
        return CreateCourseSection(ok=ok, course_section=course_section_instance)


class UpdateCourseSection(graphene.Mutation):
    class Meta:
        description = "Mutation to update a CourseSection"

    class Arguments:
        id = graphene.ID(required=True)
        input = CourseSectionInput(required=True)

    ok = graphene.Boolean()
    course_section = graphene.Field(CourseSectionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        course_section_instance = CourseSection.objects.get(
            pk=id, active=True)
        if course_section_instance:
            ok = True
            course_section_instance.title = input.title if input.title is not None else course_section_instance.title
            course_section_instance.index = input.index if input.index is not None else course_section_instance.index
            course_section_instance.course_id = input.course_id if input.course_id is not None else course_section_instance.course_id

            searchField = input.title
            searchField = searchField.lower()

            course_section_instance.save()
            payload = {"course_section": course_section_instance,
                       "method": UPDATE_METHOD}
            NotifyCourseSection.broadcast(
                payload=payload)
            return UpdateCourseSection(ok=ok, course_section=course_section_instance)
        return UpdateCourseSection(ok=ok, course_section=None)


class DeleteCourseSection(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a CourseSection as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    course_section = graphene.Field(CourseSectionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        course_section_instance = CourseSection.objects.get(
            pk=id, active=True)
        if course_section_instance:
            ok = True
            course_section_instance.active = False

            course_section_instance.save()
            payload = {"course_section": course_section_instance,
                       "method": DELETE_METHOD}
            NotifyCourseSection.broadcast(
                payload=payload)
            return DeleteCourseSection(ok=ok, course_section=course_section_instance)
        return DeleteCourseSection(ok=ok, course_section=None)


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
        if input.status is None:
            error += "Status is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.instructions if input.instructions is not None else ""
        searchField = searchField.lower()

        chapter_instance = Chapter(title=input.title, instructions=input.instructions,
                                   course_id=input.course_id, section_id=input.section_id, due_date=input.due_date, points=input.points, status= input.status, searchField=searchField)
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
            chapter_instance.status = input.status if input.status is not None else chapter.status

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

class PublishChapter(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Chapter as published"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    chapter = graphene.Field(ChapterType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    def mutate(root, info, id):
        ok = False
        chapter = Chapter.objects.get(pk=id, active=True)
        chapter_instance = chapter
        if chapter_instance:
            ok = True
            chapter_instance.status = Chapter.StatusChoices.PUBLISHED

            chapter_instance.save()

            payload = {"chapter": chapter_instance,
                       "method": UPDATE_METHOD}
            NotifyChapter.broadcast(
                payload=payload)

            return PublishChapter(ok=ok, chapter=chapter_instance)
        return PublishChapter(ok=ok, chapter=None)



class CreateExercise(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new Exercise"

    class Arguments:
        input = ExerciseInput(required=True)

    ok = graphene.Boolean()
    exercise = graphene.Field(ExerciseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.prompt is None:
            error += "Prompt is a required field<br />"
        if input.chapter_id is None:
            error += "Chapter is a required field<br />"
        if input.course_id is None:
            error += "Course is a required field<br />"            
        if input.question_type is None:
            error += "Question type is a required field<br />"
        else:
            if input.question_type == Exercise.QuestionTypeChoices.OPTIONS:
                if input.valid_option is None:
                    error += "A valid option key is required"
            if input.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
                if len(input.valid_answers) == 0:
                    error += "A valid answer key is required"
            if input.question_type == Exercise.QuestionTypeChoices.IMAGE:
                if len(input.reference_images) == 0:
                    error += "At least one valid reference image is required"
            if input.question_type ==  Exercise.QuestionTypeChoices.LINK:
                if input.reference_link is None:
                    error += "A valid link key is required"                                                            
        if input.required is None:
            error += "Required is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.prompt
        searchField = searchField.lower()

        exercise_instance = Exercise(prompt=input.prompt, course_id=input.course_id, chapter_id=input.chapter_id,
                                     question_type=input.question_type, required=input.required, options=input.options, points=input.points, searchField=searchField)
        exercise_instance.save()

        exercise_key_instance = ExerciseKey(exercise=exercise_instance, course_id=input.course_id, chapter_id=input.chapter_id, valid_option=input.valid_option, valid_answers=input.valid_answers, reference_link = input.reference_link, reference_images = input.reference_images)

        exercise_key_instance.save()

        # Notifying creation of Exercise
        payload = {"exercise": exercise_instance,
                   "method": CREATE_METHOD}
        NotifyExercise.broadcast(
            payload=payload)

        #Notifying creation of Exercise Key
        exercise_key_payload = {"exercise_key": exercise_key_instance,
                   "method": CREATE_METHOD}
        NotifyExerciseKey.broadcast(
            payload=exercise_key_payload)        

        return CreateExercise(ok=ok, exercise=exercise_instance)


class UpdateExercise(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Exercise"

    class Arguments:
        id = graphene.ID(required=True)
        input = ExerciseInput(required=True)

    ok = graphene.Boolean()
    exercise = graphene.Field(ExerciseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        exercise_instance = Exercise.objects.get(pk=id, active=True)
        exercise_key_instance = ExerciseKey.objects.get(exercise=exercise_instance, active=True)
        if exercise_instance and exercise_key_instance:
            ok = True
            exercise_instance.prompt = input.prompt if input.prompt is not None else exercise_instance.prompt
            exercise_instance.chapter_id = input.chapter_id if input.chapter_id is not None else exercise_instance.chapter_id
            exercise_instance.course_id = input.course_id if input.course_id is not None else exercise_instance.course_id
            exercise_instance.question_type = input.question_type if input.question_type is not None else exercise_instance.question_type
            exercise_instance.required = input.required if input.required is not None else exercise_instance.required
            exercise_instance.options = input.options if input.options is not None else exercise_instance.options
            exercise_instance.points = input.points if input.points is not None else exercise_instance.points

            searchField = input.prompt
            exercise_instance.searchField = searchField.lower()

            exercise_instance.save()

            # Notifying updating of Exercise
            payload = {"exercise": exercise_instance,
                       "method": UPDATE_METHOD}
            NotifyExercise.broadcast(
                payload=payload)

            exercise_key_instance.valid_option = input.valid_option if input.valid_option is not None else exercise_key_instance.valid_option
            exercise_key_instance.valid_answers = input.valid_answers if input.valid_answers is not None else exercise_key_instance.valid_answers
            exercise_key_instance.reference_link = input.reference_link if input.reference_link is not None else exercise_key_instance.reference_link
            exercise_key_instance.reference_images = input.reference_images if input.reference_images is not None else exercise_key_instance.reference_images
         
            exercise_key_instance.save()
            payload = {"exercise_key": exercise_key_instance,
                       "method": UPDATE_METHOD}
            NotifyExerciseKey.broadcast(
                payload=payload)            


            return UpdateExercise(ok=ok, exercise=exercise_instance)            
        return UpdateExercise(ok=ok, exercise=None)


class DeleteExercise(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a Exercise as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    exercise = graphene.Field(ExerciseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        exercise_instance = Exercise.objects.get(pk=id, active=True)
        if exercise_instance:
            ok = True
            exercise_instance.active = False

            exercise_instance.save()
            payload = {"exercise": exercise_instance,
                       "method": DELETE_METHOD}
            NotifyExercise.broadcast(
                payload=payload)
            return DeleteExercise(ok=ok, exercise=exercise_instance)
        return DeleteExercise(ok=ok, exercise=None)


# class UpdateExerciseKey(graphene.Mutation):
#     class Meta:
#         description = "Mutation to update a Exercise Key"

#     class Arguments:
#         id = graphene.ID(required=True)
#         input = ExerciseKeyInput(required=True)

#     ok = graphene.Boolean()
#     exercise_key = graphene.Field(ExerciseKeyType)

    # @staticmethod
    # @login_required
    # @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    # def mutate(root, info, id, input=None):
    #     ok = False
    #     exercise_key_instance = ExerciseKey.objects.get(pk=id, active=True)
    #     if exercise_key_instance:
    #         ok = True
    #         exercise_key_instance.exercise = input.exercise if input.exercise is not None else exercise_key_instance.exercise
    #         exercise_key_instance.valid_option = input.valid_option if input.valid_option is not None else exercise_key_instance.valid_option
    #         exercise_key_instance.valid_answers = input.valid_answers if input.valid_answers is not None else exercise_key_instance.valid_answers
    #         exercise_key_instance.reference_link = input.reference_link if input.reference_link is not None else exercise_key_instance.reference_link
    #         exercise_key_instance.reference_images = input.reference_images if input.reference_images is not None else exercise_key_instance.reference_images
         
    #         exercise_key_instance.save()
    #         payload = {"exercise_key": exercise_key_instance,
    #                    "method": UPDATE_METHOD}
    #         NotifyExerciseKey.broadcast(
    #             payload=payload)
    #         return UpdateExerciseKey(ok=ok, exercise_key=exercise_key_instance)
    #     return UpdateExerciseKey(ok=ok, exercise_key=None)


class CreateExerciseSubmissions(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new ExerciseSubmission"

    class Arguments:
        exercise_submissions = graphene.List(ExerciseSubmissionInput, required=True)

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['CREATE']))
    def mutate(root, info, exercise_submissions=None):
        ok = False
        error = ""
        for submission in exercise_submissions:
            exercise_instance = Exercise.objects.get(pk=submission.exercise_id, active=True)
            if submission.exercise_id is None:
                error += "Exercise is a required field<br />"
            if submission.chapter_id is None:
                error += "Chapter is a required field<br />"
            if submission.course_id is None:
                error += "Course is a required field<br />"            
            if exercise_instance.question_type is None:
                error += "Question type is a required field<br />"
            if exercise_instance.required == True:
                if exercise_instance.question_type == Exercise.QuestionTypeChoices.OPTIONS:
                    if submission.option is None:
                        error += "A valid option is required"
                if exercise_instance.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
                    if len(submission.answer) == 0:
                        error += "A valid answer is required"
                if exercise_instance.question_type == Exercise.QuestionTypeChoices.IMAGE:
                    if len(submission.images) == 0:
                        error += "At least one image is required"
                if exercise_instance.question_type ==  Exercise.QuestionTypeChoices.LINK:
                    if submission.link is None:
                        error += "A link is required"    
            if len(error) > 0:
                raise GraphQLError(error)
        for submission in exercise_submissions:
            ok = True
            exercise = Exercise.objects.get(pk=submission.exercise_id, active=True)
            exercise_key = ExerciseKey.objects.get(exercise=exercise, active=True)
            searchField = submission.option if submission.option is not None else ""
            searchField += submission.answer if submission.answer is not None else ""
            searchField += submission.link if submission.link is not None else ""
            searchField = searchField.lower()
            status = ExerciseSubmission.StatusChoices.SUBMITTED
            points = None
            if exercise.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
                if submission.answer in exercise_key.valid_answers:
                    points = exercise.points
                    status = ExerciseSubmission.StatusChoices['GRADED']
            if exercise.question_type == Exercise.QuestionTypeChoices.OPTIONS:
                if submission.option == exercise_key.valid_option:
                    points = exercise.points
                    status = ExerciseSubmission.StatusChoices.GRADED

            exercise_submission_instance = ExerciseSubmission(exercise_id=submission.exercise_id, course_id=submission.course_id, chapter_id=submission.chapter_id, participant_id=submission.participant_id, option=submission.option,
                                                            answer=submission.answer, link=submission.link, images=submission.images, points=points, status=status, searchField=searchField)
            exercise_submission_instance.save()

            payload = {"exercise_submission": exercise_submission_instance,
                    "method": CREATE_METHOD}
            NotifyExerciseSubmission.broadcast(
                payload=payload)
        return CreateExerciseSubmissions(ok=ok)


class UpdateExerciseSubmission(graphene.Mutation):
    class Meta:
        description = "Mutation to update a ExerciseSubmission"

    class Arguments:
        id = graphene.ID(required=True)
        input = ExerciseSubmissionInput(required=True)

    ok = graphene.Boolean()
    exercise_submission = graphene.Field(ExerciseSubmissionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        exercise_submission_instance = ExerciseSubmission.objects.get(
            pk=id, active=True)
        if exercise_submission_instance:
            ok = True
            exercise_submission_instance.exercise_id = input.exercise_id if input.exercise_id is not None else exercise_submission_instance.exercise_id
            exercise_submission_instance.course_id = input.course_id if input.course_id is not None else exercise_submission_instance.course_id
            exercise_submission_instance.chapter_id = input.chapter_id if input.chapter_id is not None else exercise_submission_instance.chapter_id
            exercise_submission_instance.option = input.option if input.option is not None else exercise_submission_instance.option
            exercise_submission_instance.answer = input.answer if input.answer is not None else exercise_submission_instance.answer
            exercise_submission_instance.link = input.link if input.link is not None else exercise_submission_instance.link
            exercise_submission_instance.images = input.images if input.images is not None else exercise_submission_instance.images
            exercise_submission_instance.points = input.points if input.points is not None else exercise_submission_instance.points
            exercise_submission_instance.status = input.status if input.status is not None else exercise_submission_instance.status

            searchField = input.option
            searchField += input.answer if input.answer is not None else ""
            searchField += input.link if input.link is not None else ""
            exercise_submission_instance.searchField = searchField.lower()

            exercise_submission_instance.save()
            payload = {"exercise_submission": exercise_submission_instance,
                       "method": UPDATE_METHOD}
            NotifyExerciseSubmission.broadcast(
                payload=payload)
            return UpdateExerciseSubmission(ok=ok, exercise_submission=exercise_submission_instance)
        return UpdateExerciseSubmission(ok=ok, exercise_submission=None)


class DeleteExerciseSubmission(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a ExerciseSubmission as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    exercise_submission = graphene.Field(ExerciseSubmissionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        exercise_submission_instance = ExerciseSubmission.objects.get(
            pk=id, active=True)
        if exercise_submission_instance:
            ok = True
            exercise_submission_instance.active = False

            exercise_submission_instance.save()
            payload = {"exercise_submission": exercise_submission_instance,
                       "method": DELETE_METHOD}
            NotifyExerciseSubmission.broadcast(
                payload=payload)
            return DeleteExerciseSubmission(ok=ok, exercise_submission=exercise_submission_instance)
        return DeleteExerciseSubmission(ok=ok, exercise_submission=None)


class CreateReport(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new Report"

    class Arguments:
        input = ReportInput(required=True)

    ok = graphene.Boolean()
    report = graphene.Field(ReportType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.participant_id is None:
            error += "Participant is a required field<br />"
        if input.course_id is None:
            error += "Course is a required field<br />"
        if input.completed is None:
            error += "Completed is a required field<br />"
        if input.score is None:
            error += "Score is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = ""
        searchField = searchField.lower()

        report_instance = Report(participant_id=input.participant_id, course_id=input.course_id,
                                 completed=input.completed, score=input.score, searchField=searchField)
        report_instance.save()

        payload = {"report": report_instance,
                   "method": CREATE_METHOD}
        NotifyReport.broadcast(
            payload=payload)
        return CreateReport(ok=ok, report=report_instance)


class UpdateReport(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Report"

    class Arguments:
        id = graphene.ID(required=True)
        input = ReportInput(required=True)

    ok = graphene.Boolean()
    report = graphene.Field(ReportType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        report_instance = Report.objects.get(pk=id, active=True)
        if report_instance:
            ok = True
            report_instance.participant_id = input.participant_id if input.participant_id is not None else report_instance.participant_id
            report_instance.course_id = input.course_id if input.course_id is not None else report_instance.course_id
            report_instance.completed = input.completed if input.completed is not None else report_instance.completed
            report_instance.score = input.score if input.score is not None else report_instance.score

            searchField = ""
            report_instance.searchField = searchField.lower()

            report_instance.save()
            payload = {"report": report_instance,
                       "method": UPDATE_METHOD}
            NotifyReport.broadcast(
                payload=payload)
            return UpdateReport(ok=ok, report=report_instance)
        return UpdateReport(ok=ok, report=None)


class DeleteReport(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a Report as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    report = graphene.Field(ReportType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        report_instance = Report.objects.get(pk=id, active=True)
        if report_instance:
            ok = True
            report_instance.active = False

            report_instance.save()
            payload = {"report": report_instance,
                       "method": DELETE_METHOD}
            NotifyReport.broadcast(
                payload=payload)
            return DeleteReport(ok=ok, report=report_instance)
        return DeleteReport(ok=ok, report=None)


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
    publish_course = PublishCourse.Field()

    create_chapter = CreateChapter.Field()
    update_chapter = UpdateChapter.Field()
    delete_chapter = DeleteChapter.Field()
    publish_chapter = PublishChapter.Field()

    create_exercise = CreateExercise.Field()
    update_exercise = UpdateExercise.Field()
    delete_exercise = DeleteExercise.Field()

    create_exercise_submissions = CreateExerciseSubmissions.Field()

    delete_chat = DeleteChat.Field()
    chat_with_member = ChatWithMember.Field()

    create_chat_message = CreateChatMessage.Field()
    update_chat_message = UpdateChatMessage.Field()
    delete_chat_message = DeleteChatMessage.Field()
