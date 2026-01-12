from sqlmodel import create_engine, Session
from app.config.settings import settings

engine = create_engine(
	settings.database_url,
	echo=settings.debug
)

def get_session():
	with Session(engine) as session:
		yield session
