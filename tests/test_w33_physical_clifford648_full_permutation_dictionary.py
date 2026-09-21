from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_full_clifford648_dictionary_certificate():
    p=ROOT/"data/w33_physical_clifford648_full_permutation_dictionary.json"
    assert p.exists()
    o=json.loads(p.read_text())
    assert o["status"]=="PASS_ALL_648_PHYSICAL_QUTRIT_CLIFFORD_ELEMENTS_MAPPED_TO_W33_STABILIZER_PERMUTATIONS"
    assert o["orders"]=={"H27":27,"SL23":24,"normalizer":648}
    assert len(o["records"])==648
    assert o["full_multiplication_table_shape"]==[648,648]
    assert o["full_multiplication_table_digest"].startswith("sha256:")
    assert all(o["checks"].values())
