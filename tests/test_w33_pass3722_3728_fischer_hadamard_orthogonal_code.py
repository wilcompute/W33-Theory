import json
import runpy
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'analysis' / 'w33_pass3722_3728_fischer_hadamard_orthogonal_code.py'
FROZEN = ROOT / 'data' / 'PART_3722_3728_FISCHER_HADAMARD_ORTHOGONAL_CODE_results.json'


@lru_cache(maxsize=1)
def build():
    return runpy.run_path(str(SOURCE))['build_certificate']()


def test_frozen_certificate_exact():
    assert build() == json.loads(FROZEN.read_text(encoding='utf-8'))


def test_load_bearing_invariants():
    got = build()
    assert got['semantic_sha256'] == 'dd23c386c7dee92be7a91817018bd737e9efb7fe050354be6bbf91952c59e525'
    assert got['fischer_miyamoto_closure']['full_group_order'] == 51840
    assert got['fischer_miyamoto_closure']['even_product_subgroup_order'] == 25920
    assert got['binary_orthogonal_code']['weight_distribution'] == {'0': 1, '16': 27, '20': 36}
    assert got['triple_block_three_cover']['holonomy_group'] == 'S3'
    assert got['triple_block_three_cover']['deck_group'] == 'trivial'
    assert got['axial_rigidity']['derivation_dimension_over_Q'] == 0
    assert got['hadamard_naimark_completion']['identity'] == 'K K^T = 36 I'
