import sqlite3
from datetime import datetime


class DatabaseService:

    def __init__(self):
        self.conn = sqlite3.connect("fitness.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workout_sessions (
                session_id TEXT PRIMARY KEY,
                exercise_type TEXT,
                rep_count INTEGER,
                duration_seconds REAL,
                dominant_error TEXT,
                created_at TEXT
            )
        """)
        self.conn.commit()

    # ----------------------------
    # SAVE SESSION
    # ----------------------------
    def save_session(self, session_data: dict):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO workout_sessions (
                session_id,
                exercise_type,
                rep_count,
                duration_seconds,
                dominant_error,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_data["session_id"],
            session_data["exercise_type"],
            session_data["rep_count"],
            session_data["duration_seconds"],
            session_data["dominant_error"],
            datetime.utcnow().isoformat()
        ))

        self.conn.commit()

    # ----------------------------
    # GET SESSIONS
    # ----------------------------
    def get_sessions(self, limit: int = 50):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM workout_sessions
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # ----------------------------
    # GET STATS
    # ----------------------------
    def get_stats(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM workout_sessions")
        total_sessions = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COALESCE(SUM(rep_count), 0) FROM workout_sessions")
        total_reps = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COALESCE(SUM(duration_seconds), 0) FROM workout_sessions")
        total_duration = cursor.fetchone()[0] or 0

        return {
            "total_sessions": total_sessions,
            "total_reps": total_reps,
            "total_duration_seconds": total_duration
        }
