from enum import unique
import json
from typing import final

from django.db.models.query_utils import Q
import graphene
import graphql_social_auth
from graphql import GraphQLError
from vidhya.models import CompletedChapters, CourseGrader, Criterion, CriterionResponse, EmailOTP, Issue, Project, ProjectClap, SubmissionHistory, User, UserRole, Institution, Group, Announcement, Course, CourseSection, Chapter, Exercise, ExerciseKey, ExerciseSubmission, Report, Chat, ChatMessage
from graphql_jwt.decorators import login_required, user_passes_test
from .gqTypes import AnnouncementType, AnnouncementInput, CourseType, CourseSectionType,  ChapterType, CriterionInput, CriterionResponseInput, CriterionResponseType, CriterionType, ExerciseSubmissionInput, ExerciseType, ExerciseKeyType, ExerciseSubmissionType, IndexListInputType, IssueInput, IssueType, ProjectInput, ProjectType, ReportType, GroupInput, InstitutionInput,  InstitutionType, UserInput, UserRoleInput,  UserType, UserRoleType, GroupType, CourseInput, CourseSectionInput, ChapterInput, ExerciseInput, ExerciseKeyInput, ExerciseSubmissionInput, ReportInput, ChatType, ChatMessageType, ChatMessageInput, verifyEmailUser
from .gqSubscriptions import NotifyCriterion, NotifyCriterionResponse, NotifyInstitution, NotifyIssue, NotifyProject, NotifyUser, NotifyUserRole, NotifyGroup, NotifyAnnouncement, NotifyCourse, NotifyCourseSection, NotifyChapter, NotifyExercise, NotifyExerciseKey, NotifyExerciseSubmission, NotifyReport, NotifyChat, NotifyChatMessage
from vidhya.authorization import has_access, RESOURCES, ACTIONS, CREATE_METHOD, UPDATE_METHOD, DELETE_METHOD, is_admin_user
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import URLValidator, ValidationError
from common.utils import generate_otp
from .cache import announcements_modified, chapters_modified, courses_modified, exercise_submission_graded, exercise_submission_submitted, groups_modified, institutions_modified, project_clapped, projects_modified, public_announcements_modified, user_announcements_modified, user_roles_modified, users_modified
from django.core.cache import cache
from django.db import connection,transaction
from graphql_jwt.shortcuts import get_token,create_refresh_token
from django.contrib.auth import get_user_model

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
        if input.code is None:
            error += "Code is a required field<br />"            
        if input.location is None:
            error += "Location is a required field<br />"
        if input.city is None:
            error += "City is a required field<br />"
        if error:
            raise GraphQLError(error)

        searchField = input.name
        searchField += input.code if input.code is not None else ""
        searchField += input.location if input.location is not None else ""
        searchField += input.city if input.city is not None else ""
        searchField += input.website if input.website is not None else ""
        searchField += input.bio if input.bio is not None else ""
        searchField = searchField.lower()

        institution_instance = Institution(name=input.name, code=input.code, location=input.location, city=input.city,
                                           website=input.website, phone=input.phone, logo=input.logo, bio=input.bio, searchField=searchField)
        institution_instance.save()

        payload = {"institution": institution_instance,
                   "method": CREATE_METHOD}
        NotifyInstitution.broadcast(
            payload=payload)

        institutions_modified() # Invalidating the cache for institutions

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
            institution_instance.code = input.code if input.code is not None else institution.code
            institution_instance.location = input.location if input.location is not None else institution.location
            institution_instance.city = input.city if input.city is not None else institution.city
            institution_instance.website = input.website if input.website is not None else institution.website
            institution_instance.phone = input.phone if input.phone is not None else institution.phone
            institution_instance.logo = input.logo if input.logo is not None else institution.logo
            institution_instance.bio = input.bio if input.bio is not None else institution.bio

            searchField = institution_instance.name if institution_instance.name is not None else ""
            searchField = institution_instance.code if institution_instance.code is not None else ""
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

            institutions_modified() # Invalidating the cache for institutions


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
                
            institutions_modified() # Invalidating the cache for institutions

            return DeleteInstitution(ok=ok, institution=institution_instance)
        return DeleteInstitution(ok=ok, institution=None)


class VerifyInvitecode(graphene.Mutation):
    class Meta:
        description = "Mutation to add the invitecode that the user used to register"

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

class GenerateEmailOTP(graphene.Mutation):
    class Meta:
        description = "Mutation to generate email OTP and save it to the database"

    class Arguments:
        email = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def check_email_verified(email=None):
        email_verified = False # Variable to check whether the provided email is already verified        
        try:
            # Checking whether the email has been veriied previously, by searching or a record with the same email and 'True' in verified column
            verified_email = EmailOTP.objects.get(email=email, verified=True).exists()
            # if the record exists, we mark the verified_email field as true
            if verified_email:
                email_verified=True
        except:
            pass
    
        return email_verified

    @staticmethod
    def check_if_email_otp_exists(email=None):
        email_otp = False
        try:
            email_otp = EmailOTP.objects.get(email=email)
        except:
            email_otp = EmailOTP(email=email)
        return email_otp

    @staticmethod
    def send_email_otp(email):
        email_otp = EmailOTP.objects.get(email=email)
        send_mail(
            'Your email verification code',
            'Dear user,\n\nThe code for verifying your email ID is as follows\n\n' + email_otp.otp + '\n\nPlease do not reply to this email.',
            settings.DEFAULT_FROM_EMAIL,
            [email_otp.email],
            fail_silently=False,
        )

    @staticmethod
    def mutate(root, info, email=None):
        ok = False
        if email is None:
            ok = False
        else:
            email_verified = GenerateEmailOTP.check_email_verified()

            # If the email was previously verified, we simply mark ok as true and return the result to the user
            if email_verified:
                ok = True
                
            else:
                email_otp = GenerateEmailOTP.check_if_email_otp_exists(email)
                email_otp.otp = generate_otp()
                email_otp.save()
                # Once the record is saved, we send the OTP to the email ID
                GenerateEmailOTP.send_email_otp(email)
            
                ok = True        

        return GenerateEmailOTP(ok=ok)

class VerifyEmailOTP(graphene.Mutation):
    class Meta:
        description = "Mutation to verify the OTP sent to their email"

    class Arguments:
        email = graphene.String(required=True)
        otp = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, email=None, otp=None):
        ok = False
        record = None
        if email and otp:
            try:
                record = EmailOTP.objects.get(email=email,
                    otp=otp)
            except:
               pass
            if record:
                record.verified = True
                record.save()
                ok = True
                
        return VerifyEmailOTP(ok=ok)                

class AddInvitecode(graphene.Mutation):
    class Meta:
        descriptioin = "Mutation to add the invitecode that the user used to register"

    class Arguments:
        invitecode = graphene.String(required=True)
        email = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def removeEmailOtpRecord(email=None):
        EmailOTP.objects.filter(email=email).delete()

    @staticmethod
    def mutate(root, info, invitecode, email, input=None):
        ok = False
        try:
            institution = Institution.objects.get(invitecode=invitecode, active=True)
            user = User.objects.get(email=email, active=True)
            if user and institution:
                ok = True
                user.institution_id = institution.id
                user.save()
                AddInvitecode.removeEmailOtpRecord();
        except:
            raise GraphQLError(
                "There was an error in your registration. Please contact the admin.")

        return AddInvitecode(ok=ok)


# class createUser(graphene.Mutation):
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
#         return createUser(ok=ok, user=user_instance)

# class passwordChange(graphene.Mutation):
#     class Meta:
#         description = "Change Password"

#     class Arguments:
#         input = UserInput(required=True)
    
#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)

#     @staticmethod
#     @login_required
#     def mutate(root, info, input=None):
#         ok = False
#         current_user = info.context.user
#         user = User.objects.get(pk=current_user.id, active=True)
#         user_instance = user

#         if user_instance:
#             ok = True
#             user_instance.password = input.password if input.password is not None else user.password
#             user_instance.save()
        
#             users_modified() # Invalidating users cache

#             payload = {"user": user_instance,
#                         "method": UPDATE_METHOD}
#             NotifyUser.broadcast(
#                 payload=payload)

#             return passwordChange(ok=ok, user=user_instance)
#         return passwordChange(ok=ok, user=None)

class verifyEmailUser(graphene.Mutation):
    class Meta:
        description = "Verify Email Account"

        
    class Arguments:
        user_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info,user_id, input=None):
        ok = False
        user = get_user_model().objects.get(pk=user_id)
        user_instance = user
        if user_instance:
            ok = True
            if(user_instance.status.verified == False):
                user_instance.status.verified = True
                user_instance.status.save()
                return verifyEmailUser(ok=ok, user=user_instance)
        return verifyEmailUser(ok=ok, user=None)

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
            user_instance.name = user_instance.first_name + ' ' + user_instance.last_name if user_instance.first_name is not None and user_instance.last_name is not None else ""
            user_instance.avatar = input.avatar if input.avatar is not None else user.avatar
            user_instance.institution_id = input.institution_id if input.institution_id is not None else user.institution_id
            user_instance.role_id = input.role_id if input.role_id is not None else user.role_id
            user_instance.title = input.title if input.title is not None else user.title
            user_instance.bio = input.bio if input.bio is not None else user.bio
            user_instance.mobileno = input.mobileno if input.mobileno is not None else user.mobileno
            user_instance.phoneno = input.phoneno if input.phoneno is not None else user.phoneno
            user_instance.address = input.address if input.address is not None else user.address
            user_instance.dob = input.dob if input.dob is not None else user.dob
            user_instance.institutiontype = input.institutiontype if input.institutiontype is not None else user.institutiontype
            user_instance.year = input.year if input.year is not None else user.year
            user_instance.schoolorcollege = input.year if input.schoolorcollege is not None else user.schoolorcollege
            user_instance.courseorclass = input.courseorclass if input.courseorclass is not None else user.courseorclass

            # Updatiing the membership status to Pending if the user is currently Uninitialized and
            # they provide first name, last name and institution to set up their profile
            if user_instance.membership_status == 'UI':
                if user_instance.name and user_instance.institution_id is not None:
                    user_instance.membership_status = 'PE'

            searchField = user_instance.first_name if user_instance.first_name is not None else ""
            searchField += user_instance.last_name if user_instance.last_name is not None else ""
            searchField += user_instance.title if user_instance.title is not None else ""
            searchField += user_instance.bio if user_instance.bio is not None else ""
            searchField += user_instance.membership_status if user_instance.membership_status is not None else ""
            if user_instance.institution:
                searchField += user_instance.institution.name if user_instance.institution.name is not None else ""
            user_instance.searchField = searchField.lower()

            user_instance.save()
        
            users_modified() # Invalidating users cache

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

            users_modified() # Invalidating users cache

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
        current_user = info.context.user
        user = User.objects.get(pk=user_id, active=True)
        user_instance = user
        role = UserRole.objects.get(pk=role_name, active=True)
        if user_instance and role:
            ok = True
            user_instance.role = role
            user_instance.membership_status = 'AP'
            send_mail(
                'Your Vidhya.io account is approved!',
                'Dear '+user_instance.username+',\n\nYour account is now approved!\n\nPlease login with your credentials - '+settings.FRONTEND_DOMAIN_URL+'.\n\nThis approval action was undertaken by ' + current_user.name+ '.\n\nPlease do not reply to this email.',
                settings.DEFAULT_FROM_EMAIL,
                [user_instance.email],
                fail_silently=False,
            )
            user_instance.save()

            users_modified() # Invalidating users cache

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

            users_modified() # Invalidating users cache


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
        if error:
            raise GraphQLError(error)
        searchField = input.name
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        user_role_instance = UserRole(name=input.name, description=input.description,
                                      permissions=input.permissions, priority=input.priority, searchField=searchField)
        user_role_instance.save()

        user_roles_modified() # Invalidating User roles cache

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

            user_roles_modified() # Invalidating User roles cache

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

            user_roles_modified() # Invalidating User roles cache

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

    def validate_group(input):
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.institution_id is None:
            error += "Institution is a required field<br />"
        if not input.admin_ids:
            error += "The group needs at least one admin<br />"
        if error:
            raise GraphQLError(error)    

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['GROUP'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        CreateGroup.validate_group(input)
        searchField = input.name

        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        group_instance = Group(name=input.name, avatar=input.avatar, description=input.description, group_type=input.group_type,
                               institution_id=input.institution_id, searchField=searchField)
        group_instance.save()

        groups_modified() # Invalidating groups cache

        if input.member_ids:
            group_instance.members.add(*input.member_ids)
        if input.admin_ids:
            group_instance.admins.add(*input.admin_ids)

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
        CreateGroup.validate_group(input)
        group = Group.objects.get(pk=id, active=True)
        group_instance = group
        if group_instance:
            ok = True
            group_instance.name = input.name if input.name is not None else group.name
            group_instance.description = input.description if input.description is not None else group.description
            group_instance.institution_id = input.institution_id if input.institution_id is not None else group.institution_id
            group_instance.avatar = input.avatar if input.avatar is not None else group.avatar
            group_instance.group_type = input.group_type if input.group_type is not None else group.group_type
            searchField = group_instance.name if group_instance.name is not None else ""
            searchField += group_instance.description if group_instance.description is not None else ""
            group_instance.searchField = searchField.lower()

            group_instance.save()

            groups_modified() # Invalidating groups cache

            if input.member_ids:
                group_instance.members.clear()
                group_instance.members.add(*input.member_ids)
            if input.admin_ids:
                group_instance.admins.clear()
                group_instance.admins.add(*input.admin_ids)

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

            groups_modified() # Invalidating groups cache

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

    def validate_announcement(input):
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.author_id is None:
            error += "Author is a required field<br />"
        if input.message is None:
            error += "Message is a required field<br />"
        if  not input.recipients_global and not input.recipients_institution and not input.group_ids and not input.public:
            error += "Recipients is a required field<br />"
        if input.institution_id is None:
            error += "Institution is a required field<br />"
        if error:
            raise GraphQLError(error)


    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        current_user = info.context.user
        CreateAnnouncement.validate_announcement(input)
        ok = True
        searchField = input.title
        searchField += input.message if input.message is not None else ""
        searchField = searchField.lower()

        if input.group_ids:
            input.recipients_global = False
            input.recipients_institution = False
        
        if input.recipients_institution == True:
            input.recipients_global = False
        
        public = False # By default all announcements are private
        if input.public == True:
            admin_user = is_admin_user(current_user)
            if admin_user:
                # They can be public only when the creator is an admin user
                public = True

        announcement_instance = Announcement(title=input.title, author_id=input.author_id, public=public, image=input.image, blurb=input.blurb, message=input.message,
                                             institution_id=input.institution_id, recipients_global=input.recipients_global, recipients_institution=input.recipients_institution, searchField=searchField)
        announcement_instance.save()

        # Cache invalidation

        announcements_modified(announcement_instance) # Invalidate announcements cache

        if input.group_ids:
            announcement_instance.groups.add(*input.group_ids)

        current_user.announcements.add(announcement_instance.id)

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

    def increment_views(id):
        announcement_instance = Announcement.objects.get(pk=id, active=True)
        announcement_instance.views = announcement_instance.views + 1;
        announcement_instance.save()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        CreateAnnouncement.validate_announcement(input)
        ok = False
        announcement = Announcement.objects.get(pk=id, active=True)
        announcement_instance = announcement
        if announcement_instance:
            ok = True
            announcement_instance.title = input.title if input.title is not None else announcement.title
            announcement_instance.image = input.image if input.image is not None else announcement.image
            announcement_instance.blurb = input.blurb if input.blurb is not None else announcement.blurb
            announcement_instance.message = input.message if input.message is not None else announcement.message
            announcement_instance.author_id = input.author if input.author is not None else announcement.author
            announcement_instance.institution_id = input.institution_id if input.institution_id is not None else announcement.institution_id

            public = False # By default all announcements are private
            if input.public == True:
                admin_user = is_admin_user(info.context.user)
                if admin_user:
                    # They can be public only when the creator is an admin user
                    public = True

            announcement_instance.public = public


            searchField = input.title
            searchField += input.message if input.message is not None else ""
            announcement_instance.searchField = searchField.lower()

            announcement_instance.save()

            # Cache invalidation
            
            announcements_modified(announcement_instance) # Invalidate announcements cache

            if input.group_ids or input.group_ids == []:
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

            # Cache invalidation
            
            announcements_modified(announcement_instance) # Invalidate announcements cache

            payload = {"announcement": announcement_instance,
                       "method": DELETE_METHOD}
            NotifyAnnouncement.broadcast(
                payload=payload)
            return DeleteAnnouncement(ok=ok, announcement=announcement_instance)
        return DeleteAnnouncement(ok=ok, announcement=None)

class MarkAnnouncementsSeen(graphene.Mutation):

    class Meta:
        description = "Mutation to mark all announcements as seen"

    class Arguments:
        pass

    announcements = graphene.List(AnnouncementType)
    ok = graphene.Boolean()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ANNOUNCEMENT'], ACTIONS['LIST']))
    def mutate(root, info,):
        ok = False
        try:
            announcements = Announcement.objects.all()
            current_user = info.context.user
            for announcement in announcements:
                current_user.announcements.add(announcement.id)
            ok = True
        except:
            ok = False

        # Invalidating cache
        
        user_announcements_modified(current_user) # Invalidating user specific announcements
        
        return MarkAnnouncementsSeen(ok=ok, announcements=announcements)

class CreateProject(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Project"

    class Arguments:
        input = ProjectInput(required=True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    def validate_project(input):
        error = ""
        if input.title is None:
            error += "Title is a required field<br />"
        if input.author_id is None:
            error += "Author is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.public is None:
            error += "Public is a required field<br />"

        if input.link:
            try:
                validator = URLValidator()
                validator(input.link)
            except ValidationError:                
                error += "Link should be a valid URL<br />"            
        if error:
            raise GraphQLError(error)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['PROJECT'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        current_user = info.context.user
        ok = True
        CreateProject.validate_project(input)
        searchField = input.title
        searchField += input.description if input.description is not None else ""
        searchField += current_user.name if current_user.name is not None else ""
        searchField = searchField.lower()

        project_instance = Project(title=input.title, author_id=input.author_id, link =input.link, public=input.public, description=input.description, course_id=input.course_id,
                                              searchField=searchField)
        project_instance.save()
        current_user.projects_clapped.add(project_instance.id)

        projects_modified() # Invalidate projects cache

        payload = {"project": project_instance,
                   "method": CREATE_METHOD}
        NotifyProject.broadcast(
            payload=payload)

        return CreateProject(ok=ok, project=project_instance)

class ClapProject(graphene.Mutation):
    class Meta:
        description = "Mutation that lets a user clap a project"
    
    class Arguments:
        id = graphene.ID(required=True)
    
    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, id):
        ok = False
        current_user = info.context.user
        project = None
        try:
            project = Project.objects.get(pk=id, active=True)
        except:
            pass
        if project:
            if current_user.id:
                user_already_clapped = ProjectClap.objects.filter(user_id=current_user.id, project_id=project.id).exists()
                if not user_already_clapped:
                    ok=True
                    project.claps = project.claps + 1
                    project.clapsBy.add(current_user)
            else:
                ok=True
                project.claps = project.claps+1
            project.save()
        
        # Invalidating project cache
        project_clapped()
        
        return ClapProject(ok=ok,project=project)
        


class UpdateProject(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Project"

    class Arguments:
        id = graphene.ID(required=True)
        input = ProjectInput(required=True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['PROJECT'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        current_user = info.context.user
        project = Project.objects.get(pk=id, active=True)
        CreateProject.validate_project(input)
        project_instance = project
        if project_instance:
            ok = True
            project_instance.title = input.title if input.title is not None else project.title
            project_instance.author_id = input.author_id if input.author_id is not None else project.author_id
            project_instance.description = input.description if input.description is not None else project.description
            project_instance.link = input.link if input.link is not None else project.link
            project_instance.course_id = input.course_id if input.course_id is not None else project.course_id
            project_instance.public = input.public if input.public is not None else project.public

            searchField = input.title
            searchField += input.description if input.description is not None else ""
            searchField += current_user.name if current_user.name is not None else ""
            searchField = searchField.lower()
            project_instance.searchField = searchField

            project_instance.save()

            projects_modified() # Invalidate projects cache

            payload = {"project": project_instance,
                       "method": UPDATE_METHOD}

            NotifyProject.broadcast(
                payload=payload)

            return UpdateProject(ok=ok, project=project_instance)
        return UpdateProject(ok=ok, project=None)


class DeleteProject(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Project as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['PROJECT'], ACTIONS['DELETE']))
    def mutate(root, info, id, input=None):
        ok = False
        project = Project.objects.get(pk=id, active=True)
        project_instance = project
        if project_instance:
            ok = True
            project_instance.active = False

            project_instance.save()

            projects_modified() # Invalidate projects cache

            payload = {"project": project_instance,
                       "method": DELETE_METHOD}
            NotifyProject.broadcast(
                payload=payload)
            return DeleteProject(ok=ok, project=project_instance)
        return DeleteProject(ok=ok, project=None)


class CreateIssue(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Issue"

    class Arguments:
        input = IssueInput(required=True)

    ok = graphene.Boolean()
    issue = graphene.Field(IssueType)

    def validate_issue(input):
        error = ""
        if input.link is None:
            error += "Link is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if input.resource_type is None:
            error += "Resource type is a required field<br />"
        if input.resource_id is None:
            error += "Resource ID is a required field<br />"
        
        resource = IssueType.get_issue_resource(input)
        if resource is None:
            error += "Unable to find the resource specified here. Please check and try again<br />"

        if input.link:
            try:
                validator = URLValidator()
                validator(input.link)
            except ValidationError:                
                error += "Link should be a valid URL<br />"
                                                     
        if error:
            raise GraphQLError(error)
        else:
            return resource

    def generate_searchField(input):
        author=None
        try:
            if input.reporter_id:
                author=User.objects.get(pk=input.reporter_id, active=True)
        except:
            pass        
        searchField = input.link
        searchField += input.description if input.description is not None else ""
        searchField += input.resource_type if input.resource_type is not None else ""
        searchField += input.remarks if input.remarks is not None else ""
        searchField += input.guest_name if input.guest_name is not None else ""
        searchField += input.status if input.status is not None else ""
        searchField += author.name if author is not None else ""
        searchField = searchField.lower()
        return searchField

    @staticmethod
    def mutate(root, info, input=None):
        ok = True

        resource = CreateIssue.validate_issue(input)
        searchField=CreateIssue.generate_searchField(input)

        institution_id = None
        if input.resource_type == Issue.ResourceTypeChoices.INSTITUTION:
            institution_id = resource.id
        elif input.resource_type == Issue.ResourceTypeChoices.USER:
            institution_id = resource.institution.id
        elif input.resource_type == Issue.ResourceTypeChoices.PROJECT:
            institution_id = resource.author.institution.id
        elif input.resource_type == Issue.ResourceTypeChoices.SUBMISSION:
            institution_id = resource.participant.institution.id

        issue_instance = Issue(link=input.link, description=input.description, resource_id=input.resource_id, institution_id=institution_id, resource_type=input.resource_type, reporter_id=input.reporter_id, guest_name=input.guest_name, guest_email=input.guest_email,screenshot=input.screenshot, status=input.status, remarks=input.remarks, 
                                              searchField=searchField)
        issue_instance.save()

        payload = {"issue": issue_instance,
                   "method": CREATE_METHOD}
        NotifyIssue.broadcast(
            payload=payload)

        return CreateIssue(ok=ok, issue=issue_instance)


class UpdateIssue(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Issue"

    class Arguments:
        id = graphene.ID(required=True)
        input = IssueInput(required=True)

    ok = graphene.Boolean()
    issue = graphene.Field(IssueType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ISSUE'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        
        issue = Issue.objects.get(pk=id, active=True)
        CreateIssue.validate_issue(input)
        issue_instance = issue
        if issue_instance:
            ok = True
            issue_instance.link = input.link if input.link is not None else issue.link
            issue_instance.description = input.description if input.description is not None else issue.description
            issue_instance.resource_id = input.resource_id if input.resource_id is not None else issue.resource_id
            issue_instance.resource_type = input.resource_type if input.resource_type is not None else issue.resource_type
            issue_instance.reporter_id = input.reporter_id if input.reporter_id is not None else issue.reporter_id
            issue_instance.guest_name = input.guest_name if input.guest_name is not None else issue.guest_name
            issue_instance.guest_email = input.guest_email if input.guest_email is not None else issue.guest_email
            issue_instance.screenshot = input.screenshot if input.screenshot is not None else issue.screenshot
            issue_instance.status = input.status if input.status is not None else issue.status
            issue_instance.remarks = input.remarks if input.remarks is not None else issue.remarks

            searchField = CreateIssue.generate_searchField(input)
            issue_instance.searchField = searchField

            issue_instance.save()


            payload = {"issue": issue_instance,
                       "method": UPDATE_METHOD}

            NotifyIssue.broadcast(
                payload=payload)

            return UpdateIssue(ok=ok, issue=issue_instance)
        return UpdateIssue(ok=ok, issue=None)

class UpdateIssueStatus(graphene.Mutation):
    class Meta:
        description = "Mutation to update the status of an Issue"

    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.String(required=True)
        remarks = graphene.String(required=True)

    ok = graphene.Boolean()
    issue = graphene.Field(IssueType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ISSUE'], ACTIONS['UPDATE']))
    def mutate(root, info, id, status=None, remarks=None):
        ok = False
        issue = None
        try:
            issue = Issue.objects.get(pk=id, active=True)
        except:
            raise GraphQLError('Issue not found!')
        issue_instance = issue

        issue.status=status
        issue.resolver_id = info.context.user.id
        issue.remarks = remarks
        issue.save()
        payload = {"issue": issue_instance,
                    "method": UPDATE_METHOD}

        NotifyIssue.broadcast(
            payload=payload)

        return UpdateIssue(ok=ok, issue=issue_instance)

class DeleteIssue(graphene.Mutation):
    class Meta:
        description = "Mutation to mark an Issue as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    issue = graphene.Field(IssueType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['ISSUE'], ACTIONS['DELETE']))
    def mutate(root, info, id, input=None):
        ok = False
        issue = Issue.objects.get(pk=id, active=True)
        issue_instance = issue
        if issue_instance:
            ok = True
            issue_instance.active = False

            issue_instance.save()
            payload = {"issue": issue_instance,
                       "method": DELETE_METHOD}
            NotifyIssue.broadcast(
                payload=payload)
            return DeleteIssue(ok=ok, issue=issue_instance)
        return DeleteIssue(ok=ok, issue=None)

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
        if error:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.blurb if input.blurb is not None else ""
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        course_instance = Course(
                                index=input.index, 
                                blurb=input.blurb, 
                                description=input.description, 
                                video=input.video,
                                instructor_id=input.instructor_id,
                                start_date=input.start_date, 
                                end_date=input.end_date, 
                                credit_hours=input.credit_hours, 
                                pass_score_percentage = input.pass_score_percentage, 
                                pass_completion_percentage = input.pass_completion_percentage, 
                                searchField=searchField)
        course_instance.save()

        courses_modified() # Invalidating course cache

        if input.institution_ids:
            course_instance.institutions.add(*input.institution_ids)

        if input.participant_ids or input.participant_ids == []:
            course_instance.participants.add(*input.participant_ids)

        if input.grader_ids or input.grader_ids == []:
            course_instance.graders.add(*input.grader_ids)            

        if input.mandatory_prerequisite_ids:
            course_instance.mandatory_prerequisites.add(
                *input.mandatory_prerequisite_ids)

        if input.recommended_prerequisite_ids:
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
            course_instance.index = input.index if input.index is not None else course.index
            course_instance.video = input.video if input.video is not None else course.video
            course_instance.blurb = input.blurb if input.blurb is not None else course.blurb
            course_instance.instructor_id = input.instructor_id if input.instructor_id is not None else course.instructor_id
            course_instance.start_date = input.start_date if input.start_date is not None else course.start_date
            course_instance.end_date = input.end_date if input.end_date is not None else course.end_date
            course_instance.credit_hours = input.credit_hours if input.credit_hours is not None else course.credit_hours
            course_instance.pass_score_percentage = input.pass_score_percentage if input.pass_score_percentage is not None else course.pass_score_percentage
            course_instance.pass_completion_percentage = input.pass_completion_percentage if input.pass_completion_percentage is not None else course.pass_completion_percentage
            course_instance.status = input.status if input.status is not None else course.status

            searchField = input.title
            searchField += input.blurb if input.blurb is not None else ""
            searchField += input.description if input.description is not None else ""
            searchField = searchField.lower()

            course_instance.save()

            courses_modified() # Invalidating course cache

            if input.institution_ids or input.institution_ids == []:
                course_instance.institutions.clear()
                course_instance.institutions.add(*input.institution_ids)

            if input.participant_ids or input.participant_ids == []:
                course_instance.participants.clear()
                course_instance.participants.add(*input.participant_ids)

            if input.grader_ids or input.grader_ids == []:
                course_instance.graders.clear()
                course_instance.graders.add(*input.grader_ids)                

            if input.mandatory_prerequisite_ids or input.mandatory_prerequisite_ids == []:
                course_instance.mandatory_prerequisites.clear()
                course_instance.mandatory_prerequisites.add(
                    *input.mandatory_prerequisite_ids)

            if input.recommended_prerequisite_ids or input.recommended_prerequisite_ids == []:
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

            #Deleting chapters in the course
            chapters = Chapter.objects.filter(course_id=id, active=True)
            for chapter in chapters:
                DeleteChapter.mutate(root, info, chapter.id)

            #Deleting course sections in the course
            sections = CourseSection.objects.filter(course_id=id, active=True)
            for section in sections:
                DeleteCourseSection.mutate(root, info, section.id)
                
            course_instance.save()

            courses_modified() # Invalidating course cache

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
            if publish_chapters==True:
                chapters = Chapter.objects.filter(course=id, active=True)
                for chapter in chapters:
                    chapter.status = Chapter.StatusChoices.PUBLISHED
                    chapter.save()
                # write method to loop through chapters and mark them as published
                pass

            course_instance.save()

            courses_modified() # Invalidating course cache

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

        if error:
            raise GraphQLError(error)

        course_section_instance = CourseSection(title=input.title, index=input.index, course_id=input.course_id,
                                                )
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

    def update_points(id=None):
        if id:
            try:
                chapter = Chapter.objects.all().get(pk=id, active=True)
                exercises = Exercise.objects.all().filter(chapter_id=id, active=True)
                chapter.points = 0
                for exercise in exercises:
                    chapter.points += exercise.points
                chapter.save()
            except:
                pass

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
        if error:
            raise GraphQLError(error)
        searchField = input.title
        searchField += input.instructions if input.instructions is not None else ""
        searchField = searchField.lower()

        points = input.points if input.points is not None else 0
        index = input.index if input.index else 100

        chapter_instance = Chapter(title=input.title, index=index, instructions=input.instructions,
                                   course_id=input.course_id, section_id=input.section_id, due_date=input.due_date, points=points, status= input.status, searchField=searchField)
        chapter_instance.save()

        chapters_modified() # Invalidating chapter cache

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
            chapter_instance.index = input.index if input.index is not None else chapter.index
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

            chapters_modified() # Invalidating chapter cache

            if input.prerequisite_ids or input.prerequisite_ids == []:
                chapter_instance.prerequisites.clear()
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

            # Deleting all exercises (and its associated entities such as key, submissions etc.) that are part of this chapter
            exercises = Exercise.objects.filter(chapter_id=id, active=True)
            for exercise in exercises:
                DeleteExercise.mutate(root, info, exercise.id)

            chapter_instance.save()

            chapters_modified() # Invalidating chapter cache

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

            chapters_modified() # Invalidating chapter cache

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

    def validate_exercise_input(input):
        error = ""
        if not input.prompt:
            error += "Prompt is a required field<br />"
          
        if not input.chapter_id:
            error += "Chapter is a required field<br />"
        if not input.course_id:
            error += "Course is a required field<br />"            
        if not input.question_type:
            error += "Question type is a required field<br />"
        else:
            if input.question_type == Exercise.QuestionTypeChoices.OPTIONS:
                if not input.valid_option:
                    error += "A valid option key is required<br />"
            if input.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
                if not input.valid_answers:
                    error += "A valid answer key is required<br />"
            if input.question_type == Exercise.QuestionTypeChoices.IMAGE:
                if not input.reference_images and not input.remarks:
                    error += "Either remarks field or at least one valid reference image is required<br />"
            if input.question_type ==  Exercise.QuestionTypeChoices.LINK:
                if not input.reference_link and not input.remarks:
                    error += "Either remarks or a valid reference link is required<br />"     
                if input.reference_link:
                    try:
                        validator = URLValidator()
                        validator(input.reference_link)
                    except ValidationError:                
                        error += "Link should be a valid URL<br />"
        if input.required is None:
            error += "Please specify if this question is required or not<br />"
        if error:
            raise GraphQLError(error)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        CreateExercise.validate_exercise_input(input)
        searchField = input.prompt
        searchField = searchField.lower()

        points = input.points if input.points is not None else 0
        index = input.index if input.index is not None else 100

        exercise_instance = Exercise(prompt=input.prompt, index=index, course_id=input.course_id, chapter_id=input.chapter_id,
                                     question_type=input.question_type, required=input.required, options=input.options, points=points, searchField=searchField)
        exercise_instance.save()

        # Creating criterion if rubric exists
        if input.rubric:
            for criterion in input.rubric:
                criterion_instance = Criterion(exercise_id= exercise_instance.id, description=criterion.description, points = criterion.points)
                criterion_instance.save()

        CreateChapter.update_points(input.chapter_id) # Updating the points on the chapter

        exercise_key_instance = ExerciseKey(exercise=exercise_instance, course_id=input.course_id, chapter_id=input.chapter_id, valid_option=input.valid_option, valid_answers=input.valid_answers, reference_link = input.reference_link, reference_images = input.reference_images, remarks = input.remarks)

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
        CreateExercise.validate_exercise_input(input)
        exercise_instance = Exercise.objects.get(pk=id, active=True)
        exercise_key_instance = ExerciseKey.objects.get(exercise=exercise_instance, active=True)
        if exercise_instance and exercise_key_instance:
            ok = True
            exercise_instance.prompt = input.prompt if input.prompt is not None else exercise_instance.prompt
            exercise_instance.index = input.index if input.index is not None else exercise_instance.index
            exercise_instance.chapter_id = input.chapter_id if input.chapter_id is not None else exercise_instance.chapter_id
            exercise_instance.course_id = input.course_id if input.course_id is not None else exercise_instance.course_id
            exercise_instance.question_type = input.question_type if input.question_type is not None else exercise_instance.question_type
            exercise_instance.required = input.required if input.required is not None else exercise_instance.required
            exercise_instance.options = input.options if input.options is not None else exercise_instance.options
            exercise_instance.points = input.points if input.points is not None else exercise_instance.points

            if input.rubric:
                for criterion in input.rubric:
                    criterion_new = False
                    if criterion.id:
                        try:
                            criterion_instance = Criterion.objects.get(pk=criterion.id, active=True)
                            criterion_instance.description = criterion.description if criterion.description is not None else criterion_instance.description
                            criterion_instance.points = criterion.points if criterion.points is not None else criterion_instance.points
                            criterion_instance.exercise_id = exercise_instance.id
                            criterion_instance.active = True if criterion.active is None or criterion.active != False else criterion.active
                            criterion_instance.save()
                        except:
                            criterion_new = True
                    elif not criterion.id or criterion_new:
                        criterion_instance = Criterion(description=criterion.description, exercise_id=exercise_instance.id, points=criterion.points)
                        criterion_instance.save()

            searchField = input.prompt
            exercise_instance.searchField = searchField.lower()

            exercise_instance.save()
            CreateChapter.update_points(exercise_instance.chapter_id) # Updating the points on the chapter

            # Notifying updating of Exercise
            payload = {"exercise": exercise_instance,
                       "method": UPDATE_METHOD}
            NotifyExercise.broadcast(
                payload=payload)
            exercise_key_instance.valid_option = input.valid_option if input.valid_option is not None else exercise_key_instance.valid_option
            exercise_key_instance.valid_answers = input.valid_answers if input.valid_answers is not None else exercise_key_instance.valid_answers
            exercise_key_instance.reference_link = input.reference_link if input.reference_link is not None else exercise_key_instance.reference_link
            exercise_key_instance.reference_images = input.reference_images if input.reference_images is not None else exercise_key_instance.reference_images
            exercise_key_instance.remarks = input.remarks if input.remarks is not None else exercise_key_instance.remarks
         
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
        exercise = Exercise.objects.get(pk=id, active=True)
        if exercise:
            ok = True
            exercise.active = False
            exercise.save()

            # Marking the exercise key as inactive as well
            try:
                exercise_key = ExerciseKey.objects.all().get(exercise_id=exercise.id, active=True)
                exercise_key.active = False
                exercise_key.save()
            except:
                pass

            # Marking the criteria for this exercise as inactive
            rubric = Criterion.objects.all().filter(exercise_id=exercise.id, active=True)
            for criterion in rubric:
                criterion.active = False
                criterion.save()

            # Marking the criteria of the submissions for this exercise also as inactive
            submissionRubric = CriterionResponse.objects.all().filter(exercise_id = exercise.id, active=True)
            for criterion in submissionRubric:
                criterion.active = False
                criterion.save()          

            # Marking any submissions of this exercise as inactive
            exercise_submissions = ExerciseSubmission.objects.all().filter(exercise_id=exercise.id, active=True)
            CreateChapter.update_points(exercise.chapter_id) # Updating the points on the chapter
            for submission in exercise_submissions:
                submission.active = False
                submission.save()

            payload = {"exercise": exercise,
                       "method": DELETE_METHOD}
            NotifyExercise.broadcast(
                payload=payload)

            exercise_key_payload = {"exercise_key": exercise_key,
                       "method": DELETE_METHOD}
            NotifyExerciseKey.broadcast(
                payload=exercise_key_payload)                
            return DeleteExercise(ok=ok, exercise=exercise)
        return DeleteExercise(ok=ok, exercise=None)


class CreateCriterion(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new Criterion"

    class Arguments:
        input = CriterionInput(required=True)

    ok = graphene.Boolean()
    criterion = graphene.Field(CriterionType)

    def validate_criterion_input(input):
        error = ""
        if not input.description:
            error += "Description is a required field<br />"
        if not input.exercise_id:
            error += "Exercise is a required field<br />"
        if not input.points:
            error += "Points is a required field<br />"            
        if error:
            raise GraphQLError(error)

    def generate_searchField(criterion):
        searchField = criterion.description if criterion.description is not None else ''
        searchField += str(criterion.points if criterion.points is not None else '')
        searchField = searchField.lower()
        return searchField

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        CreateCriterion.validate_criterion_input(input)


        criterion_instance = Criterion(description=input.description, exercise_id=input.exercise_id, points = input.points)
        criterion_instance.searchField = CreateCriterion.generate_searchField(criterion_instance)
        criterion_instance.save()

        # Notifying creation of Criterion
        payload = {"criterion": criterion_instance,
                   "method": CREATE_METHOD}
        NotifyCriterion.broadcast(
            payload=payload)

        return CreateCriterion(ok=ok, criterion=criterion_instance)


class UpdateCriterion(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Criterion"

    class Arguments:
        id = graphene.ID(required=True)
        input = CriterionInput(required=True)

    ok = graphene.Boolean()
    criterion = graphene.Field(CriterionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        CreateCriterion.validate_criterion_input(input)
        criterion_instance = Criterion.objects.get(pk=id, active=True)
        if criterion_instance:
            ok = True
            criterion_instance.description = input.description if input.description is not None else criterion_instance.description
            criterion_instance.points = input.points if input.points is not None else criterion_instance.points
            criterion_instance.exercise_id = input.exercise_id if input.exercise_id is not None else criterion_instance.exercise_id
            criterion_instance.searchField = CreateCriterion.generate_searchField(criterion_instance)

            criterion_instance.save()

            payload = {"criterion": criterion_instance,
                       "method": UPDATE_METHOD}
            NotifyCriterion.broadcast(
                payload=payload)


            return UpdateCriterion(ok=ok, criterion=criterion_instance)            
        return UpdateCriterion(ok=ok, criterion=None)


class DeleteCriterion(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a Criterion as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    criterion = graphene.Field(CriterionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        criterion = Criterion.objects.get(pk=id, active=True)
        if criterion:
            ok = True
            criterion.active = False
            criterion.save()

            criterion_resposnes = CriterionResponse.objects.all().filter(criterion_id = criterion.id, active=True)
            for response in criterion_resposnes:
                response.active = False
                response.save()

            payload = {"criterion": criterion,
                       "method": DELETE_METHOD}
            NotifyCriterion.broadcast(
                payload=payload)
               
            return DeleteCriterion(ok=ok, criterion=criterion)
        return DeleteCriterion(ok=ok, criterion=None)


class CreateCriterionResponse(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new Criterion Response"

    class Arguments:
        input = CriterionResponseInput(required=True)

    ok = graphene.Boolean()
    criterion_response = graphene.Field(CriterionResponseType)

    def generate_searchField(response):
        searchField = ''
        try:
            searchField = response.remarks if response.remarks is not None else ''
            searchField += str(response.score if response.score is not None else '')
        except:
            pass
        
        searchField = searchField.lower()
        return searchField

    def validate_criterion_response_input(input):
        error = ""
        if not input.participant_id:
            error += "Participant is a required field<br />"
        if not input.exercise_submission_id:
            error += "Exercise Submission is a requird field <br />" 
        if not input.remarker_id:
            error += "Remarker is a required field<br />"
        if not input.exercise_id:
            error += "Exercise is a required field<br />"
        if not input.score:
            error += "Score is a required field<br />"            
        if error:
            raise GraphQLError(error)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['CREATE']))
    def mutate(root, info, input=None):
        ok = True
        CreateCriterionResponse.validate_criterion_response_input(input)


        criterion_response_instance = CriterionResponse(criterion_id=input.criterion_id, exercise_submission_id=input.exercise_submission_id, exercise_id=input.exercise_id, participant_id = input.participant_id, remarker_id = input.remarker_id, score = input.score)
        criterion_response_instance.searchField= CreateCriterionResponse.generate_searchField(criterion_response_instance)
        criterion_response_instance.save()

        # Notifying creation of CriterionResponse
        payload = {"criterion_response": criterion_response_instance,
                   "method": CREATE_METHOD}
        NotifyCriterionResponse.broadcast(
            payload=payload)

        return CreateCriterionResponse(ok=ok, criterion_response=criterion_response_instance)


class UpdateCriterionResponse(graphene.Mutation):
    class Meta:
        description = "Mutation to update a CriterionResponse"

    class Arguments:
        id = graphene.ID(required=True)
        input = CriterionResponseInput(required=True)

    ok = graphene.Boolean()
    criterion_response = graphene.Field(CriterionResponseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['UPDATE']))
    def mutate(root, info, id, input=None):
        ok = False
        CreateCriterionResponse.validate_criterion_response_input(input)
        criterion_response_instance = CriterionResponse.objects.get(pk=id, active=True)
        if criterion_response_instance:
            ok = True
            criterion_response_instance.criterion_id = input.criterion_id if input.criterion_id is not None else criterion_response_instance.criterion_id
            criterion_response_instance.exercise_submission_id = input.exercise_submission_id if input.exercise_submission_id is not None else criterion_response_instance.exercise_submission_id
            criterion_response_instance.exercise_id = input.exercise_id if input.exercise_id is not None else criterion_response_instance.exercise_id
            criterion_response_instance.score = input.score if input.score is not None else criterion_response_instance.score
            criterion_response_instance.remarks = input.remarks if input.remarks is not None else criterion_response_instance.remarks
            criterion_response_instance.exercise_id = input.exercise_id if input.exercise_id is not None else criterion_response_instance.exercise_id
            criterion_response_instance.searchField = CreateCriterionResponse.generate_searchField(criterion_response_instance)

            criterion_response_instance.save()

            payload = {"criterion_response": criterion_response_instance,
                       "method": UPDATE_METHOD}
            NotifyCriterionResponse.broadcast(
                payload=payload)


            return UpdateCriterionResponse(ok=ok, criterion_response=criterion_response_instance)            
        return UpdateCriterionResponse(ok=ok, criterion_response=None)


class DeleteCriterionResponse(graphene.Mutation):
    class Meta:
        description = "Mutation to mark a CriterionResponse as inactive"

    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    criterion_response = graphene.Field(CriterionResponseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['DELETE']))
    def mutate(root, info, id):
        ok = False
        criterion_response = CriterionResponse.objects.get(pk=id, active=True)
        if criterion_response:
            ok = True
            criterion_response.active = False
            criterion_response.save()
            

            payload = {"criterion_response": criterion_response,
                       "method": DELETE_METHOD}
            NotifyCriterionResponse.broadcast(
                payload=payload)
               
            return DeleteCriterionResponse(ok=ok, criterion_response=criterion_response)
        return DeleteCriterionResponse(ok=ok, criterion_response=None)

class PatchCriterionResponses(graphene.Mutation):
    class Meta:
        description = "Mutation to patch criterion responses"

    class Arguments:
        pass

    ok = graphene.Boolean()
    criterion_responses_count = graphene.Int()

    @staticmethod
    @login_required
    # @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['LIST']))
    def mutate(root, info):
        ok = False

        all_criterion_responses = CriterionResponse.objects.all()
        total_count = all_criterion_responses.count()
        processed_count = 0
        for response in all_criterion_responses:
            try:
                submission = ExerciseSubmission.objects.get(participant_id=response.participant.id, exercise_id = response.exercise.id)
            except:
                print('Could not find submission with participant id ', response.participant.id, ' and exercise id ', response.exercise.id)
            response.exercise_submission_id = submission.id

            # Saving the response to the database
            response.save()
            processed_count += 1

        ok = True if processed_count == total_count else False
        return PatchCriterionResponses(ok=ok, criterion_responses_count=processed_count)
        
class PatchExerciseSubmissionsSearchFields(graphene.Mutation):
    class Meta:
        description = "Mutation to patch searchFields of all submissions"

    class Arguments:
        pass

    ok = graphene.Boolean()
    exercise_submissions_count = graphene.Int()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['UPDATE']))
    def mutate(root, info, exercise_submissions=None, grading=False, bulkauto=False):
        ok = False

        all_submissions = ExerciseSubmission.objects.filter(active=True)
        total_count = all_submissions.count()
        processed_count = 0
        for submission in all_submissions:
            # Generating a global searchFieldyy
            submission.searchField = CreateUpdateExerciseSubmissions.generate_searchField(submission)

            # Saving the submission to the database
            submission.save()
            processed_count += 1

        ok = True if processed_count == total_count else False
        return PatchExerciseSubmissionsSearchFields(ok=ok, exercise_submissions_count=processed_count)    

class CreateUpdateExerciseSubmissions(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new ExerciseSubmission"

    class Arguments:
        exercise_submissions = graphene.List(ExerciseSubmissionInput, required=True)
        grading = graphene.Boolean(required=True)
        bulkauto = graphene.Boolean()

    ok = graphene.Boolean()
    exercise_submissions = graphene.List(ExerciseSubmissionType)

    def generate_searchField(submission):
        searchField = ''
        if submission.course:
            searchField += submission.course.title if submission.course.title is not None else ""            
        if submission.chapter:
            searchField += submission.chapter.title if submission.chapter.title is not None else ""
        if submission.exercise:
            searchField += submission.exercise.prompt if submission.exercise.prompt is not None else ""
        searchField += submission.option if submission.option is not None else ""
        searchField += submission.answer if submission.answer is not None else ""
        searchField += submission.link if submission.link is not None else ""

        institution =  submission.participant.institution.name if submission.participant.institution.name is not None else ""
        participant = submission.participant.name if submission.participant.name is not None else ""
        grader = ""
        if submission.grader:
            grader = submission.grader.name if submission.grader.name is not None else ""
        # Adding institution, participant and grader
        searchField += institution.lower() if institution.lower() not in searchField else ""
        searchField += participant.lower() if participant.lower() not in searchField else ""
        searchField += grader.lower() if grader.lower() not in searchField else ""
        searchField = searchField.lower()      
        return searchField         

    def check_errors(exercise_submissions=None, grading=None):
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
                    if not submission.option:
                        error += "A valid option is required<br />"
                if exercise_instance.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
                    if not submission.answer:
                        error += "A valid answer is required<br />"
                if exercise_instance.question_type == Exercise.QuestionTypeChoices.IMAGE:
                    if not submission.images:
                        error += "At least one image is required<br />"
                if exercise_instance.question_type ==  Exercise.QuestionTypeChoices.LINK:
                    if not submission.link:
                        error += "A link is required<br />"
                    elif not grading:
                        try:
                            validator = URLValidator()
                            validator(submission.link)
                        except ValidationError:                
                            error += "Link should be a valid URL<br />"                        
        if error:
            raise GraphQLError(error)

    def updateCompletedChapter(root, info, chapter_id, participant_id):
        chapter = None
        participant = None
        completed_chapter = None
        try:
            chapter = Chapter.objects.get(pk=chapter_id, active=True)
            participant = User.objects.get(pk=participant_id, active=True)
            completed_chapter = CompletedChapters.objects.get(chapter_id=chapter_id, participant_id=participant_id)
        except:
            pass

        if chapter and participant and completed_chapter:
            exercises = Exercise.objects.filter(chapter_id=chapter_id, active=True)
            exerciseCount = Exercise.objects.all().filter(chapter_id=chapter_id,active=True).count()
            submittedCount = ExerciseSubmission.objects.all().filter(participant_id=participant_id, chapter_id=chapter_id, status=ExerciseSubmission.StatusChoices.SUBMITTED,active=True).count()
            gradedCount = ExerciseSubmission.objects.all().filter(participant_id=participant_id, chapter_id=chapter_id, status=ExerciseSubmission.StatusChoices.GRADED,active=True).count()        
            chapter_status = ExerciseSubmission.StatusChoices.SUBMITTED
            if submittedCount == exerciseCount - gradedCount:
                chapter_status = ExerciseSubmission.StatusChoices.SUBMITTED
            if gradedCount == exerciseCount: 
                chapter_status = ExerciseSubmission.StatusChoices.GRADED             
            totalPoints = chapter.points
            pointsScored = 0
            percentage = 0            
            for exercise in exercises:
                try:
                    submission = ExerciseSubmission.objects.all().get(participant_id=participant.id, exercise_id=exercise.id,active=True)
                    if submission.points is not None:
                        pointsScored += submission.points
                    if submission.percentage is not None:
                        percentage  += submission.percentage
                    if submission.status == ExerciseSubmission.StatusChoices.RETURNED:
                        chapter_status = ExerciseSubmission.StatusChoices.RETURNED                    
                except:
                    pass
            percentageCount = gradedCount + submittedCount
            percentage = percentage/percentageCount if percentageCount > 0 else 0
            percentage = percentage if exerciseCount > 0 else 100 # Giving them 100% if there are no exercises in the chapter

            # End of chapter status, score and total points and percentage calculation

            completed_chapter.status = chapter_status
            completed_chapter.course_id = chapter.course.id
            completed_chapter.scored_points = pointsScored
            completed_chapter.total_points = totalPoints
            completed_chapter.percentage = percentage
            completed_chapter.save()


    # Method returns ok if the chapter provided is completed by the participant
    def markChapterCompleted(root, info, chapter_id, participant_id):
        ok = False
        chapter = None
        chapter_already_completed = CompletedChapters.objects.filter(chapter_id=chapter_id, participant_id=participant_id).exists()
        # Start of process to check if the chapter is completed or not
        try:
            chapter = Chapter.objects.get(pk=chapter_id, active=True)
        except:
            pass

        if chapter is not None and not chapter_already_completed:
            # This block only executes if this chapter hasn't already been marked as completed prior
            ok = True
            all_required_exercises_submitted = False
            # First making sure that the chapter exists, if it does then we proceed to the next steps
            required_exercise_ids = Exercise.objects.filter(chapter_id=chapter_id, required=True, active=True).values_list('id', flat=True)
            if len(required_exercise_ids) > 0:
                # If the chapter has any required exercises, then check if each of the exercises has a corresponding submission
                # Calculating the ids of the exercises for which active submissions belonging to this participant exist 
                submitted_exercise_ids = ExerciseSubmission.objects.filter(chapter_id=chapter_id, participant_id=participant_id, active=True).values_list('exercise_id', flat=True)
                
                # Checking if each of the ids of the required exercise ids list exist in the submitted exercise ids list
                all_required_exercises_submitted = all(item in submitted_exercise_ids for item in required_exercise_ids)
            else:
                # If the chapter has no required exercises, add the chapter to completed chapters
                all_required_exercises_submitted = True

            if all_required_exercises_submitted:
                completed_chapter = CompletedChapters(participant_id=participant_id, chapter_id=chapter.id, course_id=chapter.course.id, total_points=chapter.points, status=ExerciseSubmission.StatusChoices.SUBMITTED)
                completed_chapter.save()
                chapter_already_completed = True # Marking this so that the updating happens below

        if chapter_already_completed:
            # Updating the status in the completed chapter list for the participant
            CreateUpdateExerciseSubmissions.updateCompletedChapter(root, info, chapter_id, participant_id)

        return ok

    # Method checks if the course is completed by the participant and if yes, adds it to the completed courses for the participant
    def markCourseCompleted(course_id, participant):
        course = None
        try:
            course = Course.objects.get(pk=course_id, active=True)
        except:
            pass    

        if course:
            report = Report.objects.get(course_id=course_id, participant_id=participant.id, active=True)
            course_completion_pass = report.completed >= course.pass_completion_percentage
            course_score_pass = report.percentage >= course.pass_score_percentage
            if course_completion_pass and course_score_pass: 
                participant.courses.add(course_id)  

    def process_submission_rubric(submission, input_rubric):
        exercise = submission.exercise
        exercise_rubric = Criterion.objects.all().filter(exercise_id=exercise.id, active=True).order_by('id')
        submission_rubric = CriterionResponse.objects.all().filter(exercise_id=exercise.id, participant_id=submission.participant.id, active=True)
        if exercise_rubric:
            if not submission_rubric:
                # While creating the submission, or if for some reason criteria for submissions don't exist yet, we create new
                for criterion in exercise_rubric:
                    criterion_response_instance = CriterionResponse(criterion_id=criterion.id, exercise_id=exercise.id, participant_id=submission.participant.id, exercise_submission_id=submission.id, score=0)
                    criterion_response_instance.save()     
            else:
                # If it exists already, we simply update them.
                for criterion_response in input_rubric:            
                    criterion_response_instance = CriterionResponse.objects.get(criterion_id=criterion_response.criterion_id, participant_id=submission.participant.id, active=True)
                    criterion_response_instance.criterion_id = criterion_response.criterion_id
                    criterion_response_instance.exercise_id = exercise.id
                    criterion_response_instance.participant_id = criterion_response.participant_id
                    criterion_response_instance.remarker_id = criterion_response.remarker_id
                    criterion_response_instance.remarks = criterion_response.remarks
                    criterion_response_instance.score = criterion_response.score if criterion_response.score is not None else 0
                    criterion_response_instance.save()

    def is_submission_empty(submission, exercise_id):
        exercise = Exercise.objects.get(pk=exercise_id)
        empty = True
        if exercise.question_type == Exercise.QuestionTypeChoices.OPTIONS:
            if submission.option:
               empty = False
        if exercise.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
            if submission.answer:
               empty = False
        if exercise.question_type == Exercise.QuestionTypeChoices.IMAGE:
            if submission.images:
               empty = False
        if exercise.question_type ==  Exercise.QuestionTypeChoices.LINK:
            if submission.link:
               empty = False    
        return empty

    def process_submission(submission, grading):
        autograded = False
        exercise = Exercise.objects.get(pk=submission.exercise_id, active=True)       
        try:
            exercise_key = ExerciseKey.objects.get(exercise_id=exercise.id, active=True)
        except:
            exercise_key = ExerciseKey(exercise_id=exercise.id, chapter_id=exercise.chapter.id, course_id=exercise.course.id)
            exercise_key.save()
            pass
        status = ExerciseSubmission.StatusChoices.SUBMITTED if grading != True  else submission.status
        points = submission.points if submission.points is not None else 0
        remarks = None if grading != True else submission.remarks

        # Automatic grading for description and multiple choice questions
        if exercise.question_type == Exercise.QuestionTypeChoices.DESCRIPTION:
            if exercise_key.valid_answers:
                if submission.answer in exercise_key.valid_answers:
                    autograded = True
                    status = ExerciseSubmission.StatusChoices['GRADED']
                    points = exercise.points
        if exercise.question_type == Exercise.QuestionTypeChoices.OPTIONS:
            autograded=True
            status = ExerciseSubmission.StatusChoices.GRADED
            if submission.option == exercise_key.valid_option:
                points = exercise.points
            else:
                points = 0
                remarks = 'Correct Option is "' + exercise_key.valid_option + '"'
        submission.points = points
        submission.status = status 
        submission.remarks = remarks
        totalPoints = exercise.points if exercise.points is not None else 0
        submission.percentage = submission.points * 100 / totalPoints if totalPoints > 0 else 100 # If total points is 0, then they get 100%

        return {'submission': submission, 'autograded': autograded}

    def freeze_rubric(submission):
        rubric = []
        try:
            for criterion_response in submission.rubric:
                criterion = Criterion.objects.all().get(pk=int(criterion_response.criterion_id))
                criterion_response['criterion'] = {'description': criterion.description, 'points': criterion.points}
                if criterion_response.remarker_id is not None:
                    remarker = User.objects.all().get(pk=int(criterion_response.remarker_id))
                    criterion_response['remarker'] = {'id': remarker.id, 'name': remarker.name}
                rubric.append(criterion_response)
        except:
            pass
        return rubric

    def update_submission(root, info, exercise_submission_instance, grading, autograded, submission, searchField):
        grader_id = info.context.user.id if grading and not autograded else None# If it is update, that means it is being graded, so here we add the grader_id
        exercise_submission_instance.exercise_id = submission.exercise_id if submission.exercise_id is not None else exercise_submission_instance.exercise_id
        exercise_submission_instance.course_id = submission.course_id if submission.course_id is not None else exercise_submission_instance.course_id
        exercise_submission_instance.chapter_id = submission.chapter_id if submission.chapter_id is not None else exercise_submission_instance.chapter_id
        exercise_submission_instance.option = submission.option if submission.option is not None else exercise_submission_instance.option
        exercise_submission_instance.answer = submission.answer if submission.answer is not None else exercise_submission_instance.answer
        exercise_submission_instance.link = submission.link if submission.link is not None else exercise_submission_instance.link
        exercise_submission_instance.images = submission.images if submission.images is not None else exercise_submission_instance.images
        exercise_submission_instance.points = submission.points if submission.points is not None else exercise_submission_instance.points
        exercise_submission_instance.percentage = submission.percentage if submission.percentage is not None else exercise_submission_instance.percentage
        exercise_submission_instance.status = submission.status if submission.status is not None else exercise_submission_instance.status
        exercise_submission_instance.remarks = submission.remarks 
        exercise_submission_instance.flagged = submission.flagged if submission.flagged is not None else exercise_submission_instance.flagged
        exercise_submission_instance.grader_id = grader_id
        exercise_submission_instance.searchField = searchField    
        return exercise_submission_instance

    def notify_graders(root, info, exercise_submission_instance):
        notification_text = exercise_submission_instance.participant.name + ' has submitted a new assignment for "' + exercise_submission_instance.chapter.title + '" in "' + exercise_submission_instance.course.title + '".\n\nPlease visit ' + settings.FRONTEND_DOMAIN_URL + '/dashboard?tab=Grading to completed grading the work.'
        graders = CourseGrader.objects.filter(course_id=exercise_submission_instance.course.id).distinct()
        print('Graders => ', graders)
        for grader in graders:
            recipient_list = [grader.grader.email]
            print('recipients_list => ',recipient_list)
            send_mail(
                'There is a new assignment submission!',
                notification_text,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
        return

    """
        This method is a bit complicated as it handles two different scenarios.
        First scenario - the student submits the exercises in a chapter. This is when the exercise submissions for the chapter are first created
        Second scenario - the grader updates the submissions with their updated score
        The difference is determined by the grading boolean argument. 
        Different things need to happen depending on this boolean value.
    """
    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['CREATE']) or has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['UPDATE']))
    def mutate(root, info, exercise_submissions=None, grading=False, bulkauto=False):
        print('Raw input for createUpdate submissions => ', exercise_submissions)
        ok = False
        current_user = info.context.user
        CreateUpdateExerciseSubmissions.check_errors(exercise_submissions, grading) # validating the input
        finalSubmissions = []
        manual_grading_required = False # This is used to track if we need to email the graders so that we only email when there is a non-autograded submission

        # If we're trying to do a bulk automatic grading of eligible submissions...
        if grading == True and bulkauto == True:
            eligible_exercises = Exercise.objects.filter(question_type__in=[Exercise.QuestionTypeChoices.DESCRIPTION,Exercise.QuestionTypeChoices.OPTIONS],active=True)
            exercise_submissions = ExerciseSubmission.objects.filter(exercise__in=eligible_exercises, status=ExerciseSubmission.StatusChoices.SUBMITTED,active=True)

        # Looping through the array of submissions to process them individually
        for submission in exercise_submissions:
            ok = True
            autograded = False 
            print('Submission in the list ', submission, 'current user ', current_user.name)

            # Calculating whether the submission is empty or not (regardless of whether it is for a required exercise)
            empty_submission = CreateUpdateExerciseSubmissions.is_submission_empty(submission, submission.exercise_id)

            print('Empty submission or not => ', empty_submission)
            if not empty_submission:

                # Processing the indivdual submission
                processed_submission = CreateUpdateExerciseSubmissions.process_submission(submission, grading)
                submission = processed_submission['submission']
                autograded = processed_submission['autograded']
                if not autograded:
                    manual_grading_required = True # This is used to track if any autograded submission exists
                    
                searchField = '' # Initializing an empty searchField. This will be added before we save it.

                # Checking if this is an update or a creation
                existing_submission = None
                method = CREATE_METHOD
                try:
                    # Looking for existing submission
                    existing_submission = ExerciseSubmission.objects.get(participant_id=submission.participant_id, exercise_id=submission.exercise_id, active=True)
                    if existing_submission is not None:
                        # If found, we store it in exercise_submission_instance
                        exercise_submission_instance = existing_submission
                        method = UPDATE_METHOD
                except:
                    pass                                           
                if existing_submission is None:
                    #If not found, we create it and store it in exercise_submission_instance
                    exercise_submission_instance = ExerciseSubmission(exercise_id=submission.exercise_id, course_id=submission.course_id, chapter_id=submission.chapter_id, participant_id=submission.participant_id, option=submission.option,
                                                                answer=submission.answer, link=submission.link, images=submission.images, points=submission.points, percentage=submission.percentage, status=submission.status, remarks=submission.remarks, searchField=searchField)
                else:
                    exercise_submission_instance = CreateUpdateExerciseSubmissions.update_submission(root, info, exercise_submission_instance, grading, autograded, submission, searchField)

                # Adding additional attributes to searchField
                searchField = CreateUpdateExerciseSubmissions.generate_searchField(exercise_submission_instance)
                exercise_submission_instance.searchField = searchField


                # Saving the variable to the database
                exercise_submission_instance.save()

                # Processing rubric for submission
                CreateUpdateExerciseSubmissions.process_submission_rubric(exercise_submission_instance, submission.rubric)

                # Freezing rubric for submission history
                frozen_rubric = CreateUpdateExerciseSubmissions.freeze_rubric(exercise_submission_instance)

                history = SubmissionHistory(exercise_id=exercise_submission_instance.exercise_id, participant_id=exercise_submission_instance.participant_id, option=exercise_submission_instance.option, answer=exercise_submission_instance.answer, link=exercise_submission_instance.link, images=exercise_submission_instance.images, points=exercise_submission_instance.points, rubric = frozen_rubric, status=exercise_submission_instance.status, flagged=exercise_submission_instance.flagged, grader=exercise_submission_instance.grader, remarks=exercise_submission_instance.remarks, active=exercise_submission_instance.active, searchField=searchField)
                history.save()

                if grading:
                    # Updating the submission status in the completed chapters field for the participant only when it is being graded,
                    # Because when the student is submitting it, this step is taken care of cumulatively for all submissions down below outside of the loop for all submissions since all of those submissions will belong to one chapter
                    # But when the grading is happening, the submissions in the loop may each belong to different chapters and we can be sure that each of those chapters is already in the participant's completed chapters list, 
                    # so while it is being graded it is possible to have it work for each submission since it will definitely have its chapter in the completed chapters list
                    CreateUpdateExerciseSubmissions.updateCompletedChapter(root, info, exercise_submission_instance.chapter.id, exercise_submission_instance.participant.id)

                # Adding it to the list of submissions that will then be passed on for report generation
                finalSubmissions.append(exercise_submission_instance)

                payload = {"exercise_submission": exercise_submission_instance,
                        "method": method}
                NotifyExerciseSubmission.broadcast(
                    payload=payload)
                
                # End of grading the submission

        # Marking the chapter as submitted and updating scores if it is in "create" mode
        if not grading and finalSubmissions:
            chapter_id = finalSubmissions[0].chapter.id
            course_id = finalSubmissions[0].course_id
            participant_id = finalSubmissions[0].participant.id
            #Marking chapter completed
            CreateUpdateExerciseSubmissions.markChapterCompleted(root, info, chapter_id, participant_id)
            # Updating completion % and score % in the report
            UpdateReport.mutate(root, info, course_id, participant_id)
            # Sending email notification to graders
            print('Manual grading required => ', manual_grading_required)
            if manual_grading_required:
                print('Sending notification emails to graders...')
                CreateUpdateExerciseSubmissions.notify_graders(root, info, exercise_submission_instance)

            exercise_submission_submitted() # Clearing cache if assignment is submitted
            ok = True
        else:
            # If grading is done, i.e. it is in "update" mode, we recalculate the score
            UpdateReport.recalculate(root, info, finalSubmissions) # updating the reports
            exercise_submission_graded() # Clearing cache if grading is done

        return CreateUpdateExerciseSubmissions(ok=ok, exercise_submissions=finalSubmissions)


# class UpdateExerciseSubmission(graphene.Mutation):
#     class Meta:
#         description = "Mutation to update a ExerciseSubmission"

#     class Arguments:
#         id = graphene.ID(required=True)
#         input = ExerciseSubmissionInput(required=True)

#     ok = graphene.Boolean()
#     exercise_submission = graphene.Field(ExerciseSubmissionType)

#     @staticmethod
#     @login_required
#     @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
#     def mutate(root, info, id, input=None):
#         ok = False
#         exercise_submission_instance = ExerciseSubmission.objects.get(
#             pk=id, active=True)
#         if exercise_submission_instance:
#             ok = True
#             exercise_submission_instance.exercise_id = input.exercise_id if input.exercise_id is not None else exercise_submission_instance.exercise_id
#             exercise_submission_instance.course_id = input.course_id if input.course_id is not None else exercise_submission_instance.course_id
#             exercise_submission_instance.chapter_id = input.chapter_id if input.chapter_id is not None else exercise_submission_instance.chapter_id
#             exercise_submission_instance.option = input.option if input.option is not None else exercise_submission_instance.option
#             exercise_submission_instance.answer = input.answer if input.answer is not None else exercise_submission_instance.answer
#             exercise_submission_instance.link = input.link if input.link is not None else exercise_submission_instance.link
#             exercise_submission_instance.images = input.images if input.images is not None else exercise_submission_instance.images
#             exercise_submission_instance.points = input.points if input.points is not None else exercise_submission_instance.points
#             exercise_submission_instance.status = input.status if input.status is not None else exercise_submission_instance.status

#             searchField = input.option
#             searchField += input.answer if input.answer is not None else ""
#             searchField += input.link if input.link is not None else ""
#             exercise_submission_instance.searchField = searchField.lower()

#             exercise_submission_instance.save()
#             payload = {"exercise_submission": exercise_submission_instance,
#                        "method": UPDATE_METHOD}
#             NotifyExerciseSubmission.broadcast(
#                 payload=payload)
#             return UpdateExerciseSubmission(ok=ok, exercise_submission=exercise_submission_instance)
#         return UpdateExerciseSubmission(ok=ok, exercise_submission=None)


# class DeleteExerciseSubmission(graphene.Mutation):
#     class Meta:
#         description = "Mutation to mark a ExerciseSubmission as inactive"

#     class Arguments:
#         id = graphene.ID(required=True)

#     ok = graphene.Boolean()
#     exercise_submission = graphene.Field(ExerciseSubmissionType)

#     @staticmethod
#     @login_required
#     @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['DELETE']))
#     def mutate(root, info, id):
#         ok = False
#         exercise_submission_instance = ExerciseSubmission.objects.get(
#             pk=id, active=True)
#         if exercise_submission_instance:
#             ok = True
#             exercise_submission_instance.active = False

#             exercise_submission_instance.save()
#             payload = {"exercise_submission": exercise_submission_instance,
#                        "method": DELETE_METHOD}
#             NotifyExerciseSubmission.broadcast(
#                 payload=payload)
#             return DeleteExerciseSubmission(ok=ok, exercise_submission=exercise_submission_instance)
#         return DeleteExerciseSubmission(ok=ok, exercise_submission=None)


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
        if input.institution_id is None:
            error += "Institution is a required field<br />"            
        if input.completed is None:
            error += "Completed is a required field<br />"
        if input.score is None:
            error += "Score is a required field<br />"
        if error:
            raise GraphQLError(error)
        searchField = ""
        searchField = searchField.lower()

        report_instance = Report(participant_id=input.participant_id, course_id=input.course_id, institution_id=input.institution_id,
                                 completed=input.completed, score=input.score, searchField=searchField)
        report_instance.save()

        payload = {"report": report_instance,
                   "method": CREATE_METHOD}
        NotifyReport.broadcast(
            payload=payload)
        return CreateReport(ok=ok, report=report_instance)

class PatchReportsSearchFields(graphene.Mutation):
    class Meta:
        description = "Mutation to patch searchFields of all reports"

    class Arguments:
        pass

    ok = graphene.Boolean()
    reports_count = graphene.Int()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['UPDATE']))
    def mutate(root, info):
        ok = False

        all_reports = Report.objects.filter(active=True)
        total_count = all_reports.count()
        processed_count = 0
        for report_instance in all_reports:
            # Generating a global searchField
            report_instance = UpdateReport.generate_searchfield(report_instance)

            report_instance.save()
            processed_count += 1

        ok = True if processed_count == total_count else False
        return PatchReportsSearchFields(ok=ok, reports_count=processed_count)    

class PatchCompletedChapters(graphene.Mutation):
    class Meta:
        description = "Mutation to update the fields in completed chapters"

    class Arguments:
        pass

    ok = graphene.Boolean()

    """
    Before running this via Postman, make sure that you mark all the rows in completed chapters table with status as PE
    """
    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['REPORT'], ACTIONS['UPDATE']))
    def mutate(root, info):
        ok = True
        count = CompletedChapters.objects.filter(status=ExerciseSubmission.StatusChoices.PENDING).count()
        completed_chapters = CompletedChapters.objects.filter(status=ExerciseSubmission.StatusChoices.PENDING)
        for chapter in completed_chapters:
            CreateUpdateExerciseSubmissions.updateCompletedChapter(root, info, chapter.chapter_id, chapter.participant_id)
            

        return PatchCompletedChapters(ok=ok)

class UpdateReport(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Report"

    class Arguments:
        course_id = graphene.ID(required=True)
        participant_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    report = graphene.Field(ReportType)

    def generate_searchfield(report):
        participant = report.participant
        searchField = report.participant.name if participant else ""
        institution = report.institution
        searchField += report.institution.name if institution else "" 
        course = report.course
        searchField += report.course.title if course else ""
        searchField += str(report.completed) if report.completed else ""
        searchField += str(report.percentage) if report.percentage else ""
        searchField = searchField.lower()
        report.searchField = searchField
        return report

    def remove_duplicate_submissions(all_submissions):
        unique_submissions = []
        for submission in all_submissions:
            if unique_submissions:
                for entry in unique_submissions:
                    if submission.participant_id == entry.participant_id and submission.course_id == entry.course_id:
                        pass
                    else:
                        unique_submissions.append(submission)
            else:
                unique_submissions.append(submission)
        return unique_submissions

    # This is the method used to update grading every time grading happens
    def recalculate(root, info, all_submissions):
        unique_submissions = UpdateReport.remove_duplicate_submissions(all_submissions)
        for submission in unique_submissions:
            participant_id = submission.participant_id
            course_id = submission.course_id
            UpdateReport.mutate(root, info, course_id, participant_id)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['CREATE']) or has_access(user, RESOURCES['EXERCISE_SUBMISSION'], ACTIONS['UPDATE']) or has_access(user, RESOURCES['REPORT'], ACTIONS['UPDATE']))    
    def mutate(root, info, course_id, participant_id):
        # Method takes in the course id and the participant id and recalculates the score and completion % in the report, creates new if it doesn't exist
        ok = False
        method = CREATE_METHOD
        report_instance=None

        if course_id is not None and participant_id is not None:
            # Getting the report instance from the course and participant
            participant=None
            try:
                participant = User.objects.all().get(pk=participant_id)
            except:
                raise GraphQLError('Participant not found')
          
            try:
                report_instance = Report.objects.get(
                    participant_id=participant_id, course_id=course_id, active=True)
                method = UPDATE_METHOD
            except:            
                report_instance = Report(participant_id=participant_id, course_id=course_id, institution_id=participant.institution.id,
                                    completed=0, percentage=0)
        
        if report_instance:
            # Only if report_instance exists, we proceed, otherwise we exit
            ok = True
            # Calculating score %
            total_percentage = 0
            participant_id = report_instance.participant.id
            course_id=report_instance.course.id
            submissions = ExerciseSubmission.objects.all().filter(participant_id=participant_id, course_id=course_id,active=True)            
            for submission in submissions:
                submission_percentage = submission.percentage if submission.percentage is not None else 0
                total_percentage = total_percentage + submission_percentage
            percentage = total_percentage/len(submissions)

            # Calculating Completion %
            completed = 0
            course_chapters_count = Chapter.objects.all().filter(course_id=course_id, active=True).count()
            completed_chapter_count = CompletedChapters.objects.filter(participant_id=participant_id, course_id=course_id).count()
            completed = (completed_chapter_count/course_chapters_count)*100

            report_instance.percentage = percentage
            report_instance.completed = completed

            # Generating searchField
            report_instance = UpdateReport.generate_searchfield(report_instance)

            report_instance.save()

            # Marking course as completed
            CreateUpdateExerciseSubmissions.markCourseCompleted(course_id, participant)
            
            payload = {"report": report_instance,
                    "method": method}
            NotifyReport.broadcast(
                payload=payload)
            return UpdateReport(ok=ok, report=report_instance)

        return UpdateReport(ok=ok, report=report_instance)


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
        if member is None:
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
    @login_required
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


class ReorderChapters(graphene.Mutation):
    class Meta:
        description = "Mutation to reorder the chapters"

    class Arguments:
        indexList = graphene.List(IndexListInputType, required=True)

    ok = graphene.Boolean()
    chapters = graphene.List(ChapterType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))
    def mutate(root, info, indexList=[]):
        ok = True
        chapters = []
        for indexObject in indexList:
            try:
                chapter = Chapter.objects.get(pk=indexObject.id, active=True)
                chapter.index = indexObject.index
                chapter.save()
                payload = {"chapter": chapter,
                        "method": UPDATE_METHOD}
                NotifyChapter.broadcast(
                    payload=payload)                
                chapters.append(chapter)
            except:
                ok = False
                pass
 
        return ReorderChapters(ok=ok, chapters=chapters)

class ReorderExercises(graphene.Mutation):
    class Meta:
        description = "Mutation to reorder the exercises"

    class Arguments:
        indexList = graphene.List(IndexListInputType, required=True)

    ok = graphene.Boolean()
    exercises = graphene.List(ExerciseType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['CHAPTER'], ACTIONS['UPDATE']))    
    def mutate(root, info, indexList=[]):
        ok = True
        exercises = []
        failedExercices = []
        for indexObject in indexList:
            try:
                exercise = Exercise.objects.all().get(pk=indexObject.id, active=True)
                exercise.index = indexObject.index
                exercise.save()
                payload = {"exercise": exercise,
                        "method": UPDATE_METHOD}
                NotifyExercise.broadcast(
                    payload=payload)                
            except:
                failedExercices.append(indexObject)
                ok=False
                pass
        return ReorderExercises(ok=ok, exercises=exercises)

class ReorderCourseSections(graphene.Mutation):
    class Meta:
        description = "Mutation to reorder the course sections"

    class Arguments:
        indexList = graphene.List(IndexListInputType, required=True)

    ok = graphene.Boolean()
    course_sections = graphene.List(CourseSectionType)

    @staticmethod
    @login_required
    @user_passes_test(lambda user: has_access(user, RESOURCES['COURSE'], ACTIONS['UPDATE']))
    def mutate(root, info, indexList=[]):
        ok = True
        course_sections = []
        for indexObject in indexList:
            try:
                course_section = CourseSection.objects.get(pk=indexObject.id, active=True)
                course_section.index = indexObject.index
                course_section.save()
                payload = {"course_section": course_section,
                        "method": UPDATE_METHOD}
                NotifyCourseSection.broadcast(
                    payload=payload)                
                course_sections.append(course_section)
            except:
                ok = False
                pass
 
        return ReorderCourseSections(ok=ok, course_sections=course_sections)

class ClearServerCache(graphene.Mutation):
    class Meta:
        description = "Clear serverside cache"

    ok = graphene.Boolean()

    @staticmethod
    @login_required
    @user_passes_test(lambda user: is_admin_user(user))
    def mutate(root, info):
        cache.clear()
        ok = True
        return ClearServerCache(ok=ok)

# createGoogleToken
class createGoogleToken(graphene.Mutation):
    ok = graphene.Boolean()
    token = graphene.String()
    refresh_token = graphene.String()
    class Meta:
        description = "Mutation to create Google login token"
    class Arguments:
        input = UserInput(required=True)
    
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(self, info, input=None):
        ok = True
        error = ""
        if input.email is None:
            error += "Email is a required field<br />"
        if error:
            raise GraphQLError(error)
        searchField = input.email
        searchField = searchField.lower()
        if (User.objects.filter(email=input.email).exists()==False):   
            user_instance = User(email=input.email,first_name=input.first_name,last_name=input.last_name, searchField=searchField)
            user_instance.save()
        else:
           user_instance= User.objects.get(email=input.email)
        
        payload = {"user": user_instance,
                    "method": CREATE_METHOD}
        NotifyUser.broadcast(
                payload=payload)        
        token = get_token(user_instance)
        refresh_token = create_refresh_token(user_instance)
        return createGoogleToken(ok=ok,user=user_instance, token=token, refresh_token=refresh_token)

class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()

    add_invitecode = AddInvitecode.Field()
    verify_invitecode = VerifyInvitecode.Field()
    generate_email_otp = GenerateEmailOTP.Field()
    verify_email_otp = VerifyEmailOTP.Field()
    verify_email_user = verifyEmailUser.Field()
    # passwordChange = passwordChange.Field()

    # create_user = createUser.Field()
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
    mark_announcements_seen = MarkAnnouncementsSeen.Field()

    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    clap_project = ClapProject.Field()

    create_issue = CreateIssue.Field()
    update_issue = UpdateIssue.Field()
    update_issue_status = UpdateIssueStatus.Field()
    delete_issue = DeleteIssue.Field()    

    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
    publish_course = PublishCourse.Field()

    create_course_section = CreateCourseSection.Field()
    update_course_section = UpdateCourseSection.Field()
    delete_course_section = DeleteCourseSection.Field()

    create_chapter = CreateChapter.Field()
    update_chapter = UpdateChapter.Field()
    delete_chapter = DeleteChapter.Field()
    publish_chapter = PublishChapter.Field()

    create_exercise = CreateExercise.Field()
    update_exercise = UpdateExercise.Field()
    delete_exercise = DeleteExercise.Field()

    create_criterion = CreateCriterion.Field()
    update_criterion = UpdateCriterion.Field()
    delete_criterion = DeleteCriterion.Field()    

    create_update_exercise_submissions = CreateUpdateExerciseSubmissions.Field()

    delete_chat = DeleteChat.Field()
    chat_with_member = ChatWithMember.Field()

    create_chat_message = CreateChatMessage.Field()
    update_chat_message = UpdateChatMessage.Field()
    delete_chat_message = DeleteChatMessage.Field()

    reorder_chapters = ReorderChapters.Field()
    reorder_exercises = ReorderExercises.Field()
    reorder_course_sections = ReorderCourseSections.Field()

    # Bulk patching/sanitizing mutations
    patch_exercise_submissions_searchFields = PatchExerciseSubmissionsSearchFields.Field()
    patch_reports_searchFields = PatchReportsSearchFields.Field()
    patch_completed_chapters = PatchCompletedChapters.Field()
    patch_criterion_responses = PatchCriterionResponses.Field()

    # Admin mutations
    clear_server_cache = ClearServerCache.Field()

    #Social AUth
    social_auth = graphql_social_auth.SocialAuthJWT.Field()

    # Create Google login Token
    create_google_token = createGoogleToken.Field()
