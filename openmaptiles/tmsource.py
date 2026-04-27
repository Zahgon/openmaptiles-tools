import collections

from .tileset import Tileset, Layer

DbParams = collections.namedtuple('DbParams',
                                  ['dbname', 'host', 'port', 'password', 'user'])


def generate_tm2source(tileset_filename, db_params):
    pass


def generate_layer(layer: Layer, db_params):
    pass
