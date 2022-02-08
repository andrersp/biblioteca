import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from biblioteca.app import create_app
from biblioteca.ext.database import get_session


app = create_app()


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")  #
def client_fixture(session: Session):  #

    def get_session_override():  #
        return session

    app.dependency_overrides[get_session] = get_session_override  #

    client = TestClient(app)  #
    yield client  #
    app.dependency_overrides.clear()  #


def test_create_book(client: TestClient):  #
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


def test_get_books(client: TestClient):  #
    response = client.get(
        "/v1/books")
    data = response.json()

    assert response.status_code == 200
    assert data.get("success") == True

    assert type(data.get("data")) == list
