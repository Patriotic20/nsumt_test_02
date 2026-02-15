from fastapi import HTTPException, status
from app.models.results.model import Result
from app.models.quiz.model import Quiz
from app.models.user.model import User
from sqlalchemy import func, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .schemas import (
    GeneralStatisticsResponse,
    QuizStatisticsResponse,
    UserStatisticsResponse,
)


class StatisticsRepository:
    async def get_general_stats(
        self, session: AsyncSession
    ) -> GeneralStatisticsResponse:
        # Total students tested (unique users in results)
        students_stmt = select(func.count(distinct(Result.user_id)))
        students_res = await session.execute(students_stmt)
        total_students = students_res.scalar() or 0

        # Total quizzes taken (total count of results)
        total_stmt = select(func.count(Result.id))
        total_res = await session.execute(total_stmt)
        total_quizzes = total_res.scalar() or 0

        # System average grade
        avg_stmt = select(func.avg(Result.grade))
        avg_res = await session.execute(avg_stmt)
        avg_grade = avg_res.scalar() or 0.0

        return GeneralStatisticsResponse(
            total_students_tested=total_students,
            total_quizzes_taken=total_quizzes,
            system_average_grade=float(avg_grade)
        )

    async def get_quiz_stats(
        self, session: AsyncSession, quiz_id: int
    ) -> QuizStatisticsResponse:
        # Check if quiz exists
        q_stmt = select(Quiz).where(Quiz.id == quiz_id)
        q_res = await session.execute(q_stmt)
        quiz = q_res.scalar_one_or_none()
        
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        # Aggregate stats
        stats_stmt = select(
            func.count(Result.id).label("times_taken"),
            func.avg(Result.grade).label("avg_grade"),
            func.max(Result.grade).label("max_grade"),
            func.min(Result.grade).label("min_grade")
        ).where(Result.quiz_id == quiz_id)
        
        res = await session.execute(stats_stmt)
        stats = res.one()

        return QuizStatisticsResponse(
            quiz_id=quiz.id,
            title=quiz.title,
            times_taken=stats.times_taken or 0,
            average_grade=float(stats.avg_grade or 0.0),
            highest_grade=stats.max_grade or 0,
            lowest_grade=stats.min_grade or 0
        )

    async def get_user_stats(
        self, session: AsyncSession, user_id: int
    ) -> UserStatisticsResponse:
        content_stmt = select(User).where(User.id == user_id)
        user_res = await session.execute(content_stmt)
        user = user_res.scalar_one_or_none()

        if not user:
             raise HTTPException(status_code=404, detail="User not found")
             
        stats_stmt = select(
            func.count(Result.id).label("quizzes_taken"),
            func.avg(Result.grade).label("avg_grade")
        ).where(Result.user_id == user_id)
        
        res = await session.execute(stats_stmt)
        stats = res.one()

        return UserStatisticsResponse(
            user_id=user.id,
            full_name=user.username, # Basic fallback, usually construct from profile if available or join teacher/student tables
            quizzes_taken=stats.quizzes_taken or 0,
            average_grade=float(stats.avg_grade or 0.0)
        )

get_statistics_repository = StatisticsRepository()
