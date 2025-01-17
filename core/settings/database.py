"""
Database singleton.
"""

import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional

from core.repositories.movie_repository import MovieRepository
from core.repositories.serie_repository import SerieRepository


class Database:
    _instance: Optional["Database"] = None
    _connection: Optional[Connection] = None

    def __new__(cls, db_name="database.db"):
        """
        Pending.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_name = db_name
        return cls._instance

    def __init__(self, db_name="database.db") -> None:
        """
        Pending.
        """
        if not hasattr(self, "db_name"):
            self.db_name: str = db_name

    def connect(self) -> Connection:
        if self._connection is None:
            self._connection: Connection = sqlite3.connect(self.db_name)
        return self._connection

    def setup(self) -> None:
        """
        Pending.
        """
        with self.connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS series (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                is_available INTEGER DEFAULT 1
            )
            """
            )

            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS movies (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL UNIQUE,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                is_available INTEGER DEFAULT 1
            )
            """
            )
            conn.commit()

    def close(self) -> None:
        """
        Pending.
        """
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_movie_repository(self) -> MovieRepository:
        """Returns a MovieRepository intance."""
        return MovieRepository(self.connect())

    def get_serie_repository(self) -> SerieRepository:
        """Returns a SerieRepository intance."""
        return SerieRepository(self.connect())
