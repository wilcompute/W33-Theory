"""Independent regression controls for the chiral null gate and Wigner witness."""
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261113_chiral_null_order3_gate as G
import toe_20261113_chiral_null_wigner_magic as W

def test_integer_clock_identities():
    d=G.verify()
    assert d["gate"]["row_M_profile"]=={"5":1,"2":10,"-1":16}
    _,A,D=G.build()
    I=np.eye(27,dtype=np.int64)
    assert np.array_equal(D@D@D,-27*D)
    M=(18*I+3*D+D@D)//2
    assert np.array_equal(M.T@M,81*I)
    assert np.array_equal(M@M@M,729*I)

def test_four_direction_probability_bias():
    _,_,D=G.build()
    M=(18*np.eye(27,dtype=np.int64)+3*D+D@D)//2
    for v in G.FUTURE:
        j=G.VID[v]
        assert (M[0,j]**2-M[j,0]**2)==3
    assert all(sum(v[i] for v in G.FUTURE)%3==0 for i in range(3))

def test_exact_wigner_mana_and_entanglement():
    x=W.verify()
    assert x["wigner"]["integer_value_histogram"]=={"-9":432,"18":270,"45":27}
    assert x["wigner"]["l1_norm"]=="41/9"
    assert x["wigner"]["total_negative_mass"]=="16/9"
    assert x["entanglement"]["schmidt_ranks_over_Q_for_each_1_vs_2_cut"]=={
        "qutrit-1":3,"qutrit-2":2,"qutrit-3":3}

def test_outside_orientation_flip():
    _,_,D=G.build()
    idx=[G.VID[tuple((-x)%3 for x in v)] for v in G.V]
    assert np.array_equal(D[np.ix_(idx,idx)],-D)
