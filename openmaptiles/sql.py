import re
from typing import Union, Dict, Tuple

from sys import stderr

from openmaptiles.pgutils import quote_literal
from openmaptiles.tileset import Tileset, Layer


def collect_sql(tileset_filename, parallel=False, nodata=False
                ) -> Union[str, Tuple[str, Dict[str, str], str]]:
    """If parallel is True, returns a sql value that must be executed first, last,
        and a dict of names -> sql code that can be ran in parallel.
        If parallel is False, returns a single sql string.
        nodata=True replaces all '/* DELAY_MATERIALIZED_VIEW_CREATION */'
        with the "WITH NO DATA" SQL."""
    pass


def layer_to_sql(layer: Layer, nodata: bool):
    pass


def _sql_hint_clause(hint):
    pass


def sql_assert_table(table, hint, layer_id):
    pass


def sql_assert_func(func, hint, layer_id):
    pass


def get_slice_language_tags(tileset):
    pass


class FieldExpander:
    def __init__(self, field: str, layer: Layer, indent: str):
        field = [v for v in layer.fields if v.name == field]
        if len(field) != 1:
            raise ValueError(f'Field {field} was not found in layer {layer.id}')
        if not field[0].values:
            raise ValueError(f"Field '{field[0].name}' in layer {layer.id} "
                             f'has no defined values')
        self.field = field[0]
        self.layer = layer
        self.indent = indent

    def parse(self):
        pass

    def to_expression(self, map_to, mapping: Union[dict, list], op='OR', top=True):
        pass

    @staticmethod
    def sql_field(field):
        pass

    @staticmethod
    def sql_value(value):
        pass


def to_sql(sql: str, layer: Layer, nodata: bool):
    """Clean up SQL, and perform any needed code injections"""
    pass
