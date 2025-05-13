from db.models import async_session, Channel
import logging



async def commit_date_to_db(data: dict, tg_id: int):
    async with async_session() as session:
        try:
            ad = Channel(
                tg_id=tg_id,
                channel=data['channel'],
                category=data['category_id'],
                cost=float(data['cost']),
                time=data['time'] 
            )

            session.add(ad)
            await session.commit()

            logging.info(f'Успешно сохранено в бд: {data["channel"]}')


        except Exception as e:
            await session.rollback()


            logging.info(f'Ошибка при внесении в бд {data["channel"]}')
            raise e