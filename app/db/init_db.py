from sqlmodel import SQLModel
from app.db.session import engine
from app.db.models import User, FeatureFlag


def init_db():
    SQLModel.metadata.create_all(engine)
