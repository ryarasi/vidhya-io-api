import graphene
from graphql import GraphQLError
from vidhya.models import User, Institution, Group, GroupMember
from graphene_django_extras import DjangoSerializerMutation
from .gqTypes import InstitutionType, InstitutionModelType, UserType, UserModelType, GroupType, GroupModelType, UserInput, InstitutionInput, GroupInput
from .serializers import UserSerializer, InstitutionSerializer, GroupSerializer


class CreateInstitution(graphene.Mutation):
    class Meta:
        description = "Mutation to create new a Institution"

    class Arguments:
        input = graphene.Argument(InstitutionInput)

    ok = graphene.Boolean()
    institution = graphene.Field(InstitutionType)

    @staticmethod
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
        id = graphene.Int(required=True)
        input = InstitutionInput(required=True)

    ok = graphene.Boolean()
    institution = graphene.Field(InstitutionType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        institution = Institution.objects.get(pk=id)
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


# class DeleteInstitution(graphene.Mutation):
#     class Meta:
#         description = "Mutation to mark an Institution as inactive"

#     class Arguments:
#         id = graphene.Int(required=True)

#     ok = graphene.Boolean()
#     institution = graphene.Field(InstitutionType)

#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         institution = Institution.objects.get(pk=id, active=True)
#         institution_instance = institution
#         if institution_instance:
#             ok = True
#             institution_instance.active = False

#             institution_instance.save()
#             return DeleteInstitution(ok=ok, institution=institution_instance)
#         return DeleteInstitution(ok=ok, institution=None)


class CreateUser(graphene.Mutation):
    class Meta:
        description = "Mutation to create a new User"

    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
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


class UpdateUser(graphene.Mutation):
    class Meta:
        description = "Mutation to update a User"

    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user = User.objects.get(pk=id)
        user_instance = user
        if user_instance:
            ok = True
            user_instance.name = input.name if input.name is not None else user.name
            user_instance.avatar = input.avatar if input.avatar is not None else user.avatar
            user_instance.institution_id = input.institution_id if input.institution_id is not None else user.institution_id
            user_instance.title = input.title if input.title is not None else user.title
            user_instance.bio = input.bio if input.bio is not None else user.bio

            searchField = user_instance.name if user_instance.name is not None else ""
            searchField += user_instance.title if user_instance.title is not None else ""
            searchField += user_instance.bio if user_instance.bio is not None else ""
            user_instance.searchField = searchField.lower()

            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


# class DeleteUser(graphene.Mutation):
#     class Meta:
#         description = "Mutation to mark a User as inactive"

#     class Arguments:
#         id = graphene.Int(required=True)

#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)

#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         user = User.objects.get(pk=id, active=True)
#         user_instance = user
#         if user_instance:
#             ok = True
#             user_instance.active = False

#             user_instance.save()
#             return UpdateUser(ok=ok, user=user_instance)
#         return UpdateUser(ok=ok, user=None)

class UserSerializerMutation(DjangoSerializerMutation):
    """
        DjangoSerializerMutation auto implement Create, Delete and Update functions
    """
    class Meta:
        description = " DRF serializer based Mutation for Users "
        serializer_class = UserSerializer


class CreateGroup(graphene.Mutation):

    class Meta:
        description = "Mutation to create a new Group"

    class Arguments:
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, input=None):
        user = info.context.user
        if not user.is_authenticated:
            return CreateGroup(errors='You must be logged in to do that!')
        ok = True
        error = ""
        if input.name is None:
            error += "Name is a required field<br />"
        if input.description is None:
            error += "Description is a required field<br />"
        if len(error) > 0:
            raise GraphQLError(error)
        searchField = input.name
        searchField += input.description if input.description is not None else ""
        searchField = searchField.lower()

        group_instance = Group(name=input.name, description=input.description,
                               institution_id=input.institution, searchField=searchField)
        group_instance.save()

        if input.members is not None:
            group_instance.members.add(*input.members)
        if input.admins is not None:
            group_instance.admins.add(*input.admins)

        # Adding the creator of the group as an admin
        group_instance.admins.set([user.id])

        return CreateGroup(ok=ok, group=group_instance)


class UpdateGroup(graphene.Mutation):
    class Meta:
        description = "Mutation to update a Group"

    class Arguments:
        id = graphene.Int(required=True)
        input = GroupInput(required=True)

    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, id, input=None):
        user = info.context.user
        if not user.is_authenticated:
            return UpdateGroup(errors='You must be logged in to do that!')
        ok = False
        group = Group.objects.get(pk=id)
        group_instance = group
        if group_instance:
            ok = True
            group_instance.name = input.name if input.name is not None else group.name
            group_instance.description = input.description if input.description is not None else group.description
            group_instance.institution_id = input.institution if input.institution is not None else group.institution_id

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
            group_instance.admins.set([user.id])

            return UpdateGroup(ok=ok, group=group_instance)
        return UpdateGroup(ok=ok, group=None)


# class DeleteGroup(graphene.Mutation):
#     class Meta:
#         description = "Mutation to mark a Group as inactive"

#     class Arguments:
#         id = graphene.Int(required=True)

#     ok = graphene.Boolean()
#     group = graphene.Field(GroupType)

#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         group = Group.objects.get(pk=id, active=True)
#         group_instance = group
#         if group_instance:
#             ok = True
#             group_instance.active = False

#             group_instance.save()
#             return UpdateGroup(ok=ok, group=group_instance)
#         return UpdateGroup(ok=ok, group=None)

class GroupSerializerMutation(DjangoSerializerMutation):
    """
        DjangoSerializerMutation auto implement Create, Delete and Update functions
    """
    class Meta:
        description = " DRF serializer based Mutation for Groups "
        serializer_class = GroupSerializer


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = InstitutionModelType.DeleteField(
        description='Delete Institution')
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = UserModelType.DeleteField(
        description='Delete User')
    create_group = CreateGroup.Field()
    update_group = UpdateGroup.Field()
    delete_group = GroupModelType.DeleteField(
        description='Delete Group')
