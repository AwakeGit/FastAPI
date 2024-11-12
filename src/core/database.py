from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"server_settings": {"client_encoding": "UTF8"}},
)


new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with new_session() as session:
        try:
            yield session
        finally:
            await session.close()
