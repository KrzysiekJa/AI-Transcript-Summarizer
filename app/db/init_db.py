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
        await db_session.flush()

    series_data = [
        {
            "title": "Malicious Package? No Build For You!",
            "url": "https://pythonbytes.fm/episodes/show/464/malicious-package-no-build-for-you",
            "transcript_file": "python_bytes_ep_464.txt",
        },
        {
            "title": "2025 is @wrapped",
            "url": "https://pythonbytes.fm/episodes/show/463/2025-is-wrapped",
            "transcript_file": "python_bytes_ep_463.txt",
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
    await db_session.flush()
    await db_session.commit()
    await db_session.close()
