import channels_graphql_ws
import graphene
from graphql_jwt.decorators import login_required
from .gqTypes import CriterionResponseType, CriterionType, InstitutionType, IssueType, ProjectType, UserType, UserRoleType, GroupType, AnnouncementType, CourseType, CourseSectionType, ChapterType, ExerciseType, ExerciseKeyType, ExerciseSubmissionType, ReportType, ChatType, ChatMessageType
from vidhya.authorization import rows_accessible, RESOURCES

class NotifyInstitution(channels_graphql_ws.Subscription):
    institution = graphene.Field(InstitutionType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['INSTITUTION'],payload['institution'], payload['method']):
            return NotifyInstitution(institution=payload["institution"], method=payload["method"])
        else:
            return None        


class NotifyUser(channels_graphql_ws.Subscription):
    user = graphene.Field(UserType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['USER'],payload['user'], payload['method']):
            return NotifyUser(user=payload["user"], method=payload["method"])
        else:
            return None        


class NotifyUserRole(channels_graphql_ws.Subscription):
    user_role = graphene.Field(UserRoleType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['USER_ROLE'],payload['user_role'], payload['method']):
            return NotifyUserRole(user_role=payload["user_role"], method=payload["method"])
        else:
            return None


class NotifyGroup(channels_graphql_ws.Subscription):
    group = graphene.Field(GroupType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['GROUP'],payload['group'], payload['method']):
            return NotifyGroup(group=payload["group"], method=payload["method"])
        else:
            return None        


class NotifyAnnouncement(channels_graphql_ws.Subscription):
    announcement = graphene.Field(AnnouncementType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['ANNOUNCEMENT'],payload['announcement'], payload['method']):
            return NotifyAnnouncement(announcement=payload["announcement"], method=payload["method"])
        else:
            return None

class NotifyProject(channels_graphql_ws.Subscription):
    project = graphene.Field(ProjectType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['PROJECT'],payload['project'], payload['method']):
            return NotifyProject(proejct=payload["project"], method=payload["method"])
        else:
            return None        

class NotifyIssue(channels_graphql_ws.Subscription):
    issue = graphene.Field(IssueType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['ISSUE'],payload['issue'], payload['method']):
            return NotifyIssue(proejct=payload["issue"], method=payload["method"])
        else:
            return None


class NotifyCourse(channels_graphql_ws.Subscription):
    course = graphene.Field(CourseType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['COURSE'],payload['course'], payload['method']):
            return NotifyCourse(course=payload["course"], method=payload["method"])
        else:
            return None        


class NotifyCourseSection(channels_graphql_ws.Subscription):
    course_section = graphene.Field(CourseSectionType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['COURSE_SECTION'],payload['course_section'], payload['method']):
            return NotifyCourseSection(course_section=payload["course_section"], method=payload["method"])
        else:
            return None


class NotifyChapter(channels_graphql_ws.Subscription):
    chapter = graphene.Field(ChapterType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['CHAPTER'],payload['chapter'], payload['method']):
            return NotifyChapter(chapter=payload["chapter"], method=payload["method"])
        else:
            return None



class NotifyExercise(channels_graphql_ws.Subscription):
    exercise = graphene.Field(ExerciseType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['EXERCISE'],payload['exercise'], payload['method']):
            return NotifyExercise(exercise=payload["exercise"], method=payload["method"])
        else:
            return None

class NotifyCriterion(channels_graphql_ws.Subscription):
    criterion = graphene.Field(CriterionType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['CRITERION'],payload['criterion'], payload['method']):
            return NotifyCriterion(criterion=payload["criterion"], method=payload["method"])
        else:
            return None        

class NotifyCriterionResponse(channels_graphql_ws.Subscription):
    criterion_response = graphene.Field(CriterionResponseType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        # return NotifyCriterionResponse(criterion_response=payload["criterion_response"], method=payload["method"])
        return



class NotifyExerciseKey(channels_graphql_ws.Subscription):
    exerciseKey = graphene.Field(ExerciseKeyType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['EXERCISE_KEY'],payload['exercise_key'], payload['method']):
            return NotifyExerciseKey(exerciseKey=payload["exercise_key"], method=payload["method"])
        else:
            return None        



class NotifyExerciseSubmission(channels_graphql_ws.Subscription):
    exercise_submission = graphene.Field(ExerciseSubmissionType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['EXERCISE_SUBMISSION'],payload['exercise_submission'], payload['method']):
            return NotifyExerciseSubmission(exercise_submission=payload["exercise_submission"], method=payload["method"])
        else:
            return None

class NotifyReport(channels_graphql_ws.Subscription):
    report = graphene.Field(ReportType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['REPORT'],payload['report'], payload['method']):
            return NotifyReport(report=payload["report"], method=payload["method"])
        else:
            return None

class NotifyChat(channels_graphql_ws.Subscription):
    chat = graphene.Field(ChatType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['CHAT'],payload['chat'], payload['method']):
            return NotifyChat(chat=payload["chat"], method=payload["method"])
        else:
            return None

class NotifyChatMessage(channels_graphql_ws.Subscription):
    chat_message = graphene.Field(ChatMessageType)
    method = graphene.String()
    # class Arguments:

    @staticmethod
    @login_required
    def subscribe(root, info):
        return None

    @staticmethod
    @login_required
    def publish(payload, info):
        if rows_accessible(info.context.user, RESOURCES['CHAT_MESSAGE'],payload['chat_message'], payload['method']):
            return NotifyChatMessage(chat_message=payload["chat_message"], method=payload["method"])
        else:
            return None


class Subscription(graphene.ObjectType):
    notify_institution = NotifyInstitution.Field()
    notify_user = NotifyUser.Field()
    notify_user_role = NotifyUserRole.Field()
    notify_group = NotifyGroup.Field()
    notify_announcement = NotifyAnnouncement.Field()
    notify_project = NotifyProject.Field()
    notify_issue=NotifyIssue.Field()
    notify_course = NotifyCourse.Field()
    notify_course_section = NotifyCourseSection.Field()
    notify_chapter = NotifyChapter.Field()
    notify_exercise = NotifyExercise.Field()
    notify_criterion_response = NotifyCriterionResponse.Field()
    notify_criterion = NotifyCriterion.Field()
    notify_exercise_key = NotifyExerciseKey.Field()
    notify_exercise_submission = NotifyExerciseSubmission.Field()
    notify_report = NotifyReport.Field()
    notify_chat = NotifyChat.Field()
    notify_chat_message = NotifyChatMessage.Field()
