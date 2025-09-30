import asyncio
import logging

from app.db.session import AsyncSessionLocal
from app.db.init_db import init_db


# TODO: def logger confFile !!!
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with AsyncSessionLocal() as db_session:
        await init_db(db_session)


async def main() -> None:
    await init()
    logger.info("Initial data inserted...")


if __name__ == "__main__":
    asyncio.run(main())
