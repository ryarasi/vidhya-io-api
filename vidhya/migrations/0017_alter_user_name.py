# Generated by Django 3.2.3 on 2021-08-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0016_auto_20210830_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
