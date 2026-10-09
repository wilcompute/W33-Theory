"""Exact shift-class and local-root necessary obstruction regression.

Fixture freezes the original 29 orbifolder base shifts with SHA256 provenance.
The external benchmark V is manually transcribed from 0708.2691 Eq E.1a.
"""
import json,sys
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_heterotic_benchmark_shift_screen as src
import w33_20261008_heterotic_benchmark_class_gate as gate
import w33_20261008_heterotic_benchmark_root_sieve as root
def load():
    obj=json.loads((ROOT/'data/w33_20261008_heterotic_base_shift_29.json').read_text())
    assert obj['z6ii_model_count']==128 and len(obj['base_shifts'])==29
    assert sum(x['ledger_model_count'] for x in obj['base_shifts'].values())==128
    return {label:tuple(F(x) for x in data['V']) for label,data in obj['base_shifts'].items()}
def test_published_shift_screen():
    bases=load()
    bench_c=gate.factor_signature(src.BENCH)
    bench_root=root.root_counts(src.BENCH)
    eligible_order=[];eligible_c=[];eligible_root=[]
    for label,V in bases.items():
        sig=gate.factor_signature(V)
        if sorted(z[0] for z in sig)==sorted(z[0] for z in bench_c):eligible_order.append(label)
        if sig==bench_c:eligible_c.append(label)
        if sig==bench_c and root.root_counts(V)==bench_root:eligible_root.append(label)
    assert len(eligible_order)==18
    assert len(eligible_c)==7
    assert eligible_root==['Z6II_34']
    assert bench_root==(44,84)
def test_weyl_lattice_shift_invariance_control():
    r=next(root.roots())
    V=src.BENCH
    moved=tuple(V[i]+(r[i] if i<8 else 0) for i in range(16))
    assert gate.factor_signature(V)==gate.factor_signature(moved)
    assert root.root_counts(V)==root.root_counts(moved)
    swapped=V[8:]+V[:8]
    assert gate.factor_signature(V)==gate.factor_signature(swapped)
    assert root.root_counts(V)==root.root_counts(swapped)
