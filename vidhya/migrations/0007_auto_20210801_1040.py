# Generated by Django 3.2.3 on 2021-08-01 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0006_alter_chapter_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='searchField',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='exercisefileattachment',
            name='searchField',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='exercisesubmission',
            name='searchField',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='searchField',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
