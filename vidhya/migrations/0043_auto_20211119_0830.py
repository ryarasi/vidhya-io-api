# Generated by Django 3.2.3 on 2021-11-19 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0042_completedchapters_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedchapters',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='completedchapters',
            name='scored_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='completedchapters',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
    ]
