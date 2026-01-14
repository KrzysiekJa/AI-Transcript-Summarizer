from types import SimpleNamespace

from .crud_series import series, episode, summary

# Provide a `crud` namespace for convenient imports like:
# from app.crud import crud
# then access `crud.episode`, `crud.series`, `crud.summary`
crud = SimpleNamespace(series=series, episode=episode, summary=summary)

__all__ = ["crud", "series", "episode", "summary"]
