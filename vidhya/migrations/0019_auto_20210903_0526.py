# Generated by Django 3.2.3 on 2021-09-03 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0004_load_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='recipients_global',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='announcement',
            name='recipients_institution',
            field=models.BooleanField(default=False),
        ),
    ]
