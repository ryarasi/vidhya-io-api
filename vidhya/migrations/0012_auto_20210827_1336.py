# Generated by Django 3.2.3 on 2021-08-27 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vidhya', '0011_auto_20210827_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='mandatory_prerequisites',
        ),
        migrations.RemoveField(
            model_name='course',
            name='recommended_prerequisites',
        ),
        migrations.CreateModel(
            name='OptionalRequiredCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('optional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='optional', to='vidhya.course')),
            ],
        ),
        migrations.CreateModel(
            name='MandatoryRequiredCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirement', to='vidhya.course')),
            ],
        ),
    ]
