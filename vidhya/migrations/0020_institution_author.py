# Generated by Django 3.2.3 on 2023-07-27 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0019_alter_institution_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='institutionAuthor', to=settings.AUTH_USER_MODEL),
        ),
    ]
