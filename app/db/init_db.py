from sqlmodel import SQLModel

from app.db.session import get_engine


def init_db():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
