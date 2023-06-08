from . import views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', FileUploadView.as_view()),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('googleLogin/', SSO.as_view()),

]
