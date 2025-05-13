from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.requests import get_categories

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Профиль')],
        [KeyboardButton(text='О проекте')],
    ],   resize_keyboard=True,
)


help_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='1. Общая информация', url='https://aiogram.dev')],
        [InlineKeyboardButton(text='2. Как работает реклама?', url='https://aiogram.dev')],
        [InlineKeyboardButton(text='3. Платежи', url='https://aiogram.dev')],
    ]
)


buy_sell = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Я хочу купить рекламу', callback_data='buy')],
        [InlineKeyboardButton(text='Я хочу продать рекламу', callback_data='sell')]
    ]
)

sell_start = InlineKeyboardMarkup(
    inline_keyboard= [
        [InlineKeyboardButton(text='ПОГНАЛИ!!!', callback_data='sell_start')]
    ]
)

sell_time = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text='1/24', callback_data = '1/24')],
        [KeyboardButton(text='2/48', callback_data='2/48')]
    ], resize_keyboard= True
)


categories_inline_sell = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Авто'), KeyboardButton(text='Бизнес')],
        [KeyboardButton(text='Спорт'), KeyboardButton(text='Медицина')],
        [KeyboardButton(text='Дом и сад'), KeyboardButton(text='Технологии')],
        [KeyboardButton(text='18+')],
        [KeyboardButton(text='<= Назад')]
    ], resize_keyboard=True, input_field_placeholder='Веберете категорию'
)


async def get_cat_kb():
    categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for cat in categories:
        keyboard.add(InlineKeyboardButton(text=cat.name, callback_data=f'category_{cat.id}'))
    return keyboard.adjust(2).as_markup()

async def get_cat_kb_sell():
    categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for cat in categories:
        keyboard.add(InlineKeyboardButton(text=cat.name, callback_data=f'sell_category_{cat.id}_{cat.name}'))
    return keyboard.adjust(2).as_markup()





async def select_page(category_id: int, current_page: int, channels: list):
    keyboard = InlineKeyboardBuilder()

    for i, ch in enumerate(channels, start = 1):
        global_index = current_page * 5 + (i - 1)
        keyboard.add(InlineKeyboardButton(text=f'Канал {ch.channel}', callback_data=f'channel_{category_id}_{current_page}_{global_index}'))

    keyboard.adjust(1)

    keyboard.row(
        InlineKeyboardButton(text='⏪ Назад', callback_data=f'prev_{category_id}_{current_page}'),
        InlineKeyboardButton(text='Вперёд ⏩', callback_data=f'next_{category_id}_{current_page}')
    )
    return keyboard.as_markup()



anketa_agree = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text='Создать объявление', callback_data='anketa_agree')]
    ]
)

buy_continue = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить', callback_data='buy_continue')]
    ]
)

buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='К оплате', callback_data='pay', pay=True)]
    ]
)

create_post = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Создать объявление', callback_data='create_post')]
    ]
)

send_post_to_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅Отправить объявление', callback_data='post_send')],
        [InlineKeyboardButton(text='❌Изменить', callback_data='post_change')]
    ]
)
