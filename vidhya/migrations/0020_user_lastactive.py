# Generated by Django 3.2.3 on 2021-05-28 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0019_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lastActive',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
