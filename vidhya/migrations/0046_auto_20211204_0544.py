# Generated by Django 3.2.3 on 2021-12-04 05:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0045_auto_20211129_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedchapters',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='completedchapters',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='completedcourses',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='completedcourses',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
