from db.models import async_session
from db.models import User, Category, Channel
from sqlalchemy import select


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        return categories
    

async def get_channels_by_category(category_id: int, channel_page: int):
    async with async_session() as session:
        result = await session.execute(select(Channel).filter(Channel.category == category_id).offset(channel_page*5).limit(5))
        channels = result.scalars().all()
        return channels
    
async def get_cost(channel_id: int):
    async with async_session() as session:
        result = await session.execute(select(Channel.cost).where(Channel.id == channel_id))
        cost = result.scalar_one_or_none()
        return cost

async def get_category_id(category_name: int):
    async with async_session() as session:
        result = await session.execute(select(Category.id).where(Category.name == category_name))
        category = result.scalar_one_or_none()
        return category
    

async def get_category_name(category_id: int):
    async with async_session() as session:
        result = await session.execute(select(Category.name).where(Category.id == category_id))
        category_name = result.scalar_one_or_none()
        return category_name
    
async def get_user_id_by_channel(channel: str):

    async with async_session() as session:
        result = await session.execute(select(Channel.tg_id).where(Channel.channel == channel))
        user_id = result.scalars().first()
        return user_id
