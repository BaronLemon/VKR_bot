from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import app.keyboards as kb


create_post_rt = Router()


class CreatePost(StatesGroup):
    text = State()
    agreements = State()
    changes = State()


@create_post_rt.callback_query(F.data == 'create_post')
async def create_post_start(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id)
    await callback.message.edit_text('Введите текст вашего объявления')
    await state.set_state(CreatePost.text)
    await callback.answer('')

@create_post_rt.message(CreatePost.text)
async def create_post_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f'Пожалуйста, внимательно перечитайте ваше объявление перед отправкой\nТекст вашего объявления:\n\n{data["text"]}\n\nОтправить в таком виде?', reply_markup=kb.send_post_to_admin)
    await state.set_state(CreatePost.agreements)
    
@create_post_rt.callback_query(CreatePost.agreements, lambda c: c.data.startswith('post_'))
async def send_or_change(callback: CallbackQuery, state: FSMContext, bot: Bot):
    action = callback.data.split('_')[1]
    data = await state.get_data()
    channel = data['channel']
    text = data['text']

    if action == 'send':
        await bot.send_message(channel, text=text)
        await state.clear()

    elif action == 'change':
        await state.clear()
        await state.set_state(CreatePost.text)
        await callback.message.edit_text('Введите текст вашего объявления')
        await state.update_data(channel=channel)


    await callback.answer('')
