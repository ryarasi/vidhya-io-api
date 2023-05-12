from rest_framework import serializers
from .models import Announcement, File, User, Institution, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"
        