# Generated by Django 3.2.3 on 2023-09-07 07:40

from django.db import migrations, models
import vidhya.models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0024_course_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseparticipant',
            name='audit',
            field=models.BooleanField(default=False, verbose_name=vidhya.models.User),
        ),
    ]
