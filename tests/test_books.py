
import os
import pytest
from biblioteca.app import create_app
from biblioteca.ext.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlmodel.pool import StaticPool


from sqlmodel import SQLModel


app = create_app()

database = 'database.db'
if os.path.exists(database):
    os.remove(database)


@pytest.fixture(name='session')
async def session_fixture():

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{database}", connect_args={"check_same_thread": False}, future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest.fixture(name='client')
async def async_app_client(session):

    def get_session_override():  #
        return session

    app.dependency_overrides[get_session] = get_session_override  #
    client = TestClient(app)
    yield client  #
    app.dependency_overrides.clear()  #


async def test_create_book(client):  #
    response = client.post(
        "/v1/obras",
        json={"titulo": "Titulo de Livro 1",
              "editora": "chimichangas4life",
              "foto": "foto",
              "autores": ["Autor 1", "Autor 2"]},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["id"] is not None

    response = client.post(
        "/v1/obras",
        json={"titulo": "Titulo de Livro 1",
              "editora": "chimichangas4life",
              "foto": "foto",
              "autores": "Teste"},
    )
    assert response.status_code == 422


async def test_get_obras(client):
    response = client.get(
        "/v1/obras",
    )

    result = response.json()

    data = result.get("data")
    assert response.status_code == 200, response.text
    assert type(result.get("data")) == list
    assert len(data) > 0


async def test_get_obra(client):
    response = client.get(
        "/v1/obras/1",
    )
    result = response.json()
    assert response.status_code == 200
    assert result.get("id") == 1

    response = client.get(
        "/v1/obras/2",
    )
    assert response.status_code == 404


async def test_delete_obra(client):
    response = client.put(
        "/v1/obras/1",
    )
    result = response.json()
    assert response.status_code == 200
    assert result.get("success") == True

    response = client.get(
        "/v1/obras/2",
    )
    assert response.status_code == 404
