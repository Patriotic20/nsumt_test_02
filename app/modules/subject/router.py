from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter

from .repository import get_subject_repository
from .schemas import (
    SubjectCreateRequest,
    SubjectCreateResponse,
    SubjectListRequest,
    SubjectListResponse,
)

router = APIRouter(
    tags=["Subject"],
    prefix="/subject",
)


@router.post(
    "/", 
    response_model=SubjectCreateResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
async def create_subject(
    data: SubjectCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("create:subject")),
):
    return await get_subject_repository.create_subject(session=session, data=data)


@router.get("/{subject_id}", response_model=SubjectCreateResponse)
@cache(expire=60)
async def get_subject(
    subject_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:subject")),
):
    return await get_subject_repository.get_subject(
        session=session, subject_id=subject_id
    )


@router.get("/", response_model=SubjectListResponse)
@cache(expire=60)
async def list_subjects(
    data: SubjectListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:subject")),
):
    return await get_subject_repository.list_subjects(
        session=session, request=data
    )


@router.put("/{subject_id}", response_model=SubjectCreateResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def update_subject(
    subject_id: int,
    data: SubjectCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:subject")),
):
    return await get_subject_repository.update_subject(
        session=session, subject_id=subject_id, data=data
    )


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def delete_subject(
    subject_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:subject")),
):
    await get_subject_repository.delete_subject(
        session=session, subject_id=subject_id
    )
