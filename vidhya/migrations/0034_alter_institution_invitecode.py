# Generated by Django 3.2.3 on 2021-06-01 04:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0033_alter_institution_invitecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='invitecode',
            field=models.CharField(default=9633385470, max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
