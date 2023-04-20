from pony.orm import *
from models import *
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import settings

@db_session
def add_user(tg_id, name, nickname=''):
    u = User(user_id=str(tg_id), name=name)
    commit()

@db_session
def show_available_meets():
    u = User.select(lambda u: u.name == 'lockiultra')
    print(u)
    
def get_keyboard(user_id):
    if user_id in settings.ADMIN_LIST:
        return get_admin_keyboard()
    return get_user_keyboard()

def get_user_keyboard():
    kb = [[types.KeyboardButton(text='Показать доступные записи')],
          [types.KeyboardButton(text='Посмотреть мои записи')]
          ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие:'
    )
    return keyboard

def get_admin_keyboard():
    kb = [[types.KeyboardButton(text='Показать доступные записи')],
          [types.KeyboardButton(text='Показать забронированные записи')],
          [types.KeyboardButton(text='Добавить окно для записи')]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие:'
    )
    return keyboard

@db_session
def get_available_meets():
    meets = [meet for meet in Meet.select()[:] if not meet.user]
    kb = InlineKeyboardBuilder()
    for meet in meets:
        kb.add(types.InlineKeyboardButton(text=f'{meet.name} {meet.date}', callback_data=f'set_meet_to_user#{meet.id}'))
    kb.add(types.InlineKeyboardButton(text='Назад', callback_data='main_menu'))
    return kb

@db_session
def set_meet(meet_id, user_id):
    user = User.get(user_id=str(user_id))
    meet = Meet.get(id=meet_id)
    print(user, meet)
    meet.user = user
    commit()

@db_session
def get_user_meets(user_id):
    user = User.get(user_id=str(user_id))
    meets = [meet for meet in Meet.select()[:] if meet.user == user]
    return '\n'.join([f'{meet.name} {meet.date}' for meet in meets])

@db_session
def get_booked_meets():
    meets = [meet for meet in Meet.select()[:] if meet.user]
    return '\n'.join([f'{meet.name} {meet.date} - {meet.user.name}' for meet in meets])

@db_session
def push_new_meet(name, date):
    meet = Meet(name=name, date=date)
    commit()