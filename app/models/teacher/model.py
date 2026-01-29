from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.kafedra.model import Kafedra
    from models.subject.model import Subject
    from models.subject_teacher.model import SubjectTeacher


class Teacher(Base, IdIntPk, TimestampMixin):
    __tablename__ = "teachers"
    kafedra_id: Mapped[int] = mapped_column(ForeignKey("kafedras.id"))

    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    third_name: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column(unique=True)

    kafedra: Mapped["Kafedra"] = relationship("Kafedra", back_populates="teachers")

    subject_teachers: Mapped[list["SubjectTeacher"]] = relationship(
        "SubjectTeacher",
        back_populates="teacher",
    )

    def __str__(self):
        return self.name