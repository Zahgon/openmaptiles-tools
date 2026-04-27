import json
from pathlib import Path
from openmaptiles.tileset import Tileset


def fp_to_dict(fp: Path) -> dict:
    pass


def get_ts_lyr_style_json_fp(yaml_fp: str) -> Path:
    pass


def add_order(lyrs: list) -> list:
    pass


def get_order(layer: dict) -> int:
    pass


def split(tileset_fp: Path, style_fp: Path):
    pass


def merge(tileset_fp: Path, style_fp: Path, style_header_fp: Path):
    pass
