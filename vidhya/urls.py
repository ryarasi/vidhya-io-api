from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', FileUploadView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
