
"""
SQLite persistence layer for the Traffic Monitoring System.
"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager
from config import DB_PATH


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_tables(self):
        schema = """
        CREATE TABLE IF NOT EXISTS vehicle_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER,
            vehicle_type TEXT,
            lane INTEGER,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS density_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_count INTEGER,
            density_level TEXT,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS speed_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER,
            vehicle_type TEXT,
            speed_kmph REAL,
            overspeed INTEGER,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            violation_type TEXT,
            track_id INTEGER,
            screenshot_path TEXT,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS signal_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            density_level TEXT,
            signal_duration INTEGER,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS prediction_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horizon_minutes INTEGER,
            predicted_volume REAL,
            timestamp TEXT
        );

        CREATE TABLE IF NOT EXISTS emergency_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT,
            lane INTEGER,
            timestamp TEXT
        );
        """
        with self._connect() as conn:
            conn.executescript(schema)

    def log_vehicle_event(self, track_id, vehicle_type, lane):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO vehicle_events (track_id, vehicle_type, lane, timestamp) VALUES (?,?,?,?)",
                (track_id, vehicle_type, lane, datetime.now().isoformat()),
            )

    def log_density(self, vehicle_count, density_level):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO density_log (vehicle_count, density_level, timestamp) VALUES (?,?,?)",
                (vehicle_count, density_level, datetime.now().isoformat()),
            )

    def log_speed(self, track_id, vehicle_type, speed_kmph, overspeed):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO speed_log (track_id, vehicle_type, speed_kmph, overspeed, timestamp) VALUES (?,?,?,?,?)",
                (track_id, vehicle_type, speed_kmph, int(overspeed), datetime.now().isoformat()),
            )

    def log_violation(self, violation_type, track_id, screenshot_path):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO violations (violation_type, track_id, screenshot_path, timestamp) VALUES (?,?,?,?)",
                (violation_type, track_id, screenshot_path, datetime.now().isoformat()),
            )

    def log_signal(self, density_level, signal_duration):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO signal_log (density_level, signal_duration, timestamp) VALUES (?,?,?)",
                (density_level, signal_duration, datetime.now().isoformat()),
            )

    def log_emergency(self, vehicle_type, lane):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO emergency_log (vehicle_type, lane, timestamp) VALUES (?,?,?)",
                (vehicle_type, lane, datetime.now().isoformat()),
            )

    def fetch_all(self, table: str, limit: int = 500):
        with self._connect() as conn:
            cur = conn.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?", (limit,))
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        return cols, rows