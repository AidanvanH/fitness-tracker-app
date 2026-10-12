
import sqlite3
from pathlib import Path

from typing import Generator


# Project root: the folder containing fitness_tracker_app
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "fitness_tracker_app"


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Provide a separate SQLite connection for each API request."""

    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(
            f"Existing database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()
