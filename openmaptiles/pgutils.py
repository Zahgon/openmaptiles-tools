from os import getenv
from typing import Dict, List

import asyncpg
from asyncpg import UndefinedFunctionError, UndefinedObjectError, Connection

from openmaptiles.perfutils import COLOR
from openmaptiles.utils import coalesce, print_err


async def get_postgis_version(conn: Connection) -> str:
    pass


async def show_settings(conn: Connection, verbose=True) -> Dict[str, str]:
    pass


def parse_pg_args(args, legacy_params=False):
    pass


class PgWarnings:
    def __init__(self, conn: Connection, delay_printing=False) -> None:
        self.messages = []
        self.delay_printing = delay_printing
        conn.add_log_listener(lambda _, msg: self.on_warning(msg))

    def on_warning(self, msg: asyncpg.PostgresLogMessage):
        pass

    @staticmethod
    def print_message(msg: asyncpg.PostgresLogMessage):
        pass

    def print(self):
        pass


async def get_sql_types(connection: Connection):
    """
    Get Postgres types that we can handle,
    and return the mapping of OSM type id (oid) => MVT style type
    """
    pass


async def get_vector_layers(conn, mvt) -> List[dict]:
    pass


def print_query_error(error_msg, err, pg_warnings, verbose, query, layer_sql=None):
    pass


def quote_literal(string):
    """Adapted from asyncpg.utils"""
    pass
