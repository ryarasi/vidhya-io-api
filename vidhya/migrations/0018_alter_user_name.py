# Generated by Django 3.2.3 on 2021-08-30 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0017_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='Uninitialied User', max_length=100),
        ),
    ]
