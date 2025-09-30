import logging

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from app.config import TRANSCRIPT_DIR
from app.models.series import Series, Episode


logger = logging.getLogger(__name__)


async def init_db(db_session: SQLModelAsyncSession) -> None:
    statement = select(Series).where(Series.name == "Python Bytes")
    query_result = await db_session.exec(statement)
    series = query_result.first()

    if not series:
        series = Series(name="Python Bytes")
        db_session.add(series)
        await db_session.commit()

    series_data = [
        {
            "title": "Can't Register for VibeCon",
            "url": "",
            "transcript_file": "",
        },
        {
            "title": "Cloud bills in scientific notation",
            "url": "",
            "transcript_file": "",
        },
    ]
    episodes = []

    for entry in series_data:
        try:
            transcript_path = TRANSCRIPT_DIR / entry["transcript_file"]
            with open(transcript_path, "r", encoding="utf-8") as file:
                transcript = file.read()
        except IOError:
            logger.error("Failed to read file %s", entry["transcript_file"])
            transcript = None

        episode = Episode(
            title=entry["title"], url=entry["url"], series=series, transcript=transcript
        )
        episodes.append(episode)

    db_session.add_all(episodes)
    await db_session.commit()
