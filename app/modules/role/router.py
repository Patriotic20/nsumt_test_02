from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_role_repository
from .schemas import (
    RoleCreateRequest,
    RoleCreateResponse,
    RoleListRequest,
    RoleListResponse,
)

router = APIRouter(
    tags=["Role"],
    prefix="/role",
)


@router.post(
    "/", response_model=RoleCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_role(
    data: RoleCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    # _: PermissionRequired = Depends(PermissionRequired("create:role"))
):
    return await get_role_repository.create_role(session=session, data=data)


@router.get("/{role_id}", response_model=RoleCreateResponse)
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:role")),
):
    return await get_role_repository.get_role(session=session, role_id=role_id)


@router.get("/", response_model=RoleListResponse)
async def list_roles(
    data: RoleListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:role")),
):
    return await get_role_repository.list_roles(session=session, request=data)


@router.put("/{role_id}", response_model=RoleCreateResponse)
async def update_role(
    role_id: int,
    data: RoleCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:role")),
):
    return await get_role_repository.update_role(
        session=session, role_id=role_id, data=data
    )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:role")),
):
    await get_role_repository.delete_role(session=session, role_id=role_id)
