import graphene
from graphene_django.types import ObjectType
from vidhya.models import Announcement, User
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
    cy_create_global_announcement = graphene.Field(OkResponse)
    cy_delete_global_announcement = graphene.Field(OkResponse)

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

    def resolve_cy_create_global_announcement(root, info, **kwargs):
        ok = False
        if settings.ENABLED_AUTOMATED_TESTING:
            input = EXISTING_DATA['newAnnouncement']
            new_announcement_instance = Announcement(title=input['title'], author_id=input['author'], message=input['message'],
                                             institution_id=input['institution'], recipients_global=input['recipients_global'])
            try:
                new_announcement_instance.save()
                ok = True
            except:
                pass
        response = OkResponse(ok=ok)
        return response

    def resolve_cy_delete_global_announcement(root, info, **kwargs):
        ok = True
        if settings.ENABLED_AUTOMATED_TESTING:
            input = EXISTING_DATA['newAnnouncement']
            all_announcements = Announcement.objects.filter(title=input['title'], author_id=input['author'], message=input['message'],
                                             institution_id=input['institution'], recipients_global=input['recipients_global'])
            for announcement in all_announcements:
                try:
                    announcement.delete()
                except:
                    ok = False
                    pass
        response = OkResponse(ok=ok)
        return response