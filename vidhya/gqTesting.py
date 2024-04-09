import graphene
from graphene_django.types import ObjectType
from vidhya.models import Announcement, Course, CourseParticipant, EmailOTP, ExerciseSubmission, Group, User
from django.conf import settings


EXISTING_DATA = {
  "institution": {
    "id": 1,
    "name": "Shuddhi Vidhya",
    "code": "shuddhividhya",
    "public": False,
    "location": "Chennai",
    "city": "Chennai",
    "website": "https://shuddhitrust.org",
    "phone": None,
    "logo": "https://i.imgur.com/dPO1MlY.png",
    "bio": "Committed to doing what is necessary",
    "invitecode": "9301911365",
    "searchField": None,
    "active": True,
    "created_at": "2021-07-25T11:32:16.488Z",
    "updated_at": "2021-07-25T11:32:16.488Z"
  },
  "admin": {
    "id": 2,
    "password": "testpassword",
    "last_login": "2021-09-01T05:58:08Z",
    "is_superuser": True,
    "username": "testadmin",
    "first_name": "Test",
    "last_name": "Admin",
    "is_staff": True,
    "is_active": True,
    "date_joined": "2021-09-01T05:57:54Z",
    "name": "Test Admin",
    "email": "test.admin@gmail.com",
    "avatar": "https://res.cloudinary.com/svidhya/image/upload/v1631089294/egxbbxth7keokyjxwajl.jpg",
    "institution": 1,
    "role": "Super Admin",
    "title": "Test User, Shuddhi Vidhya",
    "bio": "Test admin from Shuddhi Vidhya",
    "membership_status": "AP",
    "searchField": "testadmin, shuddhi vidhyai i am a test admin!apshuddhi vidhya",
    "last_active": "2021-09-05T12:08:21.131Z",
    "active": True,
    "created_at": "2021-09-01T05:57:54.816Z",
    "updated_at": "2021-10-08T15:26:39.509Z",
    "groups": [],
    "user_permissions": []
  },
  "learner": {
    "id": 3,
    "password": "testpassword",
    "last_login": None,
    "is_superuser": False,
    "username": "learner",
    "first_name": "Learner",
    "last_name": "User",
    "is_staff": False,
    "is_active": True,
    "date_joined": "2021-09-02T12:56:14.210Z",
    "name": "Learner User",
    "email": "learner.user@gmail.com",
    "avatar": "https://i.imgur.com/KHtECqa.png",
    "institution": 1,
    "role": "Learner",
    "title": "Test Learner Account",
    "bio": "Just a test account to look at learners perspective",
    "membership_status": "AP",
    "searchField": "learnerusertest accountjust a test account to look at learners perspectiveapshuddhi vidhya",
    "last_active": "2021-09-02T12:56:14.210Z",
    "active": True,
    "created_at": "2021-09-02T12:56:14.394Z",
    "updated_at": "2021-09-28T10:44:22.462Z",
    "groups": [],
    "user_permissions": []
  },
  "course": {
    "id": 2,
    "title": "Web Development Course",
    "blurb": "This course aims to help you learn how to build simple static websites using HTML and CSS",
    "description": "Learn HTML and CSS, the fundamental tools used to build any website. With this knowledge you will have the necessary foundation to learn more advanced concepts of web development. ",
    "instructor": 2,
    "start_date": "2021-09-01T18:30:00.000Z",
    "end_date": None,
    "credit_hours": 3,
    "pass_score_percentage": 100,
    "pass_completion_percentage": 75,
    "status": "PU",
    "searchField": "web development coursethis course aims to help you learn how to build simple static websites using html and csslearn html and css, the fundamental tools used to build any website. with this knowledge you will have the necessary foundation to learn more advanced concepts of web development. ",
    "active": True,
    "created_at": "2021-08-30T13:07:50.637Z",
    "updated_at": "2021-11-29T12:46:36.310Z"
  },
  "newUser": {
    "id": None,
    "password": "testpassword",
    "last_login": None,
    "is_superuser": False,
    "username": "newuser",
    "first_name": "New",
    "last_name": "User",
    "is_staff": False,
    "is_active": True,
    "date_joined": "2021-09-02T12:56:14.210Z",
    "name": "New User",
    "email": "new.user@gmail.com",
    "avatar": "https://i.imgur.com/KHtECqa.png",
    "institution": 1,
    "role": "Learner",
    "title": "New User Account",
    "bio": "A new account",
    "membership_status": "UI"
  },
  "newAnnouncement": {
    "id": None,
    "title": "New Test Announcement",
    "author": 2,
    "message": "This is a test message for the test announcement",
    "institution": 1,
    "recipients_global": True
  },
  "newGroup": {
    "id": None,
    "name": "New Test Group",
    "avatar": "https://i.imgur.com/hNdMk4c.png",
    "description": "This is a test message for the test announcement",
    "institution": 1,
    "group_type": "CL"
  }
}


# This file contains queries dedicated for automated testing purposes

class OkResponse(graphene.ObjectType):
    ok = graphene.Boolean()
class EmailOtpResponse(graphene.ObjectType):
    # emailOtp = graphene.List()
    email = graphene.String()
    id = graphene.ID()
    otp = graphene.String()
    verified = graphene.Boolean()
    
class EmptyQuery(ObjectType):
    pass


class Query(ObjectType):

    # Automated Testing related queries
    cy_delete_new_user = graphene.Field(OkResponse)
    cy_fetch_otp = graphene.Field(EmailOtpResponse,email=graphene.String())
    cy_create_global_announcement = graphene.Field(OkResponse)
    cy_delete_global_announcement = graphene.Field(OkResponse)
    cy_create_learner_group = graphene.Field(OkResponse)
    cy_delete_learner_group = graphene.Field(OkResponse)    
    cy_add_learner_to_course = graphene.Field(OkResponse)
    cy_clear_learner_exercise_submissions = graphene.Field(OkResponse)

    def resolve_cy_delete_new_user(root, info, **kwargs):
        ok = False
        if settings.ENABLED_AUTOMATED_TESTING:
            newUserUsername = EXISTING_DATA['newUser']['username']
            print('new user => ', newUserUsername)
            try:
                newuser = User.objects.get(username=newUserUsername)
                print('newuser => ', newuser)
                newuser.delete()
                ok = True
            except:
                pass
        response = OkResponse(ok=ok)
        return response
    
    def resolve_cy_fetch_otp(root, info, email, **kwargs):
        ok = False
        otp = None
        # email='logicabc@mail.com'
        print('resolve_cy_fetch_generate_otp',email)
        if settings.ENABLED_AUTOMATED_TESTING:
           try: 
               email_otp_record = EmailOTP.objects.get(email=email)
               
               ok = True
           except:
               pass
        print('email_otp_record', email_otp_record)      
        if email_otp_record  is not None:
            return email_otp_record 
        else:
            return None

    def resolve_cy_fetch_otp_password(root, info, email, **kwargs):
        ok = False
        otp = None
        # email='logicabc@mail.com'
        print('resolve_cy_fetch_generate_otp',email)
        if settings.ENABLED_AUTOMATED_TESTING:
           try: 
               email_otp_record = EmailOTP.objects.get(email=email)
               
               ok = True
           except:
               pass
        print('email_otp_record', email_otp_record)      
        if email_otp_record  is not None:
            return email_otp_record 
        else:
            return None    

    def resolve_cy_create_global_announcement(root, info, **kwargs):
        ok = False
        if settings.ENABLED_AUTOMATED_TESTING:
            input = EXISTING_DATA['newAnnouncement']
            new_announcement_instance = Announcement(title=input['title'], author_id=input['author'], message=input['message'],
                                             institution_id=input['institution'], recipients_global=input['recipients_global'])
            try:
                new_announcement_instance.save()
                ok = True
            except:
                pass
        response = OkResponse(ok=ok)
        return response

    def resolve_cy_delete_global_announcement(root, info, **kwargs):
        ok = True
        if settings.ENABLED_AUTOMATED_TESTING:
            input = EXISTING_DATA['newAnnouncement']
            all_announcements = Announcement.objects.filter(title=input['title'], author_id=input['author'], message=input['message'],
                                             institution_id=input['institution'], recipients_global=input['recipients_global'])
            for announcement in all_announcements:
                try:
                    announcement.delete()
                except:
                    ok = False
                    pass
        response = OkResponse(ok=ok)
        return response

    def resolve_cy_create_learner_group(root, info, **kwargs):
        ok = False
        if settings.ENABLED_AUTOMATED_TESTING:
            input = EXISTING_DATA['newGroup']
            learner = EXISTING_DATA['learner']
            new_announcement_instance = Group(name=input['name'], description=input['description'], institution_id=input['institution'], avatar=input['avatar'], group_type=input['group_type'])
            try:
                new_announcement_instance.save()
                new_announcement_instance.members.add(learner['id'])
                ok = True
            except:
                pass
        response = OkResponse(ok=ok)
        return response

    def resolve_cy_delete_learner_group(root, info, **kwargs):
        ok = True
        if settings.ENABLED_AUTOMATED_TESTING:
            input = EXISTING_DATA['newGroup']


            all_groups = Group.objects.filter(name=input['name'], description=input['description'], institution_id=input['institution'], avatar=input['avatar'], group_type=input['group_type'])
            for group in all_groups:
                try:
                    group.delete()
                except:
                    ok = False
                    pass
        response = OkResponse(ok=ok)
        return response

    def resolve_cy_add_learner_to_course(root, info, **kwargs):

        ok = True
        if settings.ENABLED_AUTOMATED_TESTING:
            learner_data = EXISTING_DATA['learner']
            course_data = EXISTING_DATA['course']
            course=Course.objects.get(pk=course_data['id'])
            learner = User.objects.get(pk=learner_data['id'])
            courses = Course.objects.all()
            for course in courses:
                course.participants.remove(learner.id)
            course.participants.add(learner.id)
            course.save()
            ok=True
            # except:
            #     ok=False
            # Adding in one course
        response = OkResponse(ok=ok)
        return response


    def resolve_cy_clear_learner_exercise_submissions(root, info, **kwargs):
        ok = True
        if settings.ENABLED_AUTOMATED_TESTING:
            learner_data = EXISTING_DATA['learner']
            submissions = ExerciseSubmission.objects.filter(participant_id=learner_data['id'])
            for submission in submissions:
                try:
                    submission.delete()
                except:
                    ok=False

            ok=True
            # except:
            #     ok=False
            # Adding in one course
        response = OkResponse(ok=ok)
        return response