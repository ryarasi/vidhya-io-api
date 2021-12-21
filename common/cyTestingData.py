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
  }
}
