from models.permission.view import PermissionView
from models.role.view import RoleView
from models.role_permission.view import RolePermissionView
from models.student.view import StudentView
from models.user.view import UserView
from models.user_role.view import UserRoleView
from models.faculty.view import FacultyView
from models.kafedra.view import KafedraView
from models.group.view import GroupView
from models.teacher.view import TeacherView
from models.subject.view import SubjectView
from models.question.view import QuestionView
from models.quiz.view import QuizView
from models.quiz_questions.view import QuizQuestionView
from models.subject_teacher.view import SubjectTeacherView
from models.results.view import ResultView
from sqladmin import Admin


def register_models(admin: Admin):
    admin.add_view(UserView)
    admin.add_view(RoleView)
    admin.add_view(PermissionView)
    admin.add_view(UserRoleView)
    admin.add_view(RolePermissionView)
    admin.add_view(StudentView)
    admin.add_view(FacultyView)
    admin.add_view(KafedraView)
    admin.add_view(GroupView)
    admin.add_view(TeacherView)
    admin.add_view(SubjectView)
    admin.add_view(QuestionView)
    admin.add_view(QuizView)
    admin.add_view(QuizQuestionView)
    admin.add_view(SubjectTeacherView)
    admin.add_view(ResultView)
