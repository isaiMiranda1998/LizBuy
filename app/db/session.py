from app.core.config import db_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(db_settings.database_url)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()