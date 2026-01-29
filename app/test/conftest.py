import pytest_asyncio
from core.config import settings
from core.db_helper import db_helper
from httpx import ASGITransport, AsyncClient
from main import app
from models.base import Base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

async_engine = create_async_engine(
    url=str(settings.database.test_url),
    echo=False,
    poolclass=NullPool,
)


@pytest_asyncio.fixture(scope="function")
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db):
    def override_get_db():
        yield async_db

    app.dependency_overrides[db_helper.session_getter] = override_get_db
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


@pytest_asyncio.fixture
async def test_role(async_client):
    response = await async_client.post("/role/", json={"name": "admin"})
    assert response.status_code == 201
    return response.json()


@pytest_asyncio.fixture
async def test_user(async_client, test_role):
    payload = {
        "username": "test_user",
        "password": "password123",
        "roles": [{"name": "admin"}],
    }

    response = await async_client.post("/user/", json=payload)
    assert response.status_code == 201
    return payload


@pytest_asyncio.fixture
async def access_token(async_client, test_user):
    response = await async_client.post(
        "/user/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_client(async_client, access_token):
    async_client.headers.update(
        {
            "Authorization": access_token,
        }
    )
    return async_client


@pytest_asyncio.fixture
async def create_permission(async_client, access_token):
    payload = {"name": "read:book"}

    response = await async_client.post("/permission/", json=payload)

    assert response.status_code == 201
