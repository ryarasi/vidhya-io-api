import channels_graphql_ws
import channels
import graphene
from graphql_jwt.decorators import login_required
from .gqTypes import InstitutionType


class NotifyInstitution(channels_graphql_ws.Subscription):
    institution = graphene.Field(InstitutionType)
    method = graphene.String()
    # class Arguments:

    @login_required
    @staticmethod
    def subscribe(root, info):
        # user_id = info.context.user.user_id
        # return [user_id] if user_id else None
        return None

    @login_required
    @staticmethod
    def publish(payload, method, info):
        return NotifyInstitution(institution=payload, method=method)


class Subscription(graphene.ObjectType):
    notify_institution = NotifyInstitution.Field()
