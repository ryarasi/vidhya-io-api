# Generated by Django 3.2.3 on 2024-02-15 11:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import vidhya.models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0030_auto_20240213_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title_object',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=vidhya.models.Course.default_title),
        ),
    ]
