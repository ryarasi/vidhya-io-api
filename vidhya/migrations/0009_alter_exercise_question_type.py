# Generated by Django 3.2.3 on 2021-08-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0008_delete_exercisefileattachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='question_type',
            field=models.CharField(choices=[('OP', 'OPTIONS'), ('DE', 'DESCRIPTION'), ('IM', 'IMAGE'), ('LI', 'LINK')], default='OP', max_length=2),
        ),
    ]
