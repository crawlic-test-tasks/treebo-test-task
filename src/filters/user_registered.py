from aiogram.filters import Filter
from aiogram.types import Message

from database.repositories import users_repository, async_sessionmaker
from exceptions import NotRegisteredException


class UserRegistered(Filter):
    async def __call__(self, message: Message) -> bool:
        async with async_sessionmaker() as session:
            user = await users_repository.is_registered(session, message.from_user.id)
        if not user:
            raise NotRegisteredException()
        return True
