from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.config import Settings

settings = Settings()

engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionLocal = async_sessionmaker[AsyncSession](bind=engine,
  expire_on_commit=False)