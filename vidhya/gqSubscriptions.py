import channels_graphql_ws
import graphene
from graphql_jwt.decorators import login_required
from .gqTypes import InstitutionType


class NotifyInstitution(channels_graphql_ws.Subscription):
    institution = graphene.Field(InstitutionType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        return NotifyInstitution(institution=payload["institution"], method=payload["method"])


class Subscription(graphene.ObjectType):
    notify_institution = NotifyInstitution.Field()
