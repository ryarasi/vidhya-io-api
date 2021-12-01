import channels_graphql_ws
import graphene
from graphql_jwt.decorators import login_required
from .gqTypes import CriterionResponseType, CriterionType, InstitutionType, ProjectType, UserType, UserRoleType, GroupType, AnnouncementType, CourseType, CourseSectionType, ChapterType, ExerciseType, ExerciseKeyType, ExerciseSubmissionType, ReportType, ChatType, ChatMessageType


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
        return NotifyInstitution(institution=payload["institution"], method=payload["method"])


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
        return NotifyUser(user=payload["user"], method=payload["method"])


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
        return NotifyUserRole(user_role=payload["user_role"], method=payload["method"])


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
        return NotifyGroup(group=payload["group"], method=payload["method"])


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
        return NotifyAnnouncement(announcement=payload["announcement"], method=payload["method"])

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
        return NotifyProject(proejct=payload["project"], method=payload["method"])


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
        return NotifyCourse(course=payload["course"], method=payload["method"])


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
        return NotifyCourseSection(course_section=payload["course_section"], method=payload["method"])


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
        return NotifyChapter(chapter=payload["chapter"], method=payload["method"])


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
        return NotifyExercise(exercise=payload["exercise"], method=payload["method"])

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
        return NotifyCriterion(criterion=payload["criterion"], method=payload["method"])

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
        return NotifyCriterion(criterion_response=payload["criterion_response"], method=payload["method"])



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
        return NotifyExerciseKey(exerciseKey=payload["exercise_key"], method=payload["method"])



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
        return NotifyExerciseSubmission(exercise_submission=payload["exercise_submission"], method=payload["method"])


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
        return NotifyReport(report=payload["report"], method=payload["method"])


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
        return NotifyChat(chat=payload["chat"], method=payload["method"])


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
        return NotifyChatMessage(chat_message=payload["chat_message"], method=payload["method"])


class Subscription(graphene.ObjectType):
    notify_institution = NotifyInstitution.Field()
    notify_user = NotifyUser.Field()
    notify_user_role = NotifyUserRole.Field()
    notify_group = NotifyGroup.Field()
    notify_announcement = NotifyAnnouncement.Field()
    notify_project = NotifyProject.Field()
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
