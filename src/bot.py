import logging

from sqlmodel import SQLModel

from handlers import start, add_note, exceptions_handlers, my_notes
from database.repositories import engine
from config import dp, bot

dp.include_router(start.router)
dp.include_router(add_note.router)
dp.include_router(my_notes.router)
dp.include_router(exceptions_handlers.router)

logging.basicConfig(level=logging.INFO)


async def run_bot() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    await dp.start_polling(bot)
