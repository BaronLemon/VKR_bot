import logging
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers.base import rt
from config import TOKEN
from db.models import async_main


async def main():
    await async_main() 

    bot = Bot(token=TOKEN)
    dp = Dispatcher() 
    dp.include_router(rt)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try: 
        asyncio.run(main()) 

    except KeyboardInterrupt:
        print('Exit')