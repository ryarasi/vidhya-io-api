from calendar import timegm
from datetime import datetime
from .settings import jwt_settings
from vidhya.models import User
from django.utils import timezone

# This is used to add the userId as sub to the JWT payload


def jwt_payload(user, context=None):
    username = user.get_username()
    user_id = str(user.id)

    if hasattr(username, 'pk'):
        username = username.pk

    payload = {
        user.USERNAME_FIELD: username,
        'sub': user_id,
        'exp': datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA,
    }

    if jwt_settings.JWT_ALLOW_REFRESH:
        payload['origIat'] = timegm(datetime.utcnow().utctimetuple())

    if jwt_settings.JWT_AUDIENCE is not None:
        payload['aud'] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload['iss'] = jwt_settings.JWT_ISSUER

    return payload

# This is used to update the lastActive field every time a user makes a request.
# It helps to track when they were last active.


class UpdateLastActivityMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.id) \
                        .update(last_active=timezone.now())
        response = self.get_response(request)

        return response
