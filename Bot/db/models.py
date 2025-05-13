from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///Bot/db/db.sqlite3')


async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True, nullable=False)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


    channels: Mapped[list['Channel']] = relationship(back_populates='categories')


class Channel(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[str] = mapped_column(String, nullable=False)

    
    categories: Mapped['Category'] = relationship(back_populates='channels')



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
