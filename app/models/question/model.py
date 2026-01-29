import random
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.subject.model import Subject
    from models.user.model import User


class Question(Base, IdIntPk, TimestampMixin):
    __tablename__ = "questions"

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    text: Mapped[str] = mapped_column(nullable=False)
    option_a: Mapped[str] = mapped_column(nullable=False)
    option_b: Mapped[str] = mapped_column(nullable=False)
    option_c: Mapped[str] = mapped_column(nullable=False)
    option_d: Mapped[str] = mapped_column(nullable=False)

    subject: Mapped["Subject"] = relationship(
        "Subject", 
        back_populates="questions"
    )

    user: Mapped["User"] = relationship(
        "User", 
        back_populates="questions"
    )
    

    quiz_questions: Mapped[list["QuizQuestion"]] = relationship(
        "QuizQuestion",
        back_populates="question",
    )

    def __str__(self):
        return self.text


    def to_dict(self, randomize_options: bool = True):
        """
        Convert question to dict.
        Randomly shuffles options, but does not show which is correct.
        """
        options = [self.option_a, self.option_b, self.option_c, self.option_d]
        if randomize_options:
            random.shuffle(options)

        return {
            "id": self.id,
            "text": self.text,
            "options": options,
        }