from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from middleware.check_channel_and_role import check_channel_and_admin

import app.keyboards as kb
import db.commits as cm 

sell_rt = Router()


@sell_rt.callback_query(F.data == 'sell')
async def sell_start(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer(' ')

    await callback.message.answer(
f'''{callback.message.from_user.first_name}, я рад, что ты решила облегчить себе жизнь и воспользоваться нашим проектом!
Если ты хочешь продавать рекламу в своем канале, то тебе необходимо будет заполнить небольшую анкету далее :D''', reply_markup=kb.sell_start)
    


class Anketa(StatesGroup):
    tg_id = State()
    channel = State()
    category = State()
    cost = State()
    time = State()



@sell_rt.callback_query(F.data == 'sell_start')
async def anketa_fsm(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer('')
    await state.set_state(Anketa.channel)

    await callback.message.answer('Введите ссылку на ваш канал в формате @channel_name', reply_markup=ReplyKeyboardRemove())


@sell_rt.message(Anketa.channel)
async def error_channel_name (message: Message, state: FSMContext):
    channel_name = message.text.strip()

    
    await check_channel_and_admin(message = message, bot = message.bot, user_id = message.from_user.id, channel_name = channel_name)
    
    await state.update_data(channel = message.text)
    await state.set_state(Anketa.category)
    await message.answer('Укажите категорию своего канала', reply_markup=await kb.get_cat_kb_sell())
    
    
@sell_rt.callback_query(Anketa.category, lambda c: c.data.startswith('sell_category_'))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[2])
    category_name = str(callback.data.split('_')[3])
    await state.update_data(category_id = category_id, category_name=category_name)
    await state.set_state(Anketa.cost)

    await callback.message.answer('Укажите стоимость размещения поста', reply_markup=ReplyKeyboardRemove())
    await callback.answer('')


@sell_rt.message(Anketa.cost)
async def anketa_time_fsm(message: Message, state: FSMContext):
    await state.update_data(cost = message.text)
    await state.set_state(Anketa.time)
    await message.answer(
'''Выберете желаемое время размещения:

1) 1/24 (1 час в топе, 24 часа в ленте)
2) 2/48 (2 часа в топе, 48 часов в ленте)''', reply_markup=kb.sell_time)



@sell_rt.message(Anketa.time)
async def anketa_end(message: Message, state = FSMContext):

    
    if message.text.startswith('1/24') or message.text.startswith('2/48'):
        pass
    else:
        await message.answer('⚠️ Вы указали некорректное значение. Пожалуйста, используйте клавиатуру или введите корректный формат времени (1/24 или 2/48)')
        return
    

    await state.update_data(time = message.text)
    data = await state.get_data()
    
    await message.answer(
        f"📝 <b>Результаты анкеты</b>\n\n"
        f"📢 <b>Канал</b>: {data['channel']}\n"
        f"📂 <b>Категория</b>: {data['category_name']}\n"
        f"💰 <b>Стоимость размещения</b>: {data['cost']} рублей\n"
        f"⏱  <b>Время размещения поста</b>: {data['time']}\n", 
        reply_markup=kb.anketa_agree, parse_mode='HTML') 


@sell_rt.callback_query(F.data == 'anketa_agree')
async def agree(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer('')
    await callback.message.answer('✅Объявление успешно создано.\n\nЖдите заказы!', reply_markup=kb.start)


    tg_id = callback.from_user.id
    data = await state.get_data()
    await cm.commit_date_to_db(data, tg_id)
    await state.clear()




