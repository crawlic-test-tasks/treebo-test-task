import asyncio
from datetime import datetime
import pytest


from database.repositories import (
    User,
    Note,
    UserRepository,
    NotesRepository,
    async_sessionmaker,
)


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_user_repository():
    user_repository = UserRepository()
    async with async_sessionmaker() as session:
        user = User(name="test", email="test@example.com", telegram_id=1)
        await user_repository.create(session, user)
        assert await user_repository.is_registered(session, 1)
        assert (await user_repository.get_by_telegram_id(session, 1)) is not None


@pytest.mark.asyncio
async def test_notes_repository():
    notes_repository = NotesRepository()
    users_repository = UserRepository()
    async with async_sessionmaker() as session:
        user = User(name="test", email="test@example.com", telegram_id=1)
        await users_repository.create(session, user)

        note = Note(user_id=user.id, text="test note", reminder_time=datetime.now())
        await notes_repository.create(session, note)

        assert await notes_repository.get_by_id(session, note.id)
