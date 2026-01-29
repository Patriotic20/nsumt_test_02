from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.subject.model import Subject
    from models.teacher.model import Teacher


class SubjectTeacher(Base, IdIntPk, TimestampMixin):
    __tablename__ = "subject_teachers"
    
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    subject: Mapped["Subject"] = relationship("Subject", back_populates="subject_teachers")
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subject_teachers")

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.name}"