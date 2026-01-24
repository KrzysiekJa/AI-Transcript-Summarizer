import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.series import Series, Episode, Summary
from app.config import SUMMARY_DIR


async def update_db(db: AsyncSession) -> None:
    results = await db.exec(select(Series).where(Series.name == "Python Bytes"))
    series = results.first()

    if not series:
        new_series = Series(
            name="Python Bytes", description="A podcast about Python news."
        )
        db.add(new_series)
        await db.flush()

    series_data = [
        {
            "title": "Malicious Package? No Build For You!",
            "summary_file": "python_bytes_ep_464_summary.json",
        },
        {
            "title": "2025 is @wrapped",
            "summary_file": "python_bytes_ep_463_summary.json",
        },
    ]

    for entry in series_data:
        summary_path = SUMMARY_DIR / entry["summary_file"]

        try:
            with open(summary_path, "r", encoding="utf-8") as file:
                summary_text = file.read()
        except IOError:
            summary_text = None

        episode_results = await db.exec(
            select(Episode).where(Episode.title == entry["title"])
        )
        episode = episode_results.first()

        if episode:
            summary_results = await db.exec(
                select(Summary).where(Summary.episode_id == episode.id)
            )
            summary = summary_results.first()

            if summary:
                summary.content = json.dumps(summary_text)
            else:
                new_summary = Summary(content=summary_text, episode_id=episode.id)
                db.add(new_summary)

        await db.commit()
        await db.close()
