





async def check_channel_and_admin(message, bot, user_id: int, channel_name: str):

    if not message.text.startswith('@'):
        await message.answer('⚠️ Некорректный формат канала. Введите имя канала, начиная с @')
        return

    else:
        try: 
            chat = await bot.get_chat(channel_name)
        except Exception as e:
            await message.answer(f'Не удалось найти канал с именем {channel_name}. Проверьте правильность ввода.')
            return
        try:
            admin = await bot.get_chat_member(chat.id, user_id)
        except Exception as e:
            await message.answer(f'Вы не являетесь администратором или владельцем в канале {channel_name}.')
            return
        

        if admin.status == 'creator':
            status = 'владельцом'

        if admin.status == 'administrator':
            status = 'админом'
        
        if admin.status in ['creator', 'administrator']:
            await message.answer(
f'''✅ Канал принят!
                
<u>Имя канала:</u>
<b>{chat.title}</b>

<u>Описание канала:</u>
<b>{chat.description}</b>

Вы являетесь {status} в канале {channel_name}''', parse_mode='HTML')

