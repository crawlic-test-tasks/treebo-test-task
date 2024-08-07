from aiogram import Router, types
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext

from exceptions import NotRegisteredException
from .start import RegisterState

router = Router(name="exception_router")


@router.error(ExceptionTypeFilter(NotRegisteredException))
async def handle_not_registered(event: types.ErrorEvent, state: FSMContext):
    await event.update.message.answer(
        "Вы не зарегистрированы в системе. Введите ваше имя."
    )
    await state.set_state(RegisterState.enter_name)
