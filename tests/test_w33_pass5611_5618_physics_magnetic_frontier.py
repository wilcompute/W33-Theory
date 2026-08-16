from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(rel,name):
    p=ROOT/rel;spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(m);return m

def test_5611_affine_bands_small():
    m=load('analysis/w33_pass5611_general_q_heisenberg_magnetic_bulk.py','p5611')
    for q in (3,5): assert m.verify_anchor(q)['formula_verified']

def test_5612_prime_minwords_small_and_q9_frobenius():
    m=load('analysis/w33_pass5612_projectivity_minwords_semilinear.py','p5612')
    assert m.exhaustive_prime(3)['qualifying_minimum_graphs']==12
    assert m.exhaustive_prime(5)['qualifying_minimum_graphs']==60
    q9=m.q9_semilinear_check();assert q9['Frobenius_is_minimum_word'] and q9['P_Sigma_L2_constructed_order']==720

def test_5613_section_correction_and_lift_main(tmp_path,monkeypatch):
    m=load('analysis/w33_pass5613_intrinsic_heisenberg_vector_lift.py','p5613')
    P=m.p1();reps=[m.segre(u,v) for u in P for v in P]
    a=m.projective_matrix(reps);r=list(reps);r[0]=tuple(2*x%3 for x in r[0]);b=m.projective_matrix(r)
    assert round(m.tr_power(a,4))==2256 and round(m.tr_power(b,4))==2400
    ev=m.np.linalg.eigvalsh(m.lifted_matrix(reps))
    assert len(set(m.np.round(ev,8)))==7

def test_5614_q3_selectors():
    m=load('analysis/w33_pass5614_q3_physics_selector.py','p5614')
    r=m.row(3);assert r['fusion_relation_k2']==0 and r['fusion_multiplicity_m1']==0 and r['is_literal_double_cover']
    assert m.row(5)['fusion_relation_k2']>0 and not m.row(5)['is_literal_double_cover']

def test_5616_clifford_dispersion_runs():
    m=load('analysis/w33_pass5616_dirac_magnetic_dispersion.py','p5616')
    # main includes the full 128x128 H^2 and eigenvalue checks.
    m.main()

def test_5617_harper_runs():
    m=load('analysis/w33_pass5617_z3_gauge_harper.py','p5617');m.main()

def test_5618_neutrality_runs():
    m=load('analysis/w33_pass5618_gauge_matter_phase_selection.py','p5618');m.main()
