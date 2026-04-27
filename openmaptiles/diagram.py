import re
from pathlib import Path

from graphviz import Digraph
from typing import Tuple, List

from openmaptiles.tileset import process_layers, Layer


class GraphGenerator:
    def __init__(self, filename, output_dir, compare_dir, cleanup, extensions):
        self.messages = []
        self.filename = Path(filename)
        self.output_dir = Path(output_dir)
        self.compare_dir = Path(compare_dir) if compare_dir else None
        self.cleanup = cleanup
        self.extensions = extensions

    def do_layer(self, layer, is_tileset) -> None:
        pass

    def get_graph(self, layer: Layer, is_tileset: bool) -> Tuple[Digraph, Path]:
        pass

    def compare_file(self, dot_file, ext, new_file):
        pass

    def run(self) -> int:
        pass


class EtlGraph(GraphGenerator):
    # search for  '# etldoc:...' and '-- etldoc:...'
    re_mapping = re.compile(r'^\s*#\s*etldoc\s*:(.*)$')
    re_schema = re.compile(r'^\s*--\s*etldoc\s*:(.*)$')

    def get_graph(self, layer: Layer, is_tileset: bool) -> Tuple[Digraph, Path]:
        pass

    @staticmethod
    def parse_files(content_list: list, matcher: re) -> List[str]:
        pass


class MappingGraph(GraphGenerator):
    def get_graph(self, layer: Layer, is_tileset: bool) -> Tuple[Digraph, Path]:
        pass

    @staticmethod
    def generate_mapping_subgraph(name, mapping):
        pass
