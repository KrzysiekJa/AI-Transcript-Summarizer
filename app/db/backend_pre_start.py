import asyncio
import logging

from sqlmodel import select

from app.db.session import AsyncSessionLocal


# TODO: def logger confFile !!!
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with AsyncSessionLocal() as db_session:
        try:
            # trying to create session to check if DB is awake
            await db_session.exec(select(1))
        except Exception as error:
            logger.error(error)
            raise error


async def main() -> None:
    logger.info("Initializing DB...")
    await init()
    logger.info("Finishing DB initialization...")


if __name__ == "__main__":
    asyncio.run(main())
