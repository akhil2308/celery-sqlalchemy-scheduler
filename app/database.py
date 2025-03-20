from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import Config

engine = create_engine(
    url = Config.DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_connection() -> Session:
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def close_db_connection(db: Session):
    if db:
        db.close()
