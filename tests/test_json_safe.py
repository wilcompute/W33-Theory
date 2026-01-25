import json
from pathlib import Path
from decimal import Decimal
import numpy as np
from utils.json_safe import dump_json, load_json


def test_dump_and_load_numpy_and_decimal(tmp_path):
    p = tmp_path / 'test.json'
    data = {
        'npy_int': np.int64(42),
        'npy_arr': np.array([1, 2, 3]),
        'decimal': Decimal('3.14'),
        'normal': 7
    }
    dump_json(data, p, indent=2)
    loaded = load_json(p)

    assert loaded['npy_int'] == 42
    assert loaded['npy_arr'] == [1, 2, 3]
    # Decimal becomes string or numeric; allow numeric cast
    assert float(loaded['decimal']) == 3.14
    assert loaded['normal'] == 7
