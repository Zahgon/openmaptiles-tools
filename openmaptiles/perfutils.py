import shutil
from dataclasses import dataclass, field
from datetime import timedelta
from math import ceil
from sys import stdout
from typing import List, Dict, Any, Tuple

# noinspection PyUnresolvedReferences
from ascii_graph import Pyasciigraph
# noinspection PyUnresolvedReferences
from dataclasses_json import dataclass_json, config

from openmaptiles.utils import round_td, Bbox, deg2num

# If the terminal is not present, use this width
# In github, comments inside the ``` block are about 88 characters
DEFAULT_TERMINAL_WIDTH = 85


class Colors:
    GREEN = ''
    RED = ''
    RESET = ''

    def __init__(self) -> None:
        self.enable(stdout.isatty())

    def enable(self, enable=True):
        pass


COLOR = Colors()


def change(old, new, is_speed=False, color=False):
    pass


@dataclass_json
@dataclass
class PerfSummary:
    duration: timedelta = field(
        default=None,
        metadata=config(
            encoder=timedelta.total_seconds,
            decoder=lambda v: timedelta(seconds=v),
        ))
    tiles: int = 0
    bytes: int = 0
    tile_avg_size: float = 0
    gen_speed: float = 0

    def __post_init__(self):
        self.tile_avg_size = float(self.bytes) / self.tiles if self.tiles else 0
        if self.duration:
            self.gen_speed = float(self.tiles) / self.duration.total_seconds()

    def perf_format(self, old: 'PerfSummary'):
        pass

    def graph_msg(self, is_speed, group, old: 'PerfSummary'):
        pass


@dataclass_json
@dataclass
class PerfBucket:
    smallest_id: str = None
    smallest_size: int = None
    largest_id: str = None
    largest_size: int = None
    tiles: int = 0
    bytes: int = 0
    tile_avg_size: float = 0

    def __post_init__(self):
        self.tile_avg_size = float(self.bytes) / self.tiles if self.tiles else 0

    def graph_msg(self, old: 'PerfBucket'):
        pass


@dataclass_json
@dataclass
class PerfTestSummary(PerfSummary):
    id: str = None
    layers: str = None
    zoom: str = None
    buckets: List[PerfBucket] = field(default_factory=list)


@dataclass_json
@dataclass
class PerfRoot:
    created: str = None
    tileset: str = None
    pg_settings: Dict[str, str] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    layer_fields: Dict[str, List[str]] = field(default_factory=dict)
    tests: List[PerfTestSummary] = None
    summary: PerfSummary = None
    test_summary: Dict[str, PerfSummary] = field(default_factory=dict)
    zoom_summary: Dict[str, PerfSummary] = field(default_factory=dict)
    layer_summary: Dict[str, PerfSummary] = field(default_factory=dict)


@dataclass
class TestCase:
    id: str = None
    desc: str = None
    start: Tuple[int, int] = None  # inclusive tile coordinate (x,y)
    before: Tuple[int, int] = None  # exclusive tile coordinate (x,y)
    zoom: int = 14
    layers: List[str] = None
    layers_id: str = None
    query: str = None
    old_result: PerfTestSummary = None
    result: PerfTestSummary = None
    bbox: str = None

    def __post_init__(self):
        assert self.id and self.desc
        if self.start is None and self.before is None and self.bbox is not None:
            bbox = Bbox(self.bbox)
            self.start = deg2num(bbox.max_lat, bbox.min_lon, self.zoom)
            self.before = deg2num(bbox.min_lat, bbox.max_lon, self.zoom)
            self.before = (self.before[0] + 1, self.before[1] + 1)

        assert isinstance(self.start, tuple) and isinstance(self.before, tuple)
        assert len(self.start) == 2 and len(self.before) == 2
        assert self.start[0] <= self.before[0] and self.start[1] <= self.before[1]
        assert self.size() > 0 or (self.start == (0, 0) and self.before == (0, 0))
        if self.layers:
            if len(self.layers) == 1:
                self.layers_id = self.layers[0]
            else:
                self.layers_id = ','.join(self.layers)
        else:
            self.layers_id = '_all_'

    def make_test(self, zoom, layers, query) -> 'TestCase':
        pass

    def size(self) -> int:
        pass

    def fmt_table(self) -> str:
        pass

    def format(self) -> str:
        pass

    def fmt_layers(self):
        pass


def print_graph(header, data, is_bytes=False):
    pass
