import pytest

from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.db.models import User
from app.db.session import get_session

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def engine():
	""" Create a fresh engine per test """
	
	engine = create_engine(
		"sqlite:///:memory:",
		echo=True,
		connect_args={"check_same_thread": False}
	)
	SQLModel.metadata.create_all(engine)

	return engine

@pytest.fixture
def session(engine):
	connection = engine.connect()
	with Session(bind=connection) as session:
		yield session
	SQLModel.metadata.drop_all(engine)
	connection.close()

@pytest.fixture
def client(session):
	# Override dependency
	app.dependency_overrides[get_session] = lambda: session
	
	with TestClient(app) as client:
		yield client
	
	app.dependency_overrides.clear()