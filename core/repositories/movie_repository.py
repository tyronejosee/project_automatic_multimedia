from sqlite3 import Connection
from .base_repository import BaseRepository


class MovieRepository(BaseRepository):
    def __init__(self, db_connection: Connection) -> None:
        super().__init__(db_connection=db_connection, table_name="movies")
