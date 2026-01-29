from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_teacher_repository
from .schemas import (
    TeacherCreateRequest,
    TeacherCreateResponse,
    TeacherListRequest,
    TeacherListResponse,
)

router = APIRouter(
    tags=["Teacher"],
    prefix="/teacher",
)


@router.post(
    "/", response_model=TeacherCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_teacher(
    data: TeacherCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("create:teacher")),
):
    return await get_teacher_repository.create_teacher(session=session, data=data)


@router.get("/{teacher_id}", response_model=TeacherCreateResponse)
async def get_teacher(
    teacher_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:teacher")),
):
    return await get_teacher_repository.get_teacher(
        session=session, teacher_id=teacher_id
    )


@router.get("/", response_model=TeacherListResponse)
async def list_teachers(
    data: TeacherListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:teacher")),
):
    return await get_teacher_repository.list_teachers(
        session=session, request=data
    )


@router.put("/{teacher_id}", response_model=TeacherCreateResponse)
async def update_teacher(
    teacher_id: int,
    data: TeacherCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:teacher")),
):
    return await get_teacher_repository.update_teacher(
        session=session, teacher_id=teacher_id, data=data
    )


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    teacher_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:teacher")),
):
    await get_teacher_repository.delete_teacher(
        session=session, teacher_id=teacher_id
    )
