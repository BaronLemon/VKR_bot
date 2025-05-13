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

# class Register(StatesGroup):
#     name = State()
#     age = State()
#     cost = State()

# @rt.message(Command('fsm'))
# async def cmd_fsm(message: Message, state: FSMContext):
#     await state.set_state(Register.name)
#     await message.answer('Введите имя')

# @rt.message(Register.name)
# async def register_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(Register.age)
#     await message.answer('Введите возраст')

# @rt.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(Register.cost)
#     await message.answer('Введите стоимость')

# @rt.message(Register.cost)
# async def register_cost(message: Message, state: FSMContext):
#     await state.update_data(cost=message.text)
#     data = await state.get_data()
#     await message.answer(f'Your name: {data['name']}\nYour age: {data['age']}\nYour cost: {data['cost']}')
#     await state.clear()




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





# @rt.message(F.text == 'Каталог')
# async def Catalog(message: Message):
#     await message.answer('Ты хочешь купить рекламу или продать?', reply_markup=kb.buy_sell)

# @rt.callback_query(F.data == 'buy')
# async def buy(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.edit_text('BUY')

# @rt.callback_query(F.data == 'sell')
# async def sell(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.edit_text('SELL')


# @rt.callback_query(lambda c: c.data in ['buy_action', 'sell_action'])
# async def action(callback: CallbackQuery):
#     action = callback.data.split('_')[0]

#     await callback.message.delete()

#     if action == 'buy':
#         await callback.message.answer("Покупка рекламы", reply_markup=kb.test)
#     elif action == 'sell':    
#         await callback.message.answer("Продажа рекламы", reply_markup=kb.test)




@rt.message(F.text == 'Kak dela?')
async def how_are_you(message: Message):
    await message.answer('OKE')

@rt.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMgZ_vDFmPRhPguGAToV07iu32Yqc4AArrrMRvkP9lL_3McIadyKTIBAAMCAAN3AAM2BA', caption='Отправка фото по ID')

@rt.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')
# message.photo [-1] - самое лучшее качество фото на сервере ТГ


@rt.callback_query(F.data == 'main')
async def main(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('KYKY!', reply_markup=await kb.inline_cars())





