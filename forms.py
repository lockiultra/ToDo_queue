from aiogram.fsm.state import State, StatesGroup

class MeetForm(StatesGroup):
    name = State()
    date = State()