from core.db_helper import db_helper
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_quiz_process_repository
from .schemas import (
    StartQuizRequest,
    StartQuizResponse,
    EndQuizRequest,
    EndQuizResponse,
)

# Note: Permissions might be needed but usually taking a quiz is open to students?
# For now, keeping it open or simple. If auth is needed, Dependencies can be added.

router = APIRouter(
    tags=["Quiz Process"],
    prefix="/quiz_process",
)


@router.post(
    "/start_quiz", response_model=StartQuizResponse, status_code=status.HTTP_200_OK
)
async def start_quiz(
    data: StartQuizRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_quiz_process_repository.start_quiz(session=session, data=data)


@router.post(
    "/end_quiz", response_model=EndQuizResponse, status_code=status.HTTP_200_OK
)
async def end_quiz(
    data: EndQuizRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_quiz_process_repository.end_quiz(session=session, data=data)
