# Generated by Django 3.2.3 on 2021-07-27 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0005_auto_20210727_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercisefileattachment',
            name='participant',
        ),
    ]
