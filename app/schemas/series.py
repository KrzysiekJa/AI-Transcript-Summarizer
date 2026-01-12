from pydantic import BaseModel


# TODO: split into several files


class SeriesBase(BaseModel):
    title: str


class SeriesCreate(SeriesBase):
    pass


class SeriesUpdate(SeriesBase):
    pass


class SeriesInDBBase(SeriesBase):
    id: int

    class Config:
        from_attributes = True


class EpisodeBase(BaseModel):
    title: str
    url: str
    series_id: int


class EpisodeCreate(EpisodeBase):
    pass


class EpisodeUpdate(EpisodeBase):
    pass


class EpisodeInDBBase(EpisodeBase):
    id: int

    class Config:
        from_attributes = True


class Episode(EpisodeInDBBase):
    pass


class SummaryBase(BaseModel):
    content: str
    episode_id: int


class SummaryCreate(SummaryBase):
    pass


class SummaryUpdate(SummaryBase):
    pass


class SummaryInDBBase(SummaryBase):
    id: int

    class Config:
        from_attributes = True
