import asyncio
import gzip
import math
import re
import sys
from asyncio.futures import Future
from collections import defaultdict
from datetime import timedelta
from functools import cmp_to_key
from typing import List, Callable, Any, Dict, Awaitable, Iterable, TypeVar, Union, Optional, Tuple

from betterproto import which_one_of
# noinspection PyProtectedMember
from docopt import DocoptExit
from tabulate import tabulate

from openmaptiles.vector_tile import TileFeature, TileLayer, Tile, TileGeomType

T = TypeVar('T')
T2 = TypeVar('T2')


def coalesce(*args):
    """Given a list of values, returns the first one that is not None"""
    pass


# From https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Lon..2Flat._to_tile_numbers_2
def deg2num(lat_deg, lon_deg, zoom):
    pass


class Bbox:
    def __init__(self, bbox=None,
                 left=-180.0, bottom=-85.0511, right=180.0, top=85.0511,
                 center_zoom=5) -> None:
        if bbox:
            left, bottom, right, top = bbox.split(',')
        self.min_lon = float(left)
        self.min_lat = float(bottom)
        self.max_lon = float(right)
        self.max_lat = float(top)
        try:
            # Allow both integer and float center zooms
            self.center_zoom = int(center_zoom)
        except ValueError:
            self.center_zoom = float(center_zoom)

    @staticmethod
    def from_geometry(geo):
        """Given GeoJSON geometry, compute the bounding box"""
        pass

    @staticmethod
    def from_polygon(content: str):
        pass

    def bounds_str(self):
        pass

    def bounds(self):
        pass

    def center_str(self, precision=1):
        pass

    def center(self):
        pass

    def to_tiles(self, zoom: int):
        """Convert current bbox into (min_x, min_y, max_x, max_y) tile coordinates for a given zoom.
        The result is inclusive for both the min and the max coordinates"""
        pass


class Action:
    _result: Future = None

    def __init__(self, action_id: str, depends_on: List[str] = None):
        self.action_id = action_id
        self.depends_on = depends_on or []


async def run_actions(actions: List[Action],
                      executor: Callable[[Action, List[Any]], Awaitable[Any]],
                      ignore_unknown: bool = False,
                      verbose: bool = False):
    """
    Executes all actions in parallel. If action lists dependencies,
    make sure dependent actions finish running first.
    :param actions: list of Action objects, each action having a unique ID, and
        with optional depends_on being an array of other action IDs that must complete
        before this action executes. The action._result is a Future.
        All other values will be ignored (could be used by executor).
    :param executor: runs a single action. Must return a future or be an async func.
        The returned is set as each action's result.
    :param ignore_unknown ignore when dependency ID is not found in actions
    :param verbose print additional debugging info
    :return: all action results
    """
    pass


def _validate_actions(
        actions: List[Action],
        remove_missing_deps=False,
        verbose=False,
) -> Dict[str, Action]:
    """
    Make sure there is no infinite loop, and all IDs exist and not duplicated
    :return dictionary of action IDs and corresponding action objects
    """
    pass


def find_duplicates(ids: List[str]) -> Iterable[str]:
    pass


def round_td(delta: timedelta):
    """Round timedelta by first digit after the dot"""
    pass


def print_err(*args, **kwargs):
    pass


def batches(items: Iterable[T], batch_size: int,
            decorator: Callable[[T], T2] = lambda v: v) -> Iterable[List[T2]]:
    """Given a stream of objects, create a stream of batches of those objects"""
    pass


def parse_zxy_param(param):
    pass


def parse_tags(feature: TileFeature, layer: TileLayer, show_names: bool,
               summary: bool) -> dict:
    pass


def dict_comparator(keys: List[str]):
    """Returns a key= comparator function that decides which of two dictionaries (rows) should be shown first.
    Basic logic: sort first by the type of a value, followed by the value itself.
    Try to parse a str value as an int and a float."""
    pass


def print_tile(data: bytes, show_names: bool, summary: bool, info: str, sort_output: bool = False) -> None:
    pass


def shorten_str(value: str, length: int) -> str:
    pass


def parse_zoom_list(zoom: Union[None, str, List[str]],
                    minzoom: Optional[str] = None,
                    maxzoom: Optional[str] = None) -> Optional[List[int]]:
    """Parse a user-provided list of zooms (one or more --zoom parameters),
       or if not given, parse minzoom and maxzoom.  Returns a list of zooms to work on. """
    pass


def parse_zoom(zooms: Union[None, str, List[str]], is_list: bool = False) -> Union[None, List[int], int]:
    """Parse a user-provided zoom or a list of zooms (one or more --zoom parameters).
    In some cases a list of zooms could be given even if a single zoom was required"""
    pass
