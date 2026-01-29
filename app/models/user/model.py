from typing import TYPE_CHECKING

from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.role.model import Role
    from models.student.model import Student
    from models.question.model import Question
    from models.quiz.model import Quiz
    from models.results.model import Result


class User(Base, IdIntPk, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary="user_roles", back_populates="users", overlaps="user_roles"
    )

    student: Mapped["Student"] = relationship("Student", back_populates="user")

    questions: Mapped[list["Question"]] = relationship(
        "Question", 
        back_populates="user"
    )

    quizzes: Mapped[list["Quiz"]] = relationship(
        "Quiz", 
        back_populates="user"
    )

    results: Mapped[list["Result"]] = relationship(
        "Result", 
        back_populates="user"
    )

    def __str__(self):
        return self.username
