# Generated by Django 3.2.3 on 2021-12-17 12:24

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import vidhya.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(default='Uninitialized User', max_length=100)),
                ('email', vidhya.models.LowercaseEmailField(max_length=255, unique=True)),
                ('avatar', models.CharField(blank=True, default='https://i.imgur.com/KHtECqa.png', max_length=250, null=True)),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('bio', models.CharField(blank=True, max_length=300, null=True)),
                ('membership_status', models.CharField(choices=[('UI', 'UNINITIALIZED'), ('PE', 'PENDIING'), ('AP', 'APPROVED'), ('SU', 'SUSPENDED')], default='UI', max_length=2)),
                ('searchField', models.CharField(blank=True, max_length=600, null=True)),
                ('last_active', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('message', models.CharField(max_length=2000)),
                ('recipients_global', models.BooleanField(default=False)),
                ('recipients_institution', models.BooleanField(default=False)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='announcementAuthor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('instructions', models.CharField(max_length=2000)),
                ('index', models.IntegerField(default=100)),
                ('due_date', models.CharField(blank=True, max_length=100, null=True)),
                ('points', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('DR', 'DRAFT'), ('PU', 'PUBLISHED')], default='DR', max_length=2)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_type', models.CharField(choices=[('IL', 'Individual'), ('GP', 'Group')], default='IL', max_length=2)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('blurb', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('start_date', models.CharField(blank=True, max_length=100, null=True)),
                ('end_date', models.CharField(blank=True, max_length=100, null=True)),
                ('credit_hours', models.IntegerField(blank=True, null=True)),
                ('pass_score_percentage', models.IntegerField(default=100, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('pass_completion_percentage', models.IntegerField(default=75, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('status', models.CharField(choices=[('DR', 'DRAFT'), ('PU', 'PUBLISHED'), ('AR', 'ARCHIVED')], default='DR', max_length=2)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('points', models.IntegerField()),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=2000)),
                ('index', models.IntegerField(default=100)),
                ('question_type', models.CharField(choices=[('OP', 'OPTIONS'), ('DE', 'DESCRIPTION'), ('IM', 'IMAGE'), ('LI', 'LINK')], default='OP', max_length=2)),
                ('required', models.BooleanField(default=True)),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, null=True, size=None)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('avatar', models.CharField(blank=True, default='https://i.imgur.com/hNdMk4c.png', max_length=250, null=True)),
                ('searchField', models.CharField(blank=True, max_length=400, null=True)),
                ('group_type', models.CharField(choices=[('CL', 'Class'), ('TE', 'Team'), ('CO', 'Coordination')], default='TE', max_length=2)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('public', models.BooleanField(default=True)),
                ('location', models.CharField(max_length=50)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('logo', models.CharField(blank=True, default='https://i.imgur.com/dPO1MlY.png', max_length=250, null=True)),
                ('bio', models.CharField(blank=True, max_length=300, null=True)),
                ('invitecode', models.CharField(default=vidhya.models.Institution.generate_invitecode, max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10)])),
                ('searchField', models.CharField(blank=True, max_length=900, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('link', models.CharField(max_length=1000)),
                ('public', models.BooleanField(default=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projectAuthor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=500)),
                ('priority', models.IntegerField()),
                ('permissions', django.contrib.postgres.fields.jsonb.JSONField(default=vidhya.models.UserRole.default_permissions)),
                ('searchField', models.CharField(blank=True, max_length=600, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubmissionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(blank=True, max_length=200, null=True)),
                ('answer', models.CharField(blank=True, max_length=5000, null=True)),
                ('link', models.CharField(blank=True, max_length=5000, null=True)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, null=True, size=None)),
                ('points', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('rubric', django.contrib.postgres.fields.jsonb.JSONField(default=vidhya.models.SubmissionHistory.default_rubric)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('SU', 'SUBMITTED'), ('GR', 'GRADED'), ('RE', 'RETURNED'), ('FL', 'FLAGGED')], default='PE', max_length=2)),
                ('flagged', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.exercise')),
                ('grader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='grader_past', to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.IntegerField(default=0)),
                ('percentage', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.institution')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('contributor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(blank=True, through='vidhya.ProjectContributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vidhya.course'),
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
        migrations.CreateModel(
            name='MandatoryChapters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.chapter')),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirement', to='vidhya.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=5000)),
                ('description', models.CharField(max_length=2000)),
                ('resource_id', models.CharField(blank=True, max_length=100, null=True)),
                ('resource_type', models.CharField(choices=[('US', 'USER'), ('PR', 'PROJECT'), ('IN', 'INSTITUTION'), ('SU', 'SUBMISSION'), ('CO', 'COURSE'), ('CH', 'CHAPTER')], default='US', max_length=2)),
                ('guest_name', models.CharField(blank=True, max_length=100, null=True)),
                ('guest_email', vidhya.models.LowercaseEmailField(blank=True, max_length=255, null=True)),
                ('screenshot', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('RE', 'RESOLVED'), ('DU', 'GRADED'), ('NO', 'NO_ACTION')], default='PE', max_length=2)),
                ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.institution')),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='issueReporter', to=settings.AUTH_USER_MODEL)),
                ('resolver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='issueResolver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.group')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='adminInGroups', through='vidhya.GroupAdmin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vidhya.institution'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='memberInGroups', through='vidhya.GroupMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ExerciseSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(blank=True, max_length=200, null=True)),
                ('answer', models.CharField(blank=True, max_length=5000, null=True)),
                ('link', models.CharField(blank=True, max_length=5000, null=True)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, null=True, size=None)),
                ('points', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('percentage', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('SU', 'SUBMITTED'), ('GR', 'GRADED'), ('RE', 'RETURNED'), ('FL', 'FLAGGED')], default='PE', max_length=2)),
                ('flagged', models.BooleanField(default=False)),
                ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.exercise')),
                ('grader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='grader', to=settings.AUTH_USER_MODEL)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_option', models.CharField(blank=True, max_length=200, null=True)),
                ('valid_answers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=5000, null=True), blank=True, null=True, size=None)),
                ('reference_link', models.CharField(blank=True, max_length=500, null=True)),
                ('reference_images', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, null=True, size=None)),
                ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='CriterionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
                ('searchField', models.CharField(blank=True, max_length=5000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.criterion')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.exercise')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('remarker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='remarker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='criterion',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.exercise'),
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('index', models.IntegerField(default=-1)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseInstitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.institution')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='institutions',
            field=models.ManyToManyField(blank=True, through='vidhya.CourseInstitution', to='vidhya.Institution'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='mandatory_prerequisites',
            field=models.ManyToManyField(blank=True, related_name='required_courses', through='vidhya.MandatoryRequiredCourses', to='vidhya.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', through='vidhya.CourseParticipant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='recommended_prerequisites',
            field=models.ManyToManyField(blank=True, related_name='optional_courses', through='vidhya.OptionalRequiredCourses', to='vidhya.Course'),
        ),
        migrations.CreateModel(
            name='CompletedCourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedChapters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='SU', max_length=2)),
                ('scored_points', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('percentage', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1000)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='chatAuthor', to=settings.AUTH_USER_MODEL)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vidhya.chat')),
                ('seenBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chatSeenBy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vidhya.group'),
        ),
        migrations.AddField(
            model_name='chat',
            name='individual_member_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_member_one', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chat',
            name='individual_member_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chat_member_two', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.course'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, related_name='required', through='vidhya.MandatoryChapters', to='vidhya.Chapter'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='vidhya.coursesection'),
        ),
        migrations.CreateModel(
            name='AnnouncementsSeen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.announcement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.announcement')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vidhya.group')),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='groups',
            field=models.ManyToManyField(blank=True, through='vidhya.AnnouncementGroup', to='vidhya.Group'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vidhya.institution'),
        ),
        migrations.AddField(
            model_name='user',
            name='announcements',
            field=models.ManyToManyField(blank=True, through='vidhya.AnnouncementsSeen', to='vidhya.Announcement'),
        ),
        migrations.AddField(
            model_name='user',
            name='chapters',
            field=models.ManyToManyField(blank=True, through='vidhya.CompletedChapters', to='vidhya.Chapter'),
        ),
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(blank=True, through='vidhya.CompletedCourses', to='vidhya.Course'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vidhya.institution'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vidhya.userrole'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
