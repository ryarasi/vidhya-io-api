# Generated by Django 3.2.3 on 2023-08-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0023_user_credit_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.CharField(default='0', max_length=50),
        ),
    ]
