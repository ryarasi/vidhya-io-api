from django.contrib import admin
from .models import Chat, ChatMessage, CourseSection, Exercise, ExerciseSubmission, Report, User, Institution, UserRole, Group, Announcement, Course, Chapter
from django.apps import apps

# Register your models here.

admin.site.register(User)
admin.site.register(Institution)
admin.site.register(UserRole)
admin.site.register(Group)
admin.site.register(Announcement)
admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(Chapter)
admin.site.register(Exercise)
admin.site.register(ExerciseSubmission)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(Report)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)
