import json
import os
import sqlite3
from datetime import datetime
from os import getenv
from pathlib import Path
from sqlite3 import Cursor
from typing import Dict, List, Optional, Tuple

import asyncpg
from tabulate import tabulate

from openmaptiles.pgutils import get_postgis_version, get_vector_layers
from openmaptiles.sqlite_utils import query
from openmaptiles.sqltomvt import MvtGenerator
from openmaptiles.tileset import Tileset
from openmaptiles.utils import print_err, Bbox, print_tile, shorten_str


class KeyFinder:
    """Search mbtiles for frequently used duplicate tiles"""

    def __init__(self,
                 mbtiles,
                 show_size=None,
                 show_examples=None,
                 outfile: str = None,
                 zoom=None,
                 min_dup_count=None,
                 verbose=False) -> None:
        self.mbtiles = mbtiles
        if min_dup_count is not None:
            min_dup_count = int(min_dup_count)
            if min_dup_count < 2:
                raise ValueError('min_dup_count must be an integer â‰¥ 2')
            self.min_dup_count = min_dup_count
        else:
            self.min_dup_count = 50 if zoom and zoom > 12 else 20
        self.use_stdout = outfile == '-'
        self.zoom = zoom
        self.verbose = verbose
        if outfile:
            self.outfile = True if self.use_stdout else Path(outfile)
        else:
            self.outfile = None
        self.show_size = self.verbose if show_size is None else show_size
        self.show_examples = self.verbose if show_examples is None else show_examples

    def run(self):
        pass


class Imputer:

    def __init__(self, mbtiles, keys, zoom, outfile: str = None,
                 verbose=False) -> None:
        self.mbtiles = mbtiles
        self.keys = {k: 0 for k in keys}
        self.zoom = zoom
        self.use_stdout = outfile == '-'
        self.verbose = verbose or not self.use_stdout
        if outfile:
            self.outfile = True if self.use_stdout else Path(outfile)
        else:
            self.outfile = None

    def run(self):
        pass

    def tile_batches(self, conn: sqlite3.Connection, limit_to_keys=False):
        """Generate batches of tiles to be processed for the new zoom,
        based on the previous zoom level. Each yield contains two batches:
        one with 'empty' tiles (those that match known keys),
        and another with non-empty tiles (only if limit_to_keys is False).
        The first batch can be inserted into mbtiles db as is.
        The second batch will be used as a list of tiles to be generated.
        """
        pass


class Metadata:
    def __init__(self, mbtiles: str, show_json: bool = False,
                 show_ranges: bool = False) -> None:
        self.mbtiles = mbtiles
        self.show_json = show_json
        self.show_ranges = show_ranges

    def print_all(self, file: str = None):
        pass

    def get_value(self, name):
        pass

    def set_value(self, name, value):
        pass

    async def generate(self, tileset, reset, auto_minmax,
                       pghost, pgport, dbname, user, password):
        pass

    def copy(self, target_mbtiles, reset, auto_minmax):
        pass

    def show_tile(self, zoom, x, y, show_names, summary):
        pass

    def _update_metadata(self, metadata, auto_minmax, reset, file, center_zoom=None):
        pass

    @staticmethod
    def find_min_max_zoom(cursor, db_prefix='') -> Tuple[int, int]:
        pass

    @staticmethod
    def _get_metadata(file) -> Dict[str, str]:
        pass

    def _update_metadata_db(self, cursor, metadata, reset):
        pass

    def validate(self, name, value):
        pass


class TileCopier:
    """Copy tile data between mbtile files"""

    def __init__(self,
                 source: Metadata,
                 target: str,
                 zooms: List[int],
                 minzoom: Optional[int],
                 maxzoom: Optional[int],
                 reset: bool,
                 on_conflict: str,
                 auto_minmax: bool,
                 bbox: Optional[Bbox],
                 verbose: bool,
                 ) -> None:
        self.source = source
        self.target = Path(target)
        self.zooms = zooms
        self.minzoom = minzoom
        self.maxzoom = maxzoom
        self.reset = reset
        self.on_conflict = on_conflict
        self.auto_minmax = auto_minmax
        self.bbox = bbox
        self.verbose = verbose

    def run(self):
        pass

    def copy_tiles(self, cursor):
        pass

    def iterate_queries(self, cursor, sql):
        # For BBOX filter, perform one query per zoom,
        # otherwise run just one query for the whole DB
        pass

    def create_new_db(self) -> None:
        pass

    def execute(self, cursor: Cursor, sql: str, params=None):
        pass


sql_create_mbtiles = [
    'CREATE TABLE map (zoom_level INTEGER, tile_column INTEGER, tile_row INTEGER, tile_id TEXT);',
    'CREATE TABLE images (tile_data BLOB, tile_id TEXT);',
    """\
CREATE VIEW tiles AS
  SELECT
      map.zoom_level AS zoom_level,
      map.tile_column AS tile_column,
      map.tile_row AS tile_row,
      images.tile_data AS tile_data
  FROM map
  JOIN images ON images.tile_id = map.tile_id;""",
    'CREATE TABLE metadata (name text, value text);',
    'CREATE UNIQUE INDEX map_index ON map (zoom_level, tile_column, tile_row);',
    'CREATE UNIQUE INDEX images_id ON images (tile_id);',
    'CREATE UNIQUE INDEX name ON metadata (name);',
]
