from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_group_repository
from .schemas import (
    GroupCreateRequest,
    GroupCreateResponse,
    GroupListRequest,
    GroupListResponse,
)

router = APIRouter(
    tags=["Group"],
    prefix="/group",
)


@router.post(
    "/", response_model=GroupCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_group(
    data: GroupCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("create:group")),
):
    return await get_group_repository.create_group(session=session, data=data)


@router.get("/{group_id}", response_model=GroupCreateResponse)
async def get_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:group")),
):
    return await get_group_repository.get_group(
        session=session, group_id=group_id
    )


@router.get("/", response_model=GroupListResponse)
async def list_groups(
    data: GroupListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:group")),
):
    return await get_group_repository.list_groups(
        session=session, request=data
    )


@router.put("/{group_id}", response_model=GroupCreateResponse)
async def update_group(
    group_id: int,
    data: GroupCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:group")),
):
    return await get_group_repository.update_group(
        session=session, group_id=group_id, data=data
    )


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:group")),
):
    await get_group_repository.delete_group(
        session=session, group_id=group_id
    )
