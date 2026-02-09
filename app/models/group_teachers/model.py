from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.group.model import Group
    from models.teacher.model import Teacher


class GroupTeacher(Base, IdIntPk, TimestampMixin):
    __tablename__ = "group_teachers"
    __table_args__ = (
        UniqueConstraint("group_id", "teacher_id", name="idx_unique_group_teacher"),
    )

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    group: Mapped["Group"] = relationship("Group", back_populates="group_teachers")
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="teacher_groups")

    def __str__(self):
        return f"{self.group_id} - {self.teacher_id}"
