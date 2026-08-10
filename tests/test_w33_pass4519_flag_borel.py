from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def test_flag_is_exact_sylow3_normalizer_borel():
    d=json.loads((ROOT/'data/PART_W33_PASS4519_FLAG_BOREL_SYLOW3_NORMALIZER.json').read_text(encoding="utf-8"))
    assert d['pass']==4519
    assert d['group_order']==25920
    assert (d['flag']['order'],d['flag']['index'])==(162,160)
    assert (d['sylow3']['order'],d['sylow3']['index_in_flag'],d['sylow3']['generators_used'])==(81,2,2)
    assert d['normalizer']['order']==162 and d['normalizer']['equals_flag_stabilizer'] is True
    assert d['cohomology_restriction']['radical_H1_dimension']==2
    assert d['cohomology_restriction']['restriction_kernel_dimension']==2
    assert d['cohomology_restriction']['all_three_nonzero_classes_killed'] is True


def test_borel_statement_is_chained_and_public():
    chain=(ROOT/'analysis/PASS4503_4510_apartment_obstruction_scaling_insert.tex').read_text(encoding="utf-8")
    assert chain.count('PASS4519_flag_borel_sylow3_normalizer_insert')==1
    page=(ROOT/'docs/apartment-obstruction-cohomology-gq.html').read_text(encoding="utf-8")
    card=(ROOT/'analysis/PASS4503_4510_apartment_obstruction_scaling_index_insert.html').read_text(encoding="utf-8")
    assert 'Borel/Sylow-3 normalizer' in page
    assert 'Borel' in card and 'Sylow-3' in card
