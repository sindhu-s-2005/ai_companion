# core/memory_store.py
import sqlite3
import time
from typing import Optional


class MemoryStore:
    def __init__(self, db_path: str = "memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            importance INTEGER NOT NULL,
            expires_at REAL,
            created_at REAL NOT NULL
        )
        """)
        self.conn.commit()
    def add_memory(
        self,
        key: str,
        value: str,
        importance: int,
        ttl_seconds: Optional[int] = None
    ):
        if not (1 <= importance <= 5):
            raise ValueError("importance must be between 1 and 5")

        expires_at = None
        if ttl_seconds:
            expires_at = time.time() + ttl_seconds

        self.conn.execute("""
        INSERT INTO memory (key, value, importance, expires_at, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (key, value, importance, expires_at, time.time()))
        self.conn.commit()
    def get_memory_summary(self, min_importance: int = 3) -> str | None:
        cursor = self.conn.execute("""
        SELECT key, value FROM memory
        WHERE importance >= ?
        AND (expires_at IS NULL OR expires_at > ?)
        """, (min_importance, time.time()))

        rows = cursor.fetchall()
        if not rows:
            return None

        summary_lines = [
            f"- {key}: {value}" for key, value in rows
        ]
        return "\n".join(summary_lines)
    def delete_expired(self):
        self.conn.execute("""
        DELETE FROM memory
        WHERE expires_at IS NOT NULL
        AND expires_at <= ?
        """, (time.time(),))
        self.conn.commit()
