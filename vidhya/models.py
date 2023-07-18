from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import PROTECT
from common.utils import random_number_with_N_digits, generate_otp
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import CharField, IntegerField
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings
# from django.db.models import JSONField

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    name = models.CharField(max_length=100, default='Uninitialized User')
    email = LowercaseEmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True,
                              null=True, default=settings.DEFAULT_AVATARS['USER'])
    institution = models.ForeignKey(
        'Institution', on_delete=models.PROTECT, blank=True, null=True)
    role = models.ForeignKey(
        'UserRole', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300,blank=True,null=True)
    city = models.CharField(max_length=300,blank=True,null=True)
    pincode = models.CharField(max_length=150,blank=True,null=True)
    state = models.CharField(max_length=300,default='NA',null=False)
    country = models.CharField(max_length=300,default="India",null=False)
    dob = models.DateTimeField(null=True,blank=True)
    mobile = models.CharField(default="0000000000",max_length=20,null=True)
    phone = models.CharField(default="0000000000",max_length=20, blank = True,null=True)
    designation = models.CharField(max_length=300,default="NA")
    manualLogin = models.BooleanField(default="False")
    googleLogin = models.BooleanField(default="False")
    
    # invitecode = models.ForeignKey('Institution', on_delete = models.PROTECT, blank=True, null=True)
    class StatusChoices(models.TextChoices):
        UNINITIALIZED = 'UI', _('UNINITIALIZED')
        PENDINIG = "PE", _('PENDIING')
        APPROVED = "AP", _('APPROVED')
        SUSPENDED = "SU", _('SUSPENDED')
    # End of Type Choices

    membership_status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.UNINITIALIZED)
    chapters = models.ManyToManyField('Chapter', through='CompletedChapters', through_fields=('participant', 'chapter'), blank=True)
    courses = models.ManyToManyField('Course', through='CompletedCourses', through_fields=('participant', 'course'), blank=True)
    announcements = models.ManyToManyField('Announcement', through='AnnouncementsSeen', through_fields=('user','announcement'), blank=True)
    projects_clapped = models.ManyToManyField('Project', through="ProjectClap", through_fields=('user', 'project'),blank=True)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    last_active = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return f'{self.name}' 

class EmailOTP(models.Model):
    email = LowercaseEmailField(blank=False, max_length=255)
    def generate_otp():
        return generate_otp()
    otp = models.CharField(max_length=10, validators=[
                                  MinLengthValidator(10)], unique=True, default=generate_otp)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CompletedChapters(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    status=models.CharField(max_length=2, default='SU')
    scored_points = models.IntegerField(default=0)
    total_points=models.IntegerField(default=0)
    percentage=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.chapter.title}' 

class CompletedCourses(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.course.title}'

class AnnouncementsSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.announcement.title}'


class UserRole(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=500,)
    priority = models.IntegerField() # Lower the number higher the priority

    def default_permissions():
        return {}
    permissions = JSONField(default=default_permissions)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 



class Institution(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20,unique=True)
    public = models.BooleanField(default=False)
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    logo = models.CharField(
        max_length=250, blank=True, null=True, default=settings.DEFAULT_AVATARS['INSTITUTION'])
    bio = models.CharField(max_length=300, blank=True, null=True)
    verified = models.BooleanField(default=False)
    coordinator = models.ForeignKey(User,related_name="institutionCoordinators",on_delete=models.PROTECT, blank=True, null=True)
    
    class InstitutionTypeChoices(models.TextChoices):
        SCHOOL = "SC", _('School')
        COLLEGE = "CL", _('College')
        COMPANY = "CO", _('Company')
        ORGANIZATION = "OR", _('Organization')

    institution_type = models.CharField(max_length=2,
        choices=InstitutionTypeChoices.choices,
        default=InstitutionTypeChoices.SCHOOL,
    ) 
    designations = models.CharField(max_length=300,blank=True,null=True)
    address = models.CharField(max_length=300,blank=True,null=True)
    pincode = models.CharField(max_length=150,blank=True,null=True)
    state = models.CharField(max_length=300,blank=True,null=True)
    country = models.CharField(max_length=300,default="India",null=False)
    dob = models.DateTimeField(default=timezone.now)

    def generate_invitecode():
        return random_number_with_N_digits(10)

    invitecode = models.CharField(max_length=10, validators=[
                                  MinLengthValidator(10)], unique=True, default=generate_invitecode)
    searchField = models.CharField(max_length=900, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    avatar = models.CharField(
        max_length=250, blank=True, null=True, default=settings.DEFAULT_AVATARS['GROUP'])
    searchField = models.CharField(max_length=400, blank=True, null=True)

    # Type Choices
    class TypeChoices(models.TextChoices):
        CLASS = "CL", _('Class')
        TEAM = "TE", _('Team')
        COORDINATiON = "CO", _('Coordination')
    # End of Type Choices

    group_type = models.CharField(
        max_length=2, choices=TypeChoices.choices, default=TypeChoices.TEAM)
    admins = models.ManyToManyField(User, related_name="adminInGroups", through="GroupAdmin", through_fields=(
        'group', 'admin'), blank=True)
    members = models.ManyToManyField(
        User, related_name="memberInGroups", through='GroupMember', through_fields=('group', 'member'), blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 


class GroupAdmin(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Group {self.group.name}, member {self.admin.name}' 



class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Group {self.group.name}, member {self.member.name}' 

class Project(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, related_name="projectAuthor", on_delete=models.PROTECT)
    description = models.CharField(max_length=2000)
    link = models.CharField(max_length=1000)
    course = models.ForeignKey('Course', null=True, blank=True, on_delete=models.PROTECT)
    contributors = models.ManyToManyField(User, through="ProjectContributor", through_fields=('project', 'contributor'), blank=True)
    public = models.BooleanField(default=True)
    claps = models.IntegerField(default=1)
    clapsBy = models.ManyToManyField(User, related_name='clappers', through='ProjectClap', through_fields=('project','user'),blank=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectClap(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project.claps}'        

class ProjectContributor(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    role = CharField(max_length=100, null=True, blank=True)
    description = CharField(max_length=5000, null=True, blank=True)


class Announcement(models.Model):
    title = models.CharField(max_length=80)
    author = models.ForeignKey(
        User, related_name="announcementAuthor", on_delete=models.PROTECT)
    public = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    image = models.CharField(max_length=250, blank=True,
                              null=True)
    blurb = models.CharField(max_length=500, blank=True, null=True)
    message = models.CharField(max_length=10000)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    recipients_global = models.BooleanField(default=False)
    recipients_institution = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, through="AnnouncementGroup", through_fields=(
        'announcement', 'group'), blank=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

class AnnouncementGroup(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'Announcement {self.announcement.title}, Group {self.group.name}'


class Course(models.Model):
    index = models.CharField(max_length=5, default='0.0')
    title = models.CharField(max_length=80)
    blurb = models.CharField(max_length=150)
    video = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1000)
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)
    institutions = models.ManyToManyField(Institution, through="CourseInstitution", through_fields=(
        'course', 'institution'), blank=True)
    participants = models.ManyToManyField(
        User, through="CourseParticipant", related_name="participants", through_fields=('course', 'participant'), blank=True)
    graders = models.ManyToManyField(
        User, through="CourseGrader", related_name="graders", through_fields=('course', 'grader'), blank=True)
    mandatory_prerequisites = models.ManyToManyField(
        'Course', related_name="required_courses",through='MandatoryRequiredCourses', through_fields=('course', 'requirement'), blank=True)
    recommended_prerequisites = models.ManyToManyField(
        'Course', related_name="optional_courses",through='OptionalRequiredCourses',  through_fields=('course', 'optional'), blank=True)
    start_date = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.CharField(max_length=100, blank=True, null=True)
    credit_hours = models.IntegerField(blank=True, null=True)
    pass_score_percentage = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
     )
    pass_completion_percentage = models.IntegerField(default=75, validators=[MaxValueValidator(100), MinValueValidator(1)])

    # Start of setting up status choices
    class StatusChoices(models.TextChoices):
        DRAFT = 'DR', _('DRAFT')
        PUBLISHED = "PU", _('PUBLISHED')
        ARCHIVED = "AR", _('ARCHIVED')
    # End of status choices

    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.DRAFT)


    searchField = models.CharField(max_length=5000, blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class MandatoryRequiredCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Course, related_name="requirement", on_delete=models.CASCADE)

class OptionalRequiredCourses(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    optional = models.ForeignKey(Course, related_name="optional", on_delete=models.CASCADE)


class CourseInstitution(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.course.title}'


class CourseParticipant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Course {self.course.title}, Participant {self.participant.name}'

class CourseGrader(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Course {self.course.title}, Grader {self.grader.name}'

class CourseSection(models.Model):
    title = models.CharField(max_length=80)
    index = models.IntegerField(default=-1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'


class Chapter(models.Model):
    title = models.CharField(max_length=80)
    instructions = models.CharField(max_length=2000)
    index = models.IntegerField(default=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(
        CourseSection, on_delete=models.DO_NOTHING, blank=True, null=True)
    prerequisites = models.ManyToManyField(
        'Chapter', related_name="required",through='MandatoryChapters', through_fields=('chapter', 'requirement'), blank=True)        
    due_date = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(default=0)

    class StatusChoices(models.TextChoices):
        DRAFT = 'DR', _('DRAFT')
        PUBLISHED = "PU", _('PUBLISHED')     
    # End of Type Choices

    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
        
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

class MandatoryChapters(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    requirement = models.ForeignKey(Chapter, related_name="requirement", on_delete=models.CASCADE)

class Exercise(models.Model):
    prompt = models.CharField(max_length=2000)
    index = models.IntegerField(default=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class QuestionTypeChoices(models.TextChoices):
        OPTIONS = 'OP', _('OPTIONS')
        DESCRIPTION = "DE", _('DESCRIPTION')
        IMAGE = "IM", _('IMAGE')
        LINK = "LI", _('LINK')
    # End of Type Choices

    question_type = models.CharField(
        max_length=2, choices=QuestionTypeChoices.choices, default=QuestionTypeChoices.OPTIONS)
    required = models.BooleanField(default=True)
    options = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.prompt}'

class Criterion(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    points = models.IntegerField()
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    active = models.BooleanField(default=True)

class CriterionResponse(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    exercise_submission = models.ForeignKey('ExerciseSubmission', on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    remarker = models.ForeignKey(User, related_name="remarker", null=True, blank=True, on_delete=models.DO_NOTHING)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    active = models.BooleanField(default=True)

class ExerciseKey(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    valid_option = models.CharField(
        max_length=200, blank=True, null=True)
    valid_answers = ArrayField(models.CharField(max_length=5000, blank=True, null=True), blank=True, null=True)
    reference_link = models.CharField(max_length=500, blank=True, null=True)
    reference_images = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ExerciseSubmission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    option = models.CharField(
        max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=5000, blank=True, null=True)
    link = models.CharField(max_length=5000, blank=True, null=True)
    images = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True)

    percentage = models.IntegerField(blank=True, null=True)

    class StatusChoices(models.TextChoices):
        PENDING = 'PE', _('PENDING')
        SUBMITTED = "SU", _('SUBMITTED')
        GRADED = "GR", _('GRADED')
        RETURNED = "RE", _('RETURNED')
        FLAGGED = "FL", _('FLAGGED')
    # End of Type Choices

    status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    flagged = models.BooleanField(default=False)
    grader = models.ForeignKey(User, related_name="grader", blank=True, null=True, on_delete=models.DO_NOTHING)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubmissionHistory(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.CharField(
        max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=5000, blank=True, null=True)
    link = models.CharField(max_length=5000, blank=True, null=True)
    images = ArrayField(models.CharField(
        max_length=200, blank=True), blank=True, null=True)
    points = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True)

    def default_rubric():
        return []
    rubric = JSONField(default=default_rubric)
    
    status = models.CharField(
        max_length=2, choices=ExerciseSubmission.StatusChoices.choices, default=ExerciseSubmission.StatusChoices.PENDING)
    flagged = models.BooleanField(default=False)
    grader = models.ForeignKey(User, related_name="grader_past", blank=True, null=True, on_delete=models.DO_NOTHING)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Report(models.Model):
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    # This will be calculated on grading by dividing the number of graded exercise submissions by required exercises * 100
    completed = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Issue(models.Model):
    link = models.CharField(max_length=5000)
    description = models.CharField(max_length=2000)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    resource_id = models.CharField(max_length=100, blank=True, null=True)

    class ResourceTypeChoices(models.TextChoices):
        USER = 'US', _('USER')
        PROJECT = "PR", _('PROJECT')
        INSTITUTION = "IN", _('INSTITUTION')
        SUBMISSION = "SU", _('SUBMISSION')
        COURSE = "CO", _('COURSE')
        CHAPTER = 'CH', _('CHAPTER')
    # End of Type Choices

    resource_type = models.CharField(
        max_length=2, choices=ResourceTypeChoices.choices, default=ResourceTypeChoices.USER)
    reporter = models.ForeignKey(
        User, related_name="issueReporter", on_delete=models.DO_NOTHING, blank=True, null=True)
    guest_name = models.CharField(max_length=100, blank=True, null=True)
    guest_email= LowercaseEmailField(max_length=255, blank=True, null=True)
    screenshot = models.CharField(max_length=250, blank=True, null=True)

    class IssueStatusChoices(models.TextChoices):
        PENDING = 'PE', _('PENDING')
        RESOLVED = "RE", _('RESOLVED')
        DUPLICATE = "DU", _('GRADED')
        NO_ACTION = "NO", _('NO_ACTION')
    # End of Type Choices

    status = models.CharField(
        max_length=2, choices=IssueStatusChoices.choices, default= IssueStatusChoices.PENDING)
    resolver = models.ForeignKey(User, related_name="issueResolver", on_delete=models.DO_NOTHING, blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    searchField = models.CharField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, blank=True, null=True)
    individual_member_one = models.ForeignKey(
        User, related_name="chat_member_one", on_delete=models.CASCADE, blank=True, null=True)
    individual_member_two = models.ForeignKey(
        User, related_name="chat_member_two", on_delete=models.CASCADE, blank=True, null=True)

    # Type Choices
    class TypeChoices(models.TextChoices):
        INDIVIDUAL = "IL", _('Individual')
        GROUP = "GP", _('Group')
    # End of Type Choices

    chat_type = models.CharField(
        max_length=2, choices=TypeChoices.choices, default=TypeChoices.INDIVIDUAL)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)
    message = models.CharField(max_length=1000)
    author = models.ForeignKey(
        User, related_name="chatAuthor", on_delete=models.DO_NOTHING)
    seenBy = models.ForeignKey(
        User, related_name="chatSeenBy", on_delete=models.PROTECT, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.message}'

# For file uploads


class File(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name
