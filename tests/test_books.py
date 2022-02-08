
import pytest
from biblioteca.app import create_app
from biblioteca.ext.database import get_session
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlmodel.pool import StaticPool

from sqlmodel import SQLModel


app = create_app()


@pytest_asyncio.fixture(name='session')
async def session_fixture():

    engine = create_async_engine(
        "sqlite+aiosqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name='client')
async def async_app_client(session):

    def get_session_override():  #
        return session

    app.dependency_overrides[get_session] = get_session_override  #
    client = TestClient(app)
    yield client  #
    app.dependency_overrides.clear()  #


@pytest.mark.asyncio
async def test_create_user(client):
    response = client.get(
        "/v1/books",
    )
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_create_book(client):  #
    response = client.post(
        "/v1/books",
        json={"titulo": "deadpool@example.com",
              "editora": "chimichangas4life",
              "foto": "foto"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["id"] is not None
