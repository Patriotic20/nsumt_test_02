from typing import TYPE_CHECKING

from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.role.model import Role


class Permission(Base, IdIntPk, TimestampMixin):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(50), unique=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
        overlaps="role_permissions,role,permission",
    )

    def __str__(self):
        return self.name
