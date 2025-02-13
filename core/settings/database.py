"""
Database singleton.
"""

import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional

from core.repositories.movie_repository import MovieRepository
from core.repositories.serie_repository import SerieRepository


class Database:
    """
    Singleton class for managing the SQLite database connection and setup.
    """

    _instance: Optional["Database"] = None
    _connection: Optional[Connection] = None

    def __new__(cls, db_name="database.db"):
        """
        Ensures that only one instance of the Database class exists.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_name = db_name
        return cls._instance

    def __init__(self, db_name="database.db") -> None:
        """
        Initializes the Database instance, ensuring the database name is set.
        """
        if not hasattr(self, "db_name"):
            self.db_name: str = db_name

    def connect(self) -> Connection:
        """
        Establishes and returns a connection to the SQLite database.
        """
        if self._connection is None:
            self._connection: Connection = sqlite3.connect(self.db_name)
        return self._connection

    def setup(self) -> None:
        """
        Creates the necessary tables for
        movies and series if they do not exist.
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
        Closes the database connection if it is open.
        """
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_movie_repository(self) -> MovieRepository:
        """
        Returns a MovieRepository intance.
        """
        return MovieRepository(self.connect())

    def get_serie_repository(self) -> SerieRepository:
        """
        Returns a SerieRepository intance.
        """
        return SerieRepository(self.connect())
