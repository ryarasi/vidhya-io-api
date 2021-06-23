import channels_graphql_ws
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
        print('info => ', info.context.user)
        # user_id = info.context.user.user_id
        # return [user_id] if user_id else None
        return None

    @login_required
    @staticmethod
    def publish(payload, info):
        return NotifyInstitution(institution=payload["institution"], method=payload["method"])


class Subscription(graphene.ObjectType):
    notify_institution = NotifyInstitution.Field()
