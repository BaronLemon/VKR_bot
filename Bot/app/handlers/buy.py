from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from app.handlers.agreement import create_post_rt
import app.payments as pay
import app.keyboards as kb
import db.requests as rq

buy_rt = Router()
buy_rt.include_router(create_post_rt)
sent_messages = {}


@buy_rt.callback_query(F.data == 'buy')
async def catalog(callback: CallbackQuery):
    await callback.message.delete()

    await callback.answer('')
    await callback.message.answer('Выбери нужную тебе категорию', reply_markup=await kb.get_cat_kb())


@buy_rt.callback_query(lambda c: c.data.startswith('category_'))
async def choose_category(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    category_name = await rq.get_category_name(category_id)
    channels = await rq.get_channels_by_category(category_id, 0)

    if channels:
        text = f'Список каналов в категории {category_name}: \n\n'

        for i, ch in enumerate(channels, start = 1):
            text += f'{i}. 📢 Канал: {ch.channel}\n 💰 Стоимость: {ch.cost}\n ⏱Время размещения: {ch.time}\n\n'

        keyboard = await kb.select_page(category_id, 0, channels)
        await callback.message.answer(text, reply_markup=keyboard)
        await callback.answer('')

@buy_rt.callback_query(lambda c: c.data.startswith('prev_') or c.data.startswith('next_'))
async def select_page(callback: CallbackQuery):
    data = callback.data.split('_')
    action = data[0]
    category_id = int(data[1])
    current_page = int(data[2])

    if action == 'prev':
        current_page -= 1
    elif action == 'next':
        current_page += 1


    channels = await rq.get_channels_by_category(category_id, current_page)
    category_name = await rq.get_category_name(category_id)
    if channels:
        text = f'Список каналов в категории {category_name}:\n\n'

        for i, ch in enumerate(channels, start = 1 + current_page * 5): 
            text += f'{i}. 📢 Канал: {ch.channel}\n 💰 Стоимость: {ch.cost}\n ⏱Время размещения: {ch.time}\n\n'

        keyboard = await kb.select_page(category_id, current_page, channels)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer('')




@buy_rt.callback_query(lambda c: c.data.startswith('channel_'))
async def choose_channel(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    category_id = int(data[1]) 
    channel_page = int(data[2])
    local_index = int(data[3])%5
    
    channels = await rq.get_channels_by_category(category_id, channel_page)

    if 0 <= local_index < len(channels):
        channel = channels[local_index]
        text = f'Ваш выбор:\n\n 📢 Канал: {channel.channel}\n\n'
        text += f'💰 Стоимость размещения рекламы: {channel.cost}\n\n'
        text += f'⏱ Время размещения: {channel.time}\n\n'
        text += f'К оплате: {channel.cost}\n\n'

        await state.update_data(channel = channel.channel, cost = channel.cost, time = channel.time)
        await callback.message.answer(text, reply_markup=kb.buy_continue)   
             
    else: 
        await callback.message.answer('Канал не найден')

    await callback.answer('')



@buy_rt.callback_query(F.data == 'buy_continue')
async def rules(callback: CallbackQuery):
    text = '''Правила размещение рекламы: 

1. После выбора и оплаты рекламы в данном канале денежные средства заморозятся на нашем счете.
2. Для размещения рекламного поста вам необходимо подготовить рекламный пост, который будет отправлен администратору выбранного канала для согласования. 
3. После согласования пост будет автоматически размещен на указанный в объявлении срок.
4. Продавец получит денежные средства только после окончания срока размещения рекламного поста.

Если вы согласны с условиями размещения рекламы, нажмите на кнопку "Согласен"'''
    await callback.message.answer(text, reply_markup=kb.buy)



@buy_rt.callback_query(F.data == 'pay')
async def send_invoice(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    channel_name = data['channel']
    channel_cost = data['cost']
    channel_time = data['time']
    
    current_amount = int(channel_cost) * 100

    await pay.send_invoice(callback, channel_name, channel_cost, channel_time, current_amount)


@buy_rt.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok = True)


@buy_rt.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    await message.answer('✅Оплата прошла успешно.', reply_markup=kb.create_post)


