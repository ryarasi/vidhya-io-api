# Generated by Django 3.2.3 on 2024-03-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0029_courseparticipant_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preferred_language',
            field=models.CharField(default='en', max_length=300),
        ),
    ]
