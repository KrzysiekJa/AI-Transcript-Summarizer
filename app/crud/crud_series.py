import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.crud.base import CRUDBase
from app.models.series import Series, Episode, Summary
from app.schemas.series import SeriesCreate, SeriesUpdate
from app.schemas.series import EpisodeCreate, EpisodeUpdate
from app.schemas.series import SummaryCreate, SummaryUpdate


class CRUDSeries(CRUDBase[Series, SeriesCreate, SeriesUpdate]):
    """CRUD operations for Series model."""

    pass


series = CRUDSeries(Series)


class CRUDEpisode(CRUDBase[Episode, EpisodeCreate, EpisodeUpdate]):
    """CRUD operations for Episode model."""

    async def get(self, db: AsyncSession, id: Any) -> Episode | None:
        """Get a single episode by ID, including its summary."""

        stmt = (
            select(Episode)
            .where(Episode.id == id)
            .options(selectinload(Episode.summary))
        )
        result = await db.exec(stmt)
        return result.first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[Episode]:
        stmt = (
            select(Episode)
            .options(selectinload(Episode.summary))
            .offset(skip)
            .limit(limit)
        )
        results = await db.exec(stmt)
        episodes = results.all()

        for episode in episodes:
            if episode.summary and episode.summary.content:
                episode.summary.content = json.loads(episode.summary.content)

        return episodes


episode = CRUDEpisode(Episode)


class CRUDSummary(CRUDBase[Summary, SummaryCreate, SummaryUpdate]):
    """CRUD operations for Summary model."""

    pass


summary = CRUDSummary(Summary)
