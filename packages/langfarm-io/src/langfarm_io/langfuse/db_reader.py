import logging
from collections.abc import Generator
from typing import TypeVar, Optional, Type

from sqlalchemy.orm import Session

from langfarm_io.langfuse.schema import TableBase

logger = logging.getLogger(__name__)

engine = None


def get_db_session() -> Generator[Session, None, None]:
    session = Session(engine)
    logger.debug("db session=[%s] created", session.hash_key)
    try:
        yield session
    finally:
        session.close()
        logger.debug("db session=[%s] closed", session.hash_key)


_T = TypeVar("_T", bound=TableBase)


def with_db_session(func):
    def execute(stmt, t: Type[_T]) -> Optional[_T] | Generator[_T, None, None]:
        for session in get_db_session():
            return func(stmt, t, session=session)

    return execute


@with_db_session
def read_first(stmt, t: Type[_T], *, session: Session | None = None) -> Optional[_T]:
    if session is None:
        return None
    row = session.execute(stmt).first()
    return row[0] if row else None


@with_db_session
def read_list(stmt, t: Type[_T], *, session: Session | None = None) -> Generator[_T, None, None]:
    if session is None:
        return None
    rows = session.execute(stmt).all()
    for row in rows:
        yield row[0]
