# Generated by Django 3.2.3 on 2022-01-24 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0003_announcement_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
