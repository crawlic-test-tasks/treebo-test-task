from abc import ABC
from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

from settings import settings
from .tables import User, Note

DB_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"

engine = create_async_engine(
    DB_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
)
async_sessionmaker = sessionmaker[AsyncSession](engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore

T = TypeVar("T", bound=SQLModel)


class CrudRepository(ABC, Generic[T]):
    table_type = SQLModel

    def __init__(self) -> None:
        assert self.table_type != SQLModel, "table_type must be subclass of SQLModel"

    async def get_by_id(self, session: AsyncSession, entity_id: int) -> T | None:
        stmt = select(self.table_type).where(self.table_type.id == entity_id)
        result = await session.exec(stmt)
        return result.first()

    async def create(self, session: AsyncSession, entity: T) -> T:
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity


class UserRepository(CrudRepository[User]):
    table_type = User

    async def is_registered(self, session: AsyncSession, telegram_id: int) -> bool:
        """Quick check if user is registered"""

        stmt = select(self.table_type.id).where(User.telegram_id == telegram_id)
        result = await session.exec(stmt)
        return result.first() is not None

    async def get_by_telegram_id(
        self, session: AsyncSession, telegram_id: int
    ) -> User | None:
        """Get whole user with notes"""

        stmt = select(self.table_type).where(User.telegram_id == telegram_id)
        result = await session.exec(stmt)
        return result.first()


class NotesRepository(CrudRepository[Note]):
    table_type = Note


users_repository = UserRepository()
notes_repository = NotesRepository()
