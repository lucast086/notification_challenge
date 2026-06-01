from app.core.database import AsyncSessionLocal


async def get_async_session():
    """Yield an async database session for use in a request lifecycle."""
    async with AsyncSessionLocal() as session:
        yield session
