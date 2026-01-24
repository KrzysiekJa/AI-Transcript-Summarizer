import asyncio

from app.db.session import AsyncSessionLocal
from app.db.update_db import update_db


async def update():
    async with AsyncSessionLocal() as session:
        await update_db(session)


async def main():
    await update()


if __name__ == "__main__":
    asyncio.run(main())
