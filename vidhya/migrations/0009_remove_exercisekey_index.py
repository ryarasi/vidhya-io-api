# Generated by Django 3.2.3 on 2021-08-26 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0008_exercisekey_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercisekey',
            name='index',
        ),
    ]
