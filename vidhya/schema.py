import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType, ObjectType
from vidhya.models import User, Institution, Group

# Create a GraphQL type for the Institution model


class InstitutionType(DjangoObjectType):
    class Meta:
        model = Institution
        filter_fields = ['searchField']
# Create a GraphQL type for the User model


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['searchField']

# Create a GraphQL type for the Group model


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class Query(ObjectType):
    institution = graphene.Field(InstitutionType, id=graphene.Int())
    user = graphene.Field(UserType, id=graphene.Int())
    group = graphene.Field(GroupType, id=graphene.Int())
    institutions = graphene.List(InstitutionType)
    users = graphene.List(UserType)
    groups = graphene.List(GroupType)

    def resolve_institution(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            institution = Institution.objects.get(pk=id, active=True)
            if not institution:
                raise GraphQLError('Institution not found!')
            return institution

        return None

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            user = User.objects.get(pk=id, active=True)
            if not user:
                raise GraphQLError('User not found!')
            return user

        return None

    def resolve_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            group = Group.objects.get(pk=id, active=True)
            if not group:
                raise GraphQLError('Group not found!')
            return group

        return None

    def resolve_institutions(self, info, **kwargs):
        return Institution.objects.filter(active=True)

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(active=True)

    def resolve_groups(self, info, **kwargs):
        return Group.objects.filter(active=True)

# Create Input Object Types


class InstitutionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    location = graphene.String()
    city = graphene.String()
    website = graphene.String()
    phone = graphene.String()
    logo = graphene.String()
    bio = graphene.String()
    searchField = graphene.String()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    user_id = graphene.Int(name="user", required=True)
    name = graphene.String()
    email = graphene.String()
    avatar = graphene.String()
    institution_id = graphene.Int(name="institution", required=True)
    title = graphene.String()
    bio = graphene.String()
    searchField = graphene.String()


class CreateInstitution(graphene.Mutation):
    class Arguments:
        input = InstitutionInput(required=True)

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


class DeleteInstitution(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

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
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        searchField = input.username if input.username is not None else "" + \
            input.title if input.title is not None else "" + \
            input.bio if input.bio is not None else ""
        user_instance = User(user_id=input.user_id, title=input.title, bio=input.bio,
                             institution_id=input.institution_id, searchField=searchField)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)


class UpdateUser(graphene.Mutation):
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
            user_instance.searchField = user_instance.searchField + \
                user_instance.name if user_instance.name is not None else ""
            user_instance.searchField = user_instance.searchField + \
                user_instance.title if user_instance.title is not None else ""
            user_instance.searchField = user_instance.searchField + \
                user_instance.bio if user_instance.bio is not None else ""
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

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
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
