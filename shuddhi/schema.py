import vidhya.schema
import graphene
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from common.utils import generate_jti


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()


class LogoutUser(graphene.Mutation):
    id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        user.jti = generate_jti()
        user.save()
        return cls(id=user.id)


class Query(vidhya.schema.Query, UserQuery, MeQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(vidhya.schema.Mutation, AuthMutation, LogoutUser, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
