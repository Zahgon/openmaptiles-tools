import re

from typing import Iterable, Tuple, Dict, Set, Union, List, Callable

from asyncpg import Connection
# noinspection PyProtectedMember
from docopt import DocoptExit

from openmaptiles.tileset import Tileset, Layer
from openmaptiles.utils import find_duplicates


class MvtGenerator:
    layer_ids: Set[str]
    exclude_layers: bool  # if True, inverses layer_ids to use all except them

    def __init__(self,
                 tileset: Union[str, Tileset],
                 postgis_ver: str,
                 zoom: Union[None, str, int],
                 x: Union[None, str, int], y: Union[None, str, int],
                 layer_ids: List[str] = None, exclude_layers=False,
                 key_column=False, gzip: Union[int, bool] = False,
                 use_feature_id: bool = None, test_geometry=False,
                 order_layers: bool = False, extent=4096):
        if isinstance(tileset, str):
            self.tileset = Tileset.parse(tileset)
        else:
            self.tileset = tileset
        self.extent = extent
        self.pixel_width = self.tileset.pixel_scale
        self.pixel_height = self.tileset.pixel_scale
        self.key_column = key_column
        self.gzip = gzip
        self.test_geometry = test_geometry
        self.order_layers = order_layers
        self.set_layer_ids(layer_ids, exclude_layers)
        self.zoom = zoom
        self.x = x
        self.y = y

        # extract the actual version number
        # ...POSTGIS='2.4.8 r17696'...
        m = re.search(r'POSTGIS="([^"]+)"', postgis_ver)
        ver = m[1] if m else postgis_ver
        m = re.match(r'^(?P<major>\d+)\.(?P<minor>\d+)'
                     r'(\.(?P<patch>\d+)(?P<suffix>[^ ]*)?)?', ver)
        if not m:
            raise ValueError(f"Unparseable PostGIS version string '{postgis_ver}'")
        major = int(m['major'])
        minor = int(m['minor'])
        patch = int(m['patch']) if m['patch'] else 0
        if m['suffix'] != '':
            patch -= 1
        self.postgis_ver = (major, minor, patch)

        if self.postgis_ver < (3, 0):
            if use_feature_id:
                raise ValueError('Feature ID is only available in PostGIS v3.0+')
            self.use_feature_id = False
            self.tile_envelope = 'TileBBox'
        else:
            self.tile_envelope = 'ST_TileEnvelope'
            self.use_feature_id = True if use_feature_id is None else use_feature_id
        self.tile_envelope_margin = False

    def set_layer_ids(self, layer_ids: List[str], exclude_layers=False):
        pass

    def generate_sqltomvt_func(self, fname) -> str:
        """
        Creates a SQL function that returns a single bytea value or null
        """
        pass

    def generate_sqltomvt_preparer(self, fname) -> str:
        """
        Creates a SQL prepared statement returning 0 or 1 row with a single mvt column.
        """
        pass

    def generate_sql(self) -> str:
        pass

    def generate_layer(self, layer: Layer, order_layers=False) -> str:
        """
        Convert layer definition into a SQL statement.
        """
        pass

    def layer_to_query(self,
                       layer: Layer,
                       to_mvt_geometry=True,
                       mvt_geometry_wrapper: Callable[[str], str] = None,
                       extra_columns: str = None) -> str:
        pass

    def tile_to_bbox(self, layer: Layer, zoom, x, y):
        # A zoom 0 tile has width/height of 40075016.6855785 units
        # Buffer expressed as a percentage of a tile width gives us this formula.
        # Every subsequent zoom divides it by 2
        pass

    def bbox(self, zoom, x, y, margin=None):
        pass

    def substitute_sql(self, query, zoom, bbox):
        pass

    async def validate_layer_fields(
            self, connection: Connection, layer_id: str, layer: Layer
    ) -> Dict[str, str]:
        """Validate that fields in the layer definition match the ones
        returned by the dummy (0-length) SQL query.
        Returns field names => SQL types (oid) excluding the geometry field"""
        pass

    async def get_sql_fields(self, connection: Connection, layer: Layer) -> Dict[str, str]:
        """Get field names => SQL types (oid) by executing a dummy query"""
        pass

    def get_layers(self) -> Iterable[Tuple[str, Layer]]:
        pass
