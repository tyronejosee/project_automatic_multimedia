from core.models.movie_model import Movie
from core.repositories.base_repository import BaseRepository


class MovieRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__(Movie, session)
