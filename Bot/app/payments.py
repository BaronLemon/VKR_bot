from aiogram.types import LabeledPrice
import json

payment_api = '381764678:TEST:122142'



async def send_invoice(callback, channel_name: str, channel_cost: int, channel_time: str, current_amount: int):
 
    price = [LabeledPrice(label='Оплата рекламного поста', amount=current_amount)]
    provider_data = json.dumps({
    "receipt": {
        "items": [
        {
            "description": f"User ID: {callback.from_user.id}. Channel: {channel_name}. Cost: {channel_cost}. Time: {channel_time}",
            "quantity": 1,
            "amount": {
              "value": channel_cost,
              "currency": "RUB"
            },
            "vat_code": 1,
            "payment_mode": "full_payment",
            "payment_subject": "service"
        }
        ]
    }
    })


    await callback.message.answer_invoice(
        title = 'Оплата рекламного поста',
        description=f'Канал: {channel_name}. Стоимость: {channel_cost}. Время подписки: {channel_time}',
        provider_token=payment_api,
        currency='RUB', 
        need_email=True,
        send_email_to_provider=True,
        is_flexible=False,
        prices= price,
        start_parameter='ad_buy',
        payload=f'{callback.from_user.id}',
        provider_data=provider_data
    )

