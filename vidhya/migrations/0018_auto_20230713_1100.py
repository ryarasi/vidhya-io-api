# Generated by Django 3.2.3 on 2023-07-13 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0017_institution_coordinator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(default='0000000000', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.CharField(default='NA', max_length=300),
        ),
    ]
