from sqlmodel import SQLModel
from app.db.session import engine
from app.db.models.user import User # noqa: F401

def init_db():
	SQLModel.metadata.create_all(engine)