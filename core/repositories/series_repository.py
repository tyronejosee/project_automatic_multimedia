from core.models.series_model import Series
from core.repositories.base_repository import BaseRepository


class SeriesRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__(Series, session)
