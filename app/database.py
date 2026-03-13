from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def init_db(database_url: str) -> None:
    global _engine, _SessionLocal
    _engine = create_engine(database_url)
    _SessionLocal = sessionmaker(bind=_engine)
    Base.metadata.create_all(bind=_engine)


def get_session() -> Session:
    if _SessionLocal is None:
        raise RuntimeError("Database not initialised. Call init_db first.")
    return _SessionLocal()
