"""The real pezzotope partner signs recover the existing binary adjacency code."""

from collections import Counter
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def binary_span(generators):
    code = {0}
    for generator in generators:
        if generator not in code:
            code |= {word ^ generator for word in code}
    return code


def test_yoshida_partner_differences_generate_h10():
    path = ROOT / 'data/toe_20261109_real_yoshida_pezzotope_labels.json'
    result = json.loads(path.read_text(encoding='utf-8'))
    members = [frozenset(sum(triple, [])) for triple in result['yoshida_row_labels']]
    adjacency = [
        sum(1 << j for j, other in enumerate(members) if i != j and not (row & other))
        for i, row in enumerate(members)
    ]
    differences = {
        int(even, 16) ^ int(odd, 16)
        for even, odd, _ in result['chiral_pairs']['reflection_root_by_pair']
    }
    assert len(differences) == 216
    assert {word.bit_count() for word in differences} == {20}
    common_sign = (1 << 40) - 1
    assert all(word < (1 << 39) for word in differences)
    assert len(binary_span(differences)) == 512
    sign_code = binary_span(differences | {common_sign})
    assert sign_code == binary_span(adjacency)
    assert Counter(word.bit_count() for word in sign_code) == {
        0: 1, 12: 40, 16: 135, 20: 672, 24: 135, 28: 40, 40: 1,
    }
