import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/PART_W33_PASS5238_5245_RESULTS.json'


def test_pass5238_5245_frontier_lock():
    d=json.loads(DATA.read_text())
    assert d['range']==[5238,5245]
    assert d['5238']['code']=='C_F=[325,65,25]_2'
    assert d['5238']['max_clique_census']['maximum_cliques']==156
    assert '936 chamber stars' in d['5238']['equality_consequence']
    assert d['5239']['weight9_shell_size']==117000
    assert d['5239']['span_rank']==260
    assert d['5240']['shortened_bounds']=={
        'lower':28,
        'upper':40,
        'reason_lower':'d(C_F)=25, all weight-25 words are point footprints and each meets the 13-cover once, while C_F weights are 0 or 1 mod 4',
        'upper_witness':'sum of two point rows in the same cover fibre, collinear case, weight 40'
    }
    assert d['5241']['q7']['orbital_rank']==5
    assert d['5242']['statement'].endswith('zero P-component parity vector.')
    assert d['5243']['even_subcode_minimum']==40
    assert d['5243']['minimum_even_words']==180
    assert d['5244']['anchors']['q7']['r_over_lambda']==48
    assert d['5245']['primal_code']=='C_F(q=7)=[1225,175,49]_2'
    assert d['5245']['dual_minimum']==12
    assert 'Leader36 is not yet eliminated' in d['strict_frontier']


def test_shell_moment_arithmetic():
    for r,lam,dmin in [(24,3,9),(600,25,25),(18816,392,49)]:
        assert r%lam==0
        assert 1+r//lam==dmin
    assert 25*25==625
    assert 624//40==15
