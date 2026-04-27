import sqlite3
from typing import Iterable


def query(conn: sqlite3.Connection, sql: str, params: list) -> Iterable[tuple]:
    pass
