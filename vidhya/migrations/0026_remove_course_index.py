# Generated by Django 3.2.3 on 2023-09-27 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0025_courseparticipant_audit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='index',
        ),
    ]
