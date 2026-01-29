from core.db_helper import db_helper
from dependence.role_checker import PermissionRequired
from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import get_user_repository
from .schemas import (
    UserCreateRequest,
    UserCreateResponse,
    UserListRequest,
    UserListResponse,
    UserLoginRequest,
    UserLoginResponse,
    UserUpdateRequest,
)
from .service import auth_service

router = APIRouter(
    tags=["User"],
    prefix="/user",
)


@router.post("/login", response_model=UserLoginResponse)
async def login(
    data: UserLoginRequest, session: AsyncSession = Depends(db_helper.session_getter)
):
    return await auth_service.login(session=session, data=data)


@router.post("/refresh", response_model=UserLoginResponse)
async def refresh(
    authorization: str = Header(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await auth_service.refresh(session=session, refresh_token=authorization)


@router.get("/me", response_model=UserCreateResponse)
async def get_me(
    authorization: str = Header(...),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await auth_service.get_current_user(session=session, token=authorization)


@router.post(
    "/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    data: UserCreateRequest,
    # Используем Depends для инъекции сессии
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_user_repository.create_user(session=session, data=data)


@router.get("/{user_id}", response_model=UserCreateResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:user")),
):
    return await get_user_repository.get_user(session=session, user_id=user_id)


@router.get("/", response_model=UserListResponse)
async def list_users(
    # Используем Depends, чтобы параметры шли из Query string (?page=1&limit=10)
    data: UserListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("read:user")),
):
    return await get_user_repository.list_users(session=session, request=data)


@router.put("/{user_id}", response_model=UserCreateResponse)
async def update_user(
    user_id: int,
    data: UserUpdateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("update:user")),
):
    return await get_user_repository.update_user(
        session=session, user_id=user_id, data=data
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    _: PermissionRequired = Depends(PermissionRequired("delete:user")),
):
    await get_user_repository.delete_user(session=session, user_id=user_id)
