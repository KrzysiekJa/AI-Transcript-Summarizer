from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# TODO: add cascade delete
# https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/#set-ondelete-to-cascade
class Series(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    episodes: List["Episode"] = Relationship(back_populates="series")


class Episode(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    url: Optional[str] = Field(max_length=512)
    series_id: int = Field(foreign_key="series.id", nullable=False)
    series: Series = Relationship(back_populates="episodes")
    summary: Optional["Summary"] = Relationship(back_populates="episode")
    transcript: Optional[str] = Field(nullable=True)


class Summary(SQLModel, table=True):
    id: int = Field(primary_key=True)
    content: str = Field(nullable=False)
    episode_id: int = Field(foreign_key="episode.id", nullable=False, unique=True)
    episode: Episode = Relationship(back_populates="summary")
