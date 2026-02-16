from sqlmodel import create_engine, Session
from app.core.config import settings

def get_engine():
    return create_engine(
        settings.database_url,
        echo=settings.debug
        )


def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
