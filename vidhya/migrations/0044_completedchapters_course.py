# Generated by Django 3.2.3 on 2021-11-24 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0043_auto_20211119_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedchapters',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vidhya.course'),
            preserve_default=False,
        ),
    ]
