import uuid
from sqlite3 import Connection, Cursor


class BaseRepository:
    def __init__(
        self,
        db_connection: Connection,
        table_name: str,
    ) -> None:
        self.db_connection: Connection = db_connection
        self.table_name: str = table_name

    def exists(self, title: str) -> bool:
        """
        Checks if a movie with the given title exists in the database.
        """
        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                SELECT 1 FROM {self.table_name}
                WHERE title = ?
                LIMIT 1
            """
            cursor.execute(query, (title,))
            return cursor.fetchone() is not None

    def create(self, **kwargs: object) -> None:
        """
        Inserts a new record into the table.
        """
        columns: str = ", ".join(kwargs.keys())
        placeholders: str = ", ".join(["?" for _ in kwargs])
        values: tuple = tuple(kwargs.values())

        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                INSERT INTO {self.table_name} ({columns})
                VALUES ({placeholders})
            """
            cursor.execute(query, values)
            conn.commit()

    def create_batch(self, records: list[dict]) -> None:
        """
        Inserts multiple records into the table.
        """
        if not records:
            return

        # Generate unique IDs for records
        for record in records:
            if "id" not in record:
                record["id"] = str(uuid.uuid4())

        columns: str = ", ".join(records[0].keys())
        placeholders: str = ", ".join(["?" for _ in records[0]])
        values: list = [tuple(record.values()) for record in records]

        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                INSERT INTO {self.table_name} ({columns})
                VALUES ({placeholders})
            """
            cursor.executemany(query, values)
            conn.commit()

    def get_all(self) -> list[tuple]:
        """
        Retrieves all records from the table.
        """
        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                SELECT * FROM {self.table_name}
            """
            cursor.execute(query)
            return cursor.fetchall()

    def get_by_id(self, record_id: str) -> dict | None:
        """
        Retrieves a record by its ID.
        """
        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                SELECT * FROM {self.table_name}
                WHERE id = ?
            """
            cursor.execute(query, (record_id,))
            row: tuple = cursor.fetchone()
            if row:
                columns: list[str] = [
                    "id",
                    "title",
                    "created_at",
                    "updated_at",
                ]
                return dict(zip(columns, row))
            return None

    def update(self, record_id: str, **kwargs: object) -> None:
        """
        Updates a record by its ID.
        """
        updates: str = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values: tuple = tuple(kwargs.values()) + (record_id,)

        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                UPDATE {self.table_name}
                SET {updates}, updated_at = datetime('now')
                WHERE id = ?
            """
            cursor.execute(query, values)
            conn.commit()

    def delete(self, record_id: str) -> None:
        """
        Deletes a record by its ID.
        """
        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                DELETE FROM {self.table_name}
                WHERE id = ?
            """
            cursor.execute(query, (record_id,))
            conn.commit()

    def soft_delete(self, record_id: str) -> None:
        """
        Performs a logical deletion of a record by its ID.
        """
        with self.db_connection as conn:
            cursor: Cursor = conn.cursor()
            query: str = f"""
                UPDATE {self.table_name}
                SET is_available = 0, updated_at = datetime('now')
                WHERE id = ?
            """
            cursor.execute(query, (record_id,))
            conn.commit()
