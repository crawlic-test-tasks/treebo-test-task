from aiogram import Router, types
from aiogram.filters.command import Command

from database.tables import User
from database.repositories import users_repository, async_sessionmaker
from filters.user_registered import UserRegistered

router = Router(name="my_notes")


@router.message(Command("mynotes"), UserRegistered())
async def handle_my_notes(message: types.Message):
    async with async_sessionmaker() as session:
        user = await users_repository.get_by_telegram_id(session, message.from_user.id)

    await message.answer("Ваши заметки:")
    for note in user.notes:
        await message.answer(
            f"Когда: {note.reminder_time.strftime('%d.%m.%Y %H:%M')}\nЗаметка: {note.text}"
        )
