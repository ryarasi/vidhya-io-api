# Generated by Django 3.2.3 on 2022-01-26 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0005_announcement_blurb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='message',
            field=models.CharField(max_length=10000),
        ),
    ]
