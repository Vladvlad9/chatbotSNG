from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    FIO = State()

    Back = State()

    Name = State()
    Surname = State()
    Patronymic = State()
