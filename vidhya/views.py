from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

from .serializers import FileSerializer
# Create your views here.
# Create your views here.


def index(request):
    # Render the HTML template index.html
    context = {}
    return render(request, 'index.html', context=context)


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SSO(APIView):
    
    def get(self, request, *args, **kwargs):
        user = request.user

      # Render the HTML template index.html
        context = {}
        # return render(request, 'SSOLogin.html', context=context)
    
        # if UserSocialAuth.is_valid():
            # file_serializer.save()
        return Response(user)
        # else:
        #     return Response(user)
        
# class SettingsView(LoginRequiredMixin, TemplateView):
    
#     def get(self, request, *args, **kwargs):
#         user = request.user

#         try:
#             github_login = user.social_auth.get(provider='github')
#         except UserSocialAuth.DoesNotExist:
#             github_login = None

#         try:
#             twitter_login = user.social_auth.get(provider='twitter')
#         except UserSocialAuth.DoesNotExist:
#             twitter_login = None

#         try:
#             facebook_login = user.social_auth.get(provider='facebook')
#         except UserSocialAuth.DoesNotExist:
#             facebook_login = None

#         can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

#         return render(request, '/settings.html', {
#             'github_login': github_login,
#             'twitter_login': twitter_login,
#             'facebook_login': facebook_login,
#             'can_disconnect': can_disconnect
#         })
