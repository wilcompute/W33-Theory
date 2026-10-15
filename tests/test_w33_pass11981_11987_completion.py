"""Independent physical-scope and exact-witness checks for seven fronts."""
import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))


def saved(name):return json.loads((ROOT/'data'/name).read_text())


def test_flavour_full_uv_cp_witnesses_are_nondegenerate():
    from w33_pass11981_cubic_mediator_cp import determinant_energy_gradient,yukawa
    d=saved('w33_pass11981_cubic_mediator_cp.json')['third_triplet_determinant_probe']
    good=[r for r in d['draws'] if r['Jarlskog'] is not None and abs(r['Jarlskog'])>1e-5]
    assert len(good)>=5
    for r in good:
        x=np.array(r['x']);args=tuple(np.array(r[k]) for k in ('M','weights','constants','lambdas'))+(r['g'],r['mu'])
        _,g=determinant_energy_gradient(x,*args)
        assert max(abs(g))<1e-6
        assert len(r['full_UV_44_real_Hessian'])==44 and min(r['full_UV_44_real_Hessian'])>1e-3
        assert min(r['full_18_real_Hessian'])>1e-3 and r['minimum_squared_mass_gap']>.01
        h=x[:3]+1j*x[3:6];f=x[6:9]+1j*x[9:12]
        a=yukawa(h,[1,.1,.1]);b=yukawa(f,[1,.2,.2]);a=a@a.conj().T;b=b@b.conj().T;c=a@b-b@a
        assert abs(np.trace(c@c@c).imag-r['weak_CP_trace'])<1e-10
        determinant=np.linalg.det(yukawa(h,[1,.1,.1]))*np.linalg.det(yukawa(f,[1,.2,.2]))
        assert abs(np.angle(determinant)-r['naive_mass_determinant_phase'])<1e-10


def test_flavour_mediator_interference_and_conjugate_vacua():
    d=saved('w33_pass11981_cubic_mediator_cp.json')
    assert d['weak_CP_transmitting_stable_draw_count']==0
    p=d['third_triplet_determinant_probe']
    assert len(p['zero_interference_controls'])>=5
    assert max(abs(r['weak_CP_trace']) for r in p['zero_interference_controls'])<1e-12
    for r in p['draws']:
        assert abs(r['combined_CP_partner_weak_trace']+r['weak_CP_trace'])<1e-10
        assert r['combined_CP_partner_energy_error']<1e-9
        assert r['UV_effective_energy_identity_error']<1e-9


def test_flavour_analytic_gradient_in_an_independent_direction():
    from w33_pass11981_cubic_mediator_cp import determinant_energy_gradient
    r=saved('w33_pass11981_cubic_mediator_cp.json')['third_triplet_determinant_probe']['draws'][3]
    x=np.array(r['x'])+np.linspace(-.03,.02,18);args=tuple(np.array(r[k]) for k in ('M','weights','constants','lambdas'))+(r['g'],r['mu'])
    direction=np.sin(np.arange(18)+.3);direction/=np.linalg.norm(direction)
    analytic=determinant_energy_gradient(x,*args)[1]@direction
    fd=(determinant_energy_gradient(x+1e-6*direction,*args)[0]-determinant_energy_gradient(x-1e-6*direction,*args)[0])/2e-6
    assert abs(analytic-fd)<1e-6


def test_full_gauss_ring_background_change_is_unitary():
    from w33_pass11982_quantum_gauss_holonomies import ring
    h,m=ring(0,3);shifted,_=ring(.713,3)
    u=np.diag(np.exp(-.713j*m))
    assert len(m)==42 and np.max(abs(shifted-u@h@u.conj().T))<1e-12
    free,_=ring(0,3,V=0)
    assert abs(np.linalg.eigvalsh(free)[0]-np.linalg.eigvalsh(h)[0])>.01


def test_native_gauss_metric_harmonic_controls():
    from w33_pass11982_quantum_gauss_holonomies import payload
    d=payload();rows=d['harmonic_quantization']
    assert d['gauge_representative_metric_error']<1e-10
    assert d['native_metric_smallest_eigenvalue']>0
    assert max(r['frequency_over_fermi_gap'] for r in rows)<.002
    assert max(r['maximum_link_phase_RMS'] for r in rows)<.33


@lru_cache(None)
def atlas():
    from w33_pass11983_atlas_projector_descent import payload
    return payload()


def test_all_native_e6_charts_and_transport_are_rebuilt():
    d=atlas();assert d['assembled_rank']==15
    assert d['overlap_mismatch_histogram']=={'centers_collinear=0,changed_edges=16':540,'centers_collinear=1,changed_edges=36':240}
    assert d['canonical_projection_transport_histogram']=={'centers_collinear=0,rank=6,Tr_Qp_Qr=792':540,'centers_collinear=1,rank=2,Tr_Qp_Qr=648':240}


def test_exact_serialized_holonomies_are_metric_isometries_with_noninteger_trace():
    d=atlas()['compact_holonomy_closure'];G=sp.Matrix(d['source_fiber_Gram']);loops=[]
    for row in d['first_three_loop_matrices_Q_sqrt3']:
        a=sp.Matrix([[sp.Rational(x) for x in r] for r in row['rational']]);b=sp.Matrix([[sp.Rational(x) for x in r] for r in row['sqrt3_coefficient']]);h=a+sp.sqrt(3)*b
        assert (h.T*G*h-G).applyfunc(sp.simplify)==sp.zeros(6);loops.append(h)
    assert sp.simplify(sp.trace(loops[0]*loops[1]))==sp.Rational(-3,8)
    assert d['first_three_triangle_determinants']==['-1','-1','-1']


def test_density_uses_exact_rank_witnesses_over_two_fields():
    d=atlas()['compact_holonomy_closure']
    assert d['wedge2_commutant_rank_progress']==[168,221,224]
    assert d['second_rank_progress']==[168,221,224]
    assert d['full_compact_closure_O6_proved'] and d['identity_component_SO6_proved']


def test_spin_lifts_are_su4_nonclifford_entangling_gates():
    from w33_pass11987_atlas_spin_gate_alphabet import payload
    d=payload();assert d['gate_count']==5
    for r in d['gates']:
        u=np.array(r['gate_real'])+1j*np.array(r['gate_imag'])
        assert np.max(abs(u.conj().T@u-np.eye(4)))<1e-10
        assert abs(np.linalg.det(u)-1)<1e-9 and r['spin_cover_error']<1e-9
    assert d['largest_nonClifford_witness']>.6 and d['largest_00_concurrence']>.69


def test_hybrid_chiral_regulator_optical_decoupling_and_full_su5_anomalies():
    from w33_pass11984_native_fiber_overlap import payload
    d=payload();assert d['full_hybrid_spinor_dimension']==25920
    assert d['total_charge1_overlap_index']==1
    assert all(r['index_per_sector']==0 for r in d['native_optical_sectors'][1:])
    assert d['local_spectral_tensor_action_error']<1e-10
    su5=d['explicit_chiral_SU5_extension'];assert su5['all_ordered_cubic_anomaly_entries_checked']==13824
    assert su5['max_Tr_Ta_anticommutator_Tb_Tc']<1e-13


def test_nonlinear_metric_clock_closure_does_not_remove_physical_pairs():
    from w33_pass11985_nonlinear_metric_clock import payload
    d=payload();assert d['bare_clock_bracket']!='0' and d['exact_dressed_clock_bracket']=='0'
    assert d['quartic_metric_potential'] and d['quartic_matter_interaction']
    assert d['physical_real_phase_dimension']==4 and d['constraint_count']==2


def test_parallel_logical_surgery_keeps_some_order9_vacua():
    from w33_pass11986_logical_modular_descent import payload
    d=payload();assert d['integral_H1_coinvariant_factors']==[3,9]
    assert d['F3_radical_dimensions']==[26,24,21,15,11,6,3,1,0]
    assert d['center_nilpotent_power_ranks']==[16,7,0]
    assert d['surviving_original_243_holonomy_count']==27
    assert not d['selected_stable_N18_order9_survives']
    assert len(d['surviving_original_N18_minimizers'])==4
