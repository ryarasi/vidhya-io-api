import graphene

from graphene_django.types import DjangoObjectType, ObjectType
from vidhya.models import User, Institution, Group

# Create a GraphQL type for the Institution model


class InstitutionType(DjangoObjectType):
    class Meta:
        model = Institution

# Create a GraphQL type for the User model


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username', 'searchField']

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
            return Institution.objects.get(pk=id)

        return None

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_group(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Group.objects.get(pk=id)

        return None

    def resolve_institutions(self, info, **kwargs):
        return Institution.objects.all()

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_groups(self, info, **kwargs):
        return Group.objects.all()

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
        institution_instance = Institution(name=input.name, location=input.location, city=input.city,
                                           website=input.website, phone=input.phone, logo=input.logo, bio=input.bio)
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

            institution_instance.save()
            return UpdateInstitution(ok=ok, institution=institution_instance)
        return UpdateInstitution(ok=ok, institution=None)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        searchField = input.username + input.title + input.bio
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
            user_instance.searchField = user_instance.name + \
                user_instance.title + user_instance.bio
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
