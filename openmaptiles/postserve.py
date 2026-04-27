import logging
from functools import partial
from typing import Union, List, Any, Dict

from asyncpg import Connection, ConnectionDoesNotExistError, PostgresLogMessage, \
    create_pool
from asyncpg.pool import Pool
# noinspection PyUnresolvedReferences
from tornado.ioloop import IOLoop
# noinspection PyUnresolvedReferences
from tornado.log import access_log
# noinspection PyUnresolvedReferences
from tornado.web import Application, RequestHandler

from openmaptiles.pgutils import show_settings, get_postgis_version, PgWarnings, \
    get_vector_layers
from openmaptiles.sqltomvt import MvtGenerator
from openmaptiles.tileset import Tileset


class RequestHandledWithCors(RequestHandler):
    def set_default_headers(self):
        pass

    def options(self):
        pass

    def head(self):
        # TODO: Technically here we should do a full tile/metadata retrieval,
        # but without sending the actual content back.
        # We must implement it to support QGIS
        pass


class GetTile(RequestHandledWithCors):
    pool: Pool
    query: str
    key_column: str
    test_geometry: bool
    gzip: bool
    verbose: bool
    connection: Union[Connection, None]
    cancelled: bool

    def initialize(self, pool, query, key_column, gzip, verbose, test_geometry):
        pass

    async def get(self, zoom, x, y):
        pass

    def on_connection_close(self):
        pass


class GetMetadata(RequestHandledWithCors):
    metadata: str

    def initialize(self, metadata):
        pass

    def get(self):
        pass


class Postserve:
    pool: Pool
    metadata: Dict[str, Any]
    generated_query: str

    def __init__(self, url, port, pghost, pgport, dbname, user, password,
                 layers, tileset_path, sql_file, key_column, disable_feature_ids,
                 gzip, verbose, exclude_layers, test_geometry):
        self.url = url
        self.port = port
        self.pghost = pghost
        self.pgport = pgport
        self.dbname = dbname
        self.user = user
        self.password = password
        self.tileset_path = tileset_path
        self.sql_file = sql_file
        self.layer_ids = layers
        self.exclude_layers = exclude_layers
        self.key_column = key_column
        self.gzip = gzip
        self.disable_feature_ids = disable_feature_ids
        self.test_geometry = test_geometry
        self.verbose = verbose

        self.tileset = Tileset.parse(self.tileset_path)

    def create_metadata(self,
                        urls: List[str],
                        vector_layers: List[dict],
                        ) -> Dict[str, Any]:
        """Convert tileset to the tilejson spec
           https://github.com/mapbox/tilejson-spec/tree/master/2.2.0#2-file-format
           A few optional parameters were removed as irrelevant
        """
        pass

    async def init_connection(self):
        pass

    def serve(self):
        pass
