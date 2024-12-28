from asyncio import current_task
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session, create_async_engine

from .config import DATABASE


class DatabaseSession:
    def __init__(self):
        self.engine = create_async_engine(
            url=DATABASE
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )
        return session

    async def session_dependency(self):
        session = self.get_scoped_session()
        yield session
        await session.close()

db_session = DatabaseSession()
