import graphene
from graphql import GraphQLError
from vidhya.models import User, UserRole, Institution, Group, Announcement, Course, Assignment, Chat, ChatMessage
from graphql_jwt.decorators import login_required
from .gqTypes import AnnouncementInput, AnnouncementType, AnnouncementType, AssignmentInput, AssignmentType, CourseInput, CourseType, GroupInput, InstitutionInput,  InstitutionType, UserInput, UserRoleInput,  UserType, UserRoleType, GroupType, ChatType, ChatInput, ChatMessageType, ChatMessageInput


class CreateInstitution(graphene.Mutation):
    class Meta:
        description = "Mutation to create new a Institution"

    class Arguments:
        input = InstitutionInput(required=True)

    ok = graphene.Boolean()
    institution = graphene.Field(InstitutionType)

    @staticmethod
    @login_required
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
    def mutate(root, info, id, input=None):
        ok = False
        institution = Institution.objects.get(pk=id, active=True)
        institution_instance = institution
        if institution_instance:
            ok = True
            institution_instance.active = False

            institution_instance.save()
            return DeleteInstitution(ok=ok, institution=institution_instance)
        return DeleteInstitution(ok=ok, institution=None)


class CreateUser(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new User"

    class Arguments:
        user = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.name
        searchField += input.title if input.title is not None else ""
        searchField += input.bio if input.bio is not None else ""
        searchField = searchField.lower()

        user_instance = User(user_id=input.user_id, title=input.title, bio=input.bio,
                             institution_id=input.institution_id, searchField=searchField)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)


class CreateUserRole(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new User Role"

    class Arguments:
        input = UserRoleInput(required=True)

    ok = graphene.Boolean()
    user_role = graphene.Field(UserRoleType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.permissions is None:
            error += "permissions is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.name
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        user_role_instance = UserRole(name=input.name, description=input.description,
                                      permissions=input.permissions, searchField=searchField)
        user_role_instance.save()
        return CreateUserRole(ok=ok, user_role=user_role_instance)


class UpdateUserRole(graphene.Mutation):
    class Meta:
        description = "Mutation to update a User"

    class Arguments:
        id = graphene.ID(required=True)
        input = UserRoleInput(required=True)

    ok = graphene.Boolean()
    user_role = graphene.Field(UserRoleType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        ok = False
        user_role_instance = UserRole.objects.get(pk=id, active=True)
        if user_role_instance:
            ok = True
            user_role_instance.name = input.name if input.name is not None else user_role_instance.name
            user_role_instance.description = input.description if input.description is not None else user_role_instance.description
            user_role_instance.permissions = input.permissions if input.permissions is not None else user_role_instance.permissions

            searchField = input.name
            searchField += input.description if input.description is not None else ""
            searchField = searchField.lower()

            user_role_instance.save()
            return UpdateUserRole(ok=ok, user_role=user_role_instance)
        return UpdateUserRole(ok=ok, user_role=None)


class DeleteUserRole(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a User Role as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    user_role = graphene.Field(UserRoleType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_role_instance = UserRole.objects.get(pk=id, active=True)
        if user_role_instance:
            ok = True
            user_role_instance.active = False

            user_role_instance.save()
            return DeleteUserRole(ok=ok, user_role=user_role_instance)
        return DeleteUserRole(ok=ok, user_role=None)


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
        return AddInvitecode(ok=ok,)


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
    def mutate(root, info, id, input=None):
        ok = False
        user = User.objects.get(pk=id, active=True)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.active = False

            user_instance.save()
            return DeleteUser(ok=ok, user=user_instance)
        return DeleteUser(ok=ok, user=None)


class CreateGroup(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Group"

    class Arguments:
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    @login_required
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

        group_instance = Group(name=input.name, description=input.description,
                               institution_id=input.institution_id, searchField=searchField)
        group_instance.save()

        if input.members is not None:
            group_instance.members.add(*input.members)
        if input.admins is not None:
            group_instance.admins.add(*input.admins)

        # Adding the creator of the group as an admin
        group_instance.admins.set([current_user.id])

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

            searchField = group_instance.name if group_instance.name is not None else ""
            searchField += group_instance.description if group_instance.description is not None else ""
            group_instance.searchField = searchField.lower()

            group_instance.save()

            if input.members is not None:
                group_instance.members.clear()
                group_instance.members.add(*input.members)
            if input.admins is not None:
                group_instance.admins.clear()
                group_instance.admins.add(*input.admins)

            # Adding the creator of the group as an admin
            group_instance.admins.set([current_user.id])

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
    def mutate(root, info, id, input=None):
        ok = False
        group = Group.objects.get(pk=id, active=True)
        group_instance = group
        if group_instance:
            ok = True
            group_instance.active = False

            group_instance.save()
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

        if input.groups is not None:
            announcement_instance.groups.add(*input.group_ids)

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
    def mutate(root, info, id, input=None):
        ok = False
        announcement = Announcement.objects.get(pk=id, active=True)
        announcement_instance = announcement
        if announcement_instance:
            ok = True
            announcement_instance.active = False

            announcement_instance.save()
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
    def mutate(root, info, input=None):
        ok = True
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.instructor_id is None:
            error += "Instructor is a required field<br />"
        if input.institution_ids is None:
            error += "Institution(s) is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        course_instance = Course(title=input.title, description=input.description,
                                 instructor_id=input.instructor_id, searchField=searchField)
        course_instance.save()

        if input.institution_ids is not None:
            course_instance.institutions.add(*input.institution_ids)

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
    def mutate(root, info, id, input=None):
        ok = False
        course = Course.objects.get(pk=id, active=True)
        course_instance = course
        if course_instance:
            ok = True
            course_instance.title = input.title if input.title is not None else course.title
            course_instance.description = input.description if input.description is not None else course.description
            course_instance.instructor_id = input.instructor_id if input.instructor_id is not None else course.instructor_id

            searchField = input.title
            searchField += input.description if input.description is not None else ""
            course_instance.searchField = searchField.lower()

            course_instance.save()

            if input.institution_ids is not None:
                course_instance.institutions.clear()
                course_instance.institutions.add(*input.institution_ids)

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
    def mutate(root, info, id, input=None):
        ok = False
        course = Course.objects.get(pk=id, active=True)
        course_instance = course
        if course_instance:
            ok = True
            course_instance.active = False

            course_instance.save()
            return DeleteCourse(ok=ok, course=course_instance)
        return DeleteCourse(ok=ok, course=None)


class CreateAssignment(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Assignment"

    class Arguments:
        input = AssignmentInput(required=True)

    ok = graphene.Boolean()
    assignment = graphene.Field(AssignmentType)

    @staticmethod
    @login_required
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

        assignment_instance = Assignment(title=input.title, instructions=input.instructions,
                                         course_id=input.course_id, searchField=searchField)
        assignment_instance.save()

        return CreateAssignment(ok=ok, assignment=assignment_instance)


class UpdateAssignment(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Assignment"

    class Arguments:
        id = graphene.ID(required=True)
        input = AssignmentInput(required=True)

    ok = graphene.Boolean()
    assignment = graphene.Field(AssignmentType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        ok = False
        assignment = Assignment.objects.get(pk=id, active=True)
        assignment_instance = assignment
        if assignment_instance:
            ok = True
            assignment_instance.title = input.title if input.title is not None else assignment.title
            assignment_instance.instructions = input.instructions if input.instructions is not None else assignment.instructions
            assignment_instance.course_id = input.course_id if input.course_id is not None else assignment.course_id

            searchField = input.title
            searchField += input.instructions if input.instructions is not None else ""
            assignment_instance.searchField = searchField.lower()

            assignment_instance.save()

            return UpdateAssignment(ok=ok, assignment=assignment_instance)
        return UpdateAssignment(ok=ok, assignment=None)


class DeleteAssignment(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Assignment as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    assignment = graphene.Field(AssignmentType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        assignment = Assignment.objects.get(pk=id, active=True)
        assignment_instance = assignment
        if assignment_instance:
            ok = True
            assignment_instance.active = False

            assignment_instance.save()
            return DeleteAssignment(ok=ok, assignment=assignment_instance)
        return DeleteAssignment(ok=ok, assignment=None)


class CreateChat(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Chat"

    class Arguments:
        input = ChatInput(required=True)

    ok = graphene.Boolean()
    chat = graphene.Field(ChatType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        current_user = info.context.user
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.name
        searchField = searchField.lower()

        chat_instance = Chat(name=input.name,
                             searchField=searchField)
        chat_instance.save()

        if input.member_ids is not None:
            chat_instance.members.clear()
            chat_instance.members.add(*input.member_ids)

        if input.admin_ids is not None:
            chat_instance.admins.clear()
            chat_instance.admins.add(*input.admin_ids)

        # Adding the creator of the group as an admin
        chat_instance.admins.set([current_user.id])

        return CreateChat(ok=ok, chat=chat_instance)


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
        if member is None:
            return ChatWithMember(ok=False, chat=None)
        if Chat.objects.filter(
                members__in=[current_user.id, member.id]).exists():
            chat_members = Chat.objects.filter(
                members__in=[current_user.id, member.id])
            existing_chat_instance = Chat.objects.get(
                pk=chat_members[0].id)
            if existing_chat_instance is not None:
                return ChatWithMember(ok=ok, chat=existing_chat_instance)

        chat_instance = Chat()
        chat_instance.save()

        # Adding the creator of the chat and the member
        chat_instance.members.set([current_user.id, id])
        return ChatWithMember(ok=ok, chat=chat_instance)


class UpdateChat(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Chat"

    class Arguments:
        id = graphene.ID(required=True)
        input = ChatInput(required=True)

    ok = graphene.Boolean()
    chat = graphene.Field(ChatType)

    @staticmethod
    @login_required
    def mutate(root, info, id, input=None):
        ok = False
        chat = Chat.objects.get(pk=id, active=True)
        chat_instance = chat
        if chat_instance:
            ok = True
            chat_instance.name = input.name if input.name is not None else chat.name

            searchField = input.name
            chat_instance.searchField = searchField.lower()

            chat_instance.save()

            if input.member_ids is not None:
                chat_instance.members.clear()
                chat_instance.members.add(*input.member_ids)

            if input.admin_ids is not None:
                chat_instance.admins.clear()
                chat_instance.admins.add(*input.admin_ids)

            return UpdateChat(ok=ok, chat=chat_instance)
        return UpdateChat(ok=ok, chat=None)


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
            chat_message_instance.name = input.name if input.name is not None else chat_message.name

            searchField = input.name
            chat_message_instance.searchField = searchField.lower()

            chat_message_instance.save()

            if input.member_ids is not None:
                chat_message_instance.members.clear()
                chat_message_instance.members.add(*input.member_ids)

            if input.admin_ids is not None:
                chat_message_instance.admins.clear()
                chat_message_instance.admins.add(*input.admin_ids)

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
            return DeleteChatMessage(ok=ok, chat_message=chat_message_instance)
        return DeleteChatMessage(ok=ok, chat_message=None)


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()

    add_invitecode = AddInvitecode.Field()
    verify_invitecode = VerifyInvitecode.Field()

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

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

    create_assignment = CreateAssignment.Field()
    update_assignment = UpdateAssignment.Field()
    delete_assignment = DeleteAssignment.Field()

    create_chat = CreateChat.Field()
    update_chat = UpdateChat.Field()
    delete_chat = DeleteChat.Field()
    chat_with_member = ChatWithMember.Field()

    create_chat_message = CreateChatMessage.Field()
    update_chat_message = UpdateChatMessage.Field()
    delete_chat_message = DeleteChatMessage.Field()
