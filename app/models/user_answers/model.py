from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.mixins.id_int_pk import IdIntPk
from models.mixins.time_stamp_mixin import TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user.model import User
    from models.quiz.model import Quiz
    from models.question.model import Question

class UserAnswers(Base, IdIntPk, TimestampMixin):
    __tablename__ = "user_answers"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("quizzes.id", ondelete="SET NULL"), nullable=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id", ondelete="SET NULL"), nullable=True)
    answer: Mapped[str] = mapped_column(String(255), nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", backref="user_answers")
    quiz: Mapped["Quiz"] = relationship("Quiz", backref="user_answers")
    question: Mapped["Question"] = relationship("Question", backref="user_answers")

    def __str__(self):
        return f"UserAnswer {self.id} - {self.answer}"