from aiogram.dispatcher.filters.state import State, StatesGroup

class UserState(StatesGroup):
    user_text = State()
