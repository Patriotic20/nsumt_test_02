from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.faculty.model import Faculty
    from models.student.model import Student
    from models.quiz.model import Quiz
    from models.results.model import Result
    from models.group_teachers.model import GroupTeacher


class Group(Base, IdIntPk, TimestampMixin):
    __tablename__ = "groups"
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"))
    
    name: Mapped[str] = mapped_column(String(50), unique=True)

    faculty: Mapped["Faculty"] = relationship(
        "Faculty", 
        back_populates="groups"
    )
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="group"
    )

    quizzes: Mapped[list["Quiz"]] = relationship(
        "Quiz", 
        back_populates="group"
    )

    results: Mapped[list["Result"]] = relationship(
        "Result", 
        back_populates="group"
    )

    group_teachers: Mapped[list["GroupTeacher"]] = relationship(
        "GroupTeacher",
        back_populates="group",
        cascade="all, delete-orphan"
    )



    def __str__(self):
        return self.name