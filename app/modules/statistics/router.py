from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from .repository import get_statistics_repository
from .schemas import (
    GeneralStatisticsResponse,
    QuizStatisticsResponse,
    UserStatisticsResponse,
)

router = APIRouter(
    tags=["Statistics"],
    prefix="/statistics",
)


@router.get("/general", response_model=GeneralStatisticsResponse)
@cache(expire=60)
async def get_general_statistics(
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:statistics")),
):
    return await get_statistics_repository.get_general_stats(session=session)


@router.get("/quiz/{quiz_id}", response_model=QuizStatisticsResponse)
@cache(expire=60)
async def get_quiz_statistics(
    quiz_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:statistics")),
):
    return await get_statistics_repository.get_quiz_stats(
        session=session, quiz_id=quiz_id
    )


@router.get("/user/{user_id}", response_model=UserStatisticsResponse)
@cache(expire=60)
async def get_user_statistics(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:statistics")),
):
    return await get_statistics_repository.get_user_stats(
        session=session, user_id=user_id
    )
