import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
import settings
from forms import MeetForm

from utils import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TOKEN)

dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    add_user(tg_id=message.from_user.id, nickname=message.chat.username, name=message.chat.first_name)
    kb = get_keyboard(message.from_user.id)
    await message.answer('Привет!', reply_markup=kb)

@dp.message(Text('Показать доступные записи'))
async def show_available_meets(message: types.Message):
    kb = get_available_meets()
    await message.answer('Вот текущие доступные записи, выберите на какую желаете записаться или нажмите "Назад" для возвращения в главное меню', reply_markup=kb.as_markup())

@dp.message(Text('Посмотреть мои записи'))
async def show_user_meets(message: types.Message):
    meets = get_user_meets(message.from_user.id)
    kb = get_keyboard(message.from_user.id)
    await message.answer(meets, reply_markup=kb)

@dp.message(Text('Показать забронированные записи'))
async def show_booked_meets(message: types.Message):
    meets = get_booked_meets()
    await message.answer(meets)

@dp.message(Text('Добавить окно для записи'))
async def get_new_meet_name(message: types.Message, state: FSMContext):
    await message.answer('Введите название для встречи(Например: прогулка, поход в кино и тд):')
    await state.set_state(MeetForm.name)

@dp.message(MeetForm.name)
async def get_new_meet_date(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(MeetForm.date)
    await message.answer('Отлично! Теперь введите дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС')

@dp.message(MeetForm.date)
async def create_new_meet(message: types.Message, state: FSMContext):
    user_data = await state.update_data(date=message.text)
    await state.clear()
    name, date = user_data['name'], user_data['date']
    push_new_meet(name, date)
    await message.answer('Готово!')


# CALLBACKS 

@dp.callback_query(Text(startswith='set_meet_to_user#'))
async def set_meet_to_user(callback: types.CallbackQuery):
    meet_id = callback.data.split('#')[1]
    set_meet(meet_id, callback.from_user.id)
    await callback.message.answer('Готово!')

@dp.callback_query(Text('main_menu'))
async def main_menu(callback: types.CallbackQuery):
    await cmd_start(callback.message)

# MAIN 

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())