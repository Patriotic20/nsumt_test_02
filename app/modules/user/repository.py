from fastapi import HTTPException, status
from models.role.model import Role
from models.user.model import User
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .schemas import (
    UserCreateRequest,
    UserListRequest,
    UserListResponse,
    UserUpdateRequest,
)


class UserRepository:
    async def create_user(self, session: AsyncSession, data: UserCreateRequest) -> User:
        # Проверка на существование
        stmt_check = select(User).where(User.username == data.username)
        result_check = await session.execute(stmt_check)
        if result_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        roles = []
        if data.roles:
            role_names = [role.name for role in data.roles]
            # Получаем объекты ролей
            stmt_roles = select(Role).where(Role.name.in_(role_names))
            result_roles = await session.execute(stmt_roles)
            roles = result_roles.scalars().all()

            if len(roles) != len(data.roles):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more roles not found",
                )

        # Создаем пользователя. Пароль уже захэширован 
        # внутри UserCreateRequest (field_validator)
        new_user = User(username=data.username, password=data.password, roles=roles)

        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user, attribute_names=["roles"])
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

        return new_user

    async def get_user(self, session: AsyncSession, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id).options(selectinload(User.roles))
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    async def list_users(
        self, session: AsyncSession, request: UserListRequest
    ) -> UserListResponse:
        # 1. Запрос на получение моделей
        stmt = (
            select(User)
            .options(selectinload(User.roles))
            .offset(request.offset)
            .limit(request.limit)
        )

        if request.username:
            stmt = stmt.where(User.username.ilike(f"%{request.username}%"))

        result = await session.execute(stmt)
        users = result.scalars().all()

        # 2. Запрос на общее количество
        count_stmt = select(func.count()).select_from(User)
        if request.username:
            count_stmt = count_stmt.where(User.username.ilike(f"%{request.username}%"))

        total_result = await session.execute(count_stmt)
        total = total_result.scalar() or 0

        # 3. Возвращаем UserListResponse, используя данные из моделей.
        # Чтобы UserCreateResponse (внутри списка) корректно обработал роли,
        # в схеме UserCreateResponse нужно будет добавить преобразование 
        # списка объектов в список строк.
        return UserListResponse(
            total=total,
            page=request.page,
            limit=request.limit,
            users=users,  # Передаем объекты моделей, Pydantic сам их провалидирует
        )

    async def update_user(
        self, session: AsyncSession, user_id: int, data: UserUpdateRequest
    ) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Частичное обновление через Request схему
        if data.username is not None:
            user.username = data.username

        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, session: AsyncSession, user_id: int) -> None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        await session.delete(user)
        await session.commit()


get_user_repository = UserRepository()
