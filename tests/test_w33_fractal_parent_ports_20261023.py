"""Verify every explicit 40-child interconnect port and its symplectic edge."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_port_fabric_20261023 import port_template, ADJ, LINE

def test_parent_full_960_link_template():
    p=port_template()
    assert p['logical_link_count']==960
    assert p['logical_terminations']==1920
    assert len(p['per_child_terminations'])==40
    assert set(p['per_child_terminations'].values())=={48}
    assert len({x['link_id'] for x in p['logical_links']})==960

def test_parent_exact_endpoint_pairing():
    p=port_template()
    names=set()
    counts={(i,g):0 for i in range(40) for g in LINE}
    for link in p['logical_links']:
        a,b=link['endpoints']
        assert b['child'] in ADJ[a['child']]
        assert a['child'] in ADJ[b['child']]
        assert a['gateway']==b['gateway'] and a['gateway'] in LINE
        assert a['peer']==b['child'] and b['peer']==a['child']
        for x in (a,b):
            assert x['logical_port'] not in names
            names.add(x['logical_port'])
            counts[(x['child'],x['gateway'])]+=1
    assert len(names)==1920
    assert set(counts.values())=={12}
