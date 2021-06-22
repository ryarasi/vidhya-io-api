import channels_graphql_ws
import channels
import graphene
from .gqTypes import InstitutionType


class NotifyInstitution(channels_graphql_ws.Subscription):
    institution = graphene.Field(InstitutionType)

    # class Arguments:

    @staticmethod
    def subscribe(root, info):
        user_id = info.context.user.user_id
        return [user_id] if user_id else None

    @staticmethod
    def publish(payload, info):
        return NotifyInstitution(institution=payload, info=info)


class Subscription(graphene.ObjectType):
    notify_institution = NotifyInstitution.Field()
