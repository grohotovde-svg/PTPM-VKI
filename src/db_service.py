import sqlite3
import json
from typing import Optional, Dict, Any


class DatabaseService:
    """Класс для сохранения и получения результатов из БД SQLite."""

    def __init__(self, db_path: str = "triangles.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS triangles (
                    side_a TEXT,
                    side_b TEXT,
                    side_c TEXT,
                    triangle_type TEXT,
                    coords TEXT,
                    error_message TEXT,
                    PRIMARY KEY (side_a, side_b, side_c)
                )
            """)
            conn.commit()

    def add_record(self, str_a: str, str_b: str, str_c: str, t_type: str, coords: list, error_msg: str) -> bool:
        """Метод добавления записи в БД."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO triangles (side_a, side_b, side_c, triangle_type, coords, error_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (str_a, str_b, str_c, t_type, json.dumps(coords), error_msg))
                conn.commit()
                return True
        except Exception:
            return False

    def get_record(self, str_a: str, str_b: str, str_c: str) -> Optional[Dict[str, Any]]:
        """Метод получения записи из БД по трем сторонам."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT triangle_type, coords, error_message FROM triangles
                WHERE side_a = ? AND side_b = ? AND side_c = ?
            """, (str_a, str_b, str_c))
            row = cursor.fetchone()
            if row:
                return {
                    "triangle_type": row[0],
                    "coords": json.loads(row[1]),
                    "error_message": row[2]
                }
            return None

    def delete_record(self, str_a: str, str_b: str, str_c: str) -> bool:
        """Метод удаления записи из БД."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM triangles WHERE side_a = ? AND side_b = ? AND side_c = ?
            """, (str_a, str_b, str_c))
            conn.commit()
            return cursor.rowcount > 0