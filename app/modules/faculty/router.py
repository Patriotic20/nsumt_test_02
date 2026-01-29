from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_faculty_repository
from .schemas import (
    FacultyCreateRequest,
    FacultyCreateResponse,
    FacultyListRequest,
    FacultyListResponse,
)

router = APIRouter(
    tags=["Faculty"],
    prefix="/faculty",
)


@router.post(
    "/", response_model=FacultyCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_faculty(
    data: FacultyCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("create:faculty")),
):
    return await get_faculty_repository.create_faculty(session=session, data=data)


@router.get("/{faculty_id}", response_model=FacultyCreateResponse)
async def get_faculty(
    faculty_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:faculty")),
):
    return await get_faculty_repository.get_faculty(
        session=session, faculty_id=faculty_id
    )


@router.get("/", response_model=FacultyListResponse)
async def list_faculties(
    data: FacultyListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:faculty")),
):
    return await get_faculty_repository.list_faculties(
        session=session, request=data
    )


@router.put("/{faculty_id}", response_model=FacultyCreateResponse)
async def update_faculty(
    faculty_id: int,
    data: FacultyCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:faculty")),
):
    return await get_faculty_repository.update_faculty(
        session=session, faculty_id=faculty_id, data=data
    )


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    faculty_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:faculty")),
):
    await get_faculty_repository.delete_faculty(
        session=session, faculty_id=faculty_id
    )
