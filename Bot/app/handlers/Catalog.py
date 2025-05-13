from aiogram.types import Message
from aiogram import F, Router
from app.handlers.buy import buy_rt
from .sell import sell_rt

import app.keyboards as kb


Catalog_rt = Router()
Catalog_rt.include_router(buy_rt)
Catalog_rt.include_router(sell_rt)

@Catalog_rt.message(F.text == 'Каталог')
async def Buy_or_sell_choose(message: Message):
    await message.answer('Ты хочешь купить рекламу или продать?', reply_markup=kb.buy_sell)


