from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_quiz_repository
from .schemas import (
    QuizCreateRequest,
    QuizCreateResponse,
    QuizListRequest,
    QuizListResponse,
)

router = APIRouter(
    tags=["Quiz"],
    prefix="/quiz",
)


@router.post(
    "/", response_model=QuizCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_quiz(
    data: QuizCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("create:quiz")),
):
    return await get_quiz_repository.create_quiz(session=session, data=data)


@router.get("/{quiz_id}", response_model=QuizCreateResponse)
async def get_quiz(
    quiz_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:quiz")),
):
    return await get_quiz_repository.get_quiz(
        session=session, quiz_id=quiz_id
    )


@router.get("/", response_model=QuizListResponse)
async def list_quizzes(
    data: QuizListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:quiz")),
):
    return await get_quiz_repository.list_quizzes(
        session=session, request=data
    )


@router.put("/{quiz_id}", response_model=QuizCreateResponse)
async def update_quiz(
    quiz_id: int,
    data: QuizCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:quiz")),
):
    return await get_quiz_repository.update_quiz(
        session=session, quiz_id=quiz_id, data=data
    )


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:quiz")),
):
    await get_quiz_repository.delete_quiz(
        session=session, quiz_id=quiz_id
    )
