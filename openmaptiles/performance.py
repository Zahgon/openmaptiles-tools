import json
from collections import defaultdict
from datetime import timedelta, datetime as dt
from pathlib import Path
from typing import Dict, List, Callable, Any, Union

import asyncpg
from asyncpg import Connection
# noinspection PyProtectedMember
from docopt import DocoptExit

from openmaptiles.perfutils import change, PerfSummary, PerfBucket, \
    PerfRoot, TestCase, print_graph
from openmaptiles.pgutils import show_settings, get_postgis_version
from openmaptiles.sqltomvt import MvtGenerator
from openmaptiles.tileset import Tileset
from openmaptiles.utils import round_td

# All test cases are defined on z14 by default. Second x,y pair is exclusive.
# ATTENTION: Do not change tile ranges once they are published
# Use this site to get tile coordinates (use Google's variant)
# https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection/
TEST_CASES: Dict[str, TestCase] = {v.id: v for v in [
    TestCase(
        'us-across',
        'A line from Pacific ocean across US via New York and some Atlantic ocean',
        (2490, 6158), (4851, 6159)),  # DO NOT CHANGE THESE COORDINATES
    TestCase(
        'eu-prague',
        'A region around Prague of mixed urban and country side, CZ',
        (8832, 5536), (8863, 5567)),  # DO NOT CHANGE THESE COORDINATES
    TestCase(
        'eu-london',
        'A dense urban region around London, UK',
        (8175, 5441), (8192, 5452)),  # DO NOT CHANGE THESE COORDINATES
    TestCase(
        'eu-paris',
        'A dense urban region around Paris with all buildings, FR',
        (8289, 5629), (8307, 5643)),  # DO NOT CHANGE THESE COORDINATES
    TestCase(
        'ocean',
        'Ocean tiles without much content',
        (8065, 8065), (8302, 8101)),  # DO NOT CHANGE THESE COORDINATES
    TestCase(
        'null',
        'Empty set, useful for query validation.',
        (0, 0), (0, 0)),  # DO NOT CHANGE THESE COORDINATES
]}


class PerfTester:
    mvt: MvtGenerator
    test_cases: List[TestCase]

    def __init__(self, tileset: str, tests: List[str], test_all, layers: List[str],
                 zooms: List[int], dbname: str, pghost, pgport: str, user: str,
                 password: str, summary: bool, per_layer: bool, buckets: int,
                 save_to: Union[None, str, Path], compare_with: Union[None, str, Path],
                 key_column: bool, gzip: bool, disable_feature_ids: bool,
                 exclude_layers: bool, verbose: bool, bboxes: List[str]):
        self.tileset = Tileset.parse(tileset)
        self.dbname = dbname
        self.pghost = pghost
        self.pgport = pgport
        self.user = user
        self.password = password
        self.summary = summary
        self.buckets = buckets
        self.key_column = key_column
        self.gzip = gzip
        self.disable_feature_ids = disable_feature_ids
        self.verbose = verbose
        self.per_layer = per_layer
        self.save_to = Path(save_to) if save_to else None
        self.results = PerfRoot()

        if compare_with:
            path = Path(compare_with).resolve()
            with path.open('r', encoding='utf-8') as fp:
                self.old_run: PerfRoot = PerfRoot.from_dict(json.load(fp))
            since = round_td(dt.utcnow() - dt.fromisoformat(self.old_run.created))
            print(f'Comparing results with a previous run created {since} ago: {path}')
        else:
            self.old_run = None

        self.all_test_cases = TEST_CASES.copy()

        # Fake bbox tests as if they were defined, and create names for them
        for bbox_idx, bbox in enumerate(bboxes, start=1):
            tc = TestCase(f'bbox_test_{bbox_idx}', bbox, bbox=bbox)
            self.all_test_cases[tc.id] = tc
            tests.append(tc.id)

        for test in tests:
            if test not in self.all_test_cases:
                cases = '\n'.join(map(TestCase.fmt_table, self.all_test_cases.values()))
                raise DocoptExit(f"Test '{test}' is not defined. "
                                 f'Available tests are:\n{cases}\n')
        if test_all:
            # Do this after validating individual tests, they are ignored but validated
            tests = [v for v in self.all_test_cases.keys() if v != 'null']
        all_layers = [v.id for v in self.tileset.layers]
        if layers and exclude_layers:
            # inverse layers list
            layers = [v for v in all_layers if v not in layers]
        elif not layers and per_layer:
            layers = all_layers
        # Keep the order, but ensure no duplicates
        self.layers = list(dict.fromkeys(layers))
        self.tests = list(dict.fromkeys(tests))
        self.zooms = list(dict.fromkeys(zooms))

    async def run(self):
        pass

    async def _run(self, conn: Connection):
        pass

    def create_testcase(self, test, zoom, layers) -> TestCase:
        pass

    async def run_test(self, conn: Connection, test: TestCase):
        pass

    def print_summary_graphs(self, kind, key: Callable[[TestCase], Any],
                             key_fmt: Callable[[TestCase], Any], long_msg):
        pass

    def save_results(self):
        pass
