import os
import json


def _read_json(path):
    with open(path, "r") as f:
        return json.load(f)


_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_RESOURCES_DIR = os.path.join(_ROOT_DIR, "resources")

REFERENCE = _read_json(os.path.join(_RESOURCES_DIR, "iching_reference.json"))
BINARY_TO_DECIMAL = _read_json(os.path.join(_RESOURCES_DIR, "bin_to_dec.json"))
DECIMAL_TO_BINARY = {value: key for key, value in BINARY_TO_DECIMAL.items()}
