import pytest

from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.db.models.user import User

TEST_DATABASE_URL = "sqlite:///.test.db"
engine = create_engine(
	TEST_DATABASE_URL,
	echo=True, # Will log all SQL commands executed by SQLAlchemy to the console
	connect_args={"check_same_thread": False}  # Allows multi-thread access (normally restricted by SQLite)
)

@pytest.fixture(scope="session")
def test_engine():
	SQLModel.metadata.create_all(engine)
	yield engine
	SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session(test_engine):
	with Session(test_engine) as session:
		yield session

@pytest.fixture(scope="function")
def client(session):
	# Override dependency
	from app.db.session import get_session
	app.dependency_overrides[get_session] = lambda: session
	with TestClient(app) as c:
		yield c