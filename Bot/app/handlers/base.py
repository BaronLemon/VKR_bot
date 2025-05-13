from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from .Catalog import Catalog_rt
import app.keyboards as kb
import db.requests as rq


rt = Router()
rt.include_router(Catalog_rt)


@rt.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(
f'''Приветствую тебя {message.from_user.first_name}!

Очень рад, что ты решил улучшить показатели своего канала и присоединиться к большому сообществу\n
                         
Здесь ты найдешь статистику каналов и сможешь купить в них рекламу!''', reply_markup=kb.start)
    

@rt.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Здесь представлена некая информация о нас! Выбери раздел, который тебя интересует', reply_markup=kb.help_btn)

@rt.message(F.text == 'О проекте')
async def Catalog(message: Message):
    await message.answer('Здесь представлена некая информация о нас! Выбери раздел, который тебя интересует', reply_markup=kb.help_btn)






