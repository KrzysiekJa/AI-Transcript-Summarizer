from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import asyncsessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession


SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///transcript.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)

AsyncSessionLocal = asyncsessionmaker(
    expire_on_commit=False, autoflush=False, bind=engine, class_=SQLModelAsyncSession
)
