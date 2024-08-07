from aiogram import Router, types
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from pydantic import validate_email

from database.repositories import users_repository, async_sessionmaker
from database.tables import User
from filters.user_registered import UserRegistered

router = Router(name="start")


class RegisterState(StatesGroup):
    enter_name = State()
    enter_email = State()


@router.message(CommandStart(), UserRegistered())
async def handle_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в бота! Для добавления заметок используйте команду /addnote"
    )


@router.message(RegisterState.enter_name)
async def handle_enter_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите ваш email")
    await state.set_state(RegisterState.enter_email)


@router.message(RegisterState.enter_email)
async def handle_enter_email(message: types.Message, state: FSMContext):
    email = message.text.lower().strip()

    try:
        validate_email(email)
    except Exception:
        await message.answer("Вы ввели некорректный email. Попробуйте ещё раз.")
        return

    data = await state.get_data()
    user = User(name=data["name"], email=email, telegram_id=message.from_user.id)

    async with async_sessionmaker() as session:
        await users_repository.create(session, user)

    await message.answer(
        "Вы успешно зарегистрировались в системе. Для добавления заметок используйте команду /addnote"
    )
    await state.clear()
