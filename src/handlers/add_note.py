from datetime import datetime
import logging
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.tables import Note
from database.repositories import notes_repository, users_repository, async_sessionmaker
from filters.user_registered import UserRegistered
from notifications import create_notification

router = Router(name="add_note")


class AddNoteState(StatesGroup):
    enter_text = State()
    enter_dt = State()


@router.message(Command("addnote"), UserRegistered())
async def handle_add_note(message: types.Message, state: FSMContext):
    await message.answer("Введите название заметки")
    await state.set_state(AddNoteState.enter_text)


@router.message(AddNoteState.enter_text)
async def handle_enter_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        "В какое время вы хотите добавить заметку (по московскому времени)? Введите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ"
    )
    await state.set_state(AddNoteState.enter_dt)


@router.message(AddNoteState.enter_dt)
async def handle_enter_dt(message: types.Message, state: FSMContext):
    try:
        dt = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("Введите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ")
        return

    data = await state.get_data()

    async with async_sessionmaker() as session:
        user = await users_repository.get_by_telegram_id(session, message.from_user.id)
        note = Note(user_id=user.id, text=data["text"], reminder_time=dt)
        await notes_repository.create(session, note)
        await create_notification(
            f"Напоминаю, вы хотели: {note.text} сегодня в {note.reminder_time.strftime('%H:%M')}",
            user.telegram_id,
            note.reminder_time,
        )

    await message.answer(
        "Заметка успешно добавлена. Чтобы просмотреть все заявки используйте команду /mynotes"
    )
    await state.clear()
