import graphene
from graphene_django.types import ObjectType
from vidhya.models import User
from django.conf import settings
from common.cyTestingData import EXISTING_DATA

# This file contains queries dedicated for automated testing purposes

class OkResponse(graphene.ObjectType):
    ok = graphene.Boolean()

class EmptyQuery(ObjectType):
    pass


class Query(ObjectType):

    # Automated Testing related queries
    cy_delete_new_user = graphene.Field(OkResponse)


    def resolve_cy_delete_new_user(root, info, **kwargs):
        ok = False
        if settings.ENABLED_AUTOMATED_TESTING:
            newUserUsername = EXISTING_DATA['newUser']['username']
            print('new user => ', newUserUsername)
            try:
                newuser = User.objects.get(username=newUserUsername)
                print('newuser => ', newuser)
                newuser.delete()
                ok = True
            except:
                pass
        response = OkResponse(ok=ok)
        return response