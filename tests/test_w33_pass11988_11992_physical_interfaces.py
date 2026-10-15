"""Independent maps, direct UV, Schrodinger and full metric controls."""
import importlib
import itertools
import json
import sys
from functools import lru_cache
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
STEMS={11988:'spinor_weil_intertwiner',11989:'joint_source_barr',11990:'odd_even_holonomic_controls',11991:'native_four_period_cover',11992:'nonlinear_einstein_benchmark'}


def module(n):return importlib.import_module(f'w33_pass{n}_{STEMS[n]}')
def saved(n):return json.loads((ROOT/f'data/w33_pass{n}_{STEMS[n]}.json').read_text())
@lru_cache(None)
def fresh(n):return module(n).payload()


def test_same_label_weil_intertwiner_obstruction_is_exact():
    d=fresh(11988);assert d['Hom_dimension_over_Q_omega']==0
    assert d['exact_Q_omega_canonical_Pauli_conjugations_checked']==52
    assert d['exact_trace_obstruction']['atlas_characteristic_polynomial']=='(x - 1)**4*(x**2 + x + 1)'
    assert d['exact_trace_obstruction']['Weil_exterior_square_characteristic_polynomial']=='(x**2 + x + 1)**3'
    for cert in d['Hom_modular_full_rank_certificates'].values():assert cert['progress']==[18,32,36]
    assert d['Hom_modular_full_rank_certificates']==saved(11988)['Hom_modular_full_rank_certificates']


def test_projective_tangent_repair_names_an_exact_map_and_complex_structure():
    d=fresh(11988)['exact_projective_tangent_repair'];S=s.Matrix(d['intertwiner_integer_matrix'])
    assert S.det()==9 and d['Hom_dimension_over_Q']==2
    J=s.Matrix(d['complex_structure_numerator_Q']);assert J*J==-3*s.eye(6)
    assert d['finite_stabilizer_preserves_J']
    assert all(s.sympify(r['exact_metric_Frobenius_commutator_squared'])>0 for r in d['polar_holonomy_commutator_controls'])
    assert d['intertwiner_integer_matrix']==saved(11988)['exact_projective_tangent_repair']['intertwiner_integer_matrix']


def test_odd_data_and_even_auxiliaries_are_actual_two_qutrit_subspaces():
    m=module(11988);O,E=m.odd_encoding();assert O.shape==(9,4) and E.shape==(9,5)
    assert np.max(abs(np.c_[O,E].T@np.c_[O,E]-np.eye(9)))<1e-14
    states=list(itertools.product(range(3),repeat=2));P=np.zeros((9,9))
    for j,x in enumerate(states):P[states.index(tuple((-a)%3 for a in x)),j]=1
    assert np.max(abs(P@O+O))<1e-14 and np.max(abs(P@E-E))<1e-14


def test_joint_source_gradient_matches_a_directional_energy_difference():
    m=module(11989);prior=json.loads((ROOT/'data/w33_pass11981_cubic_mediator_cp.json').read_text())['third_triplet_determinant_probe']['draws'][3]
    args=m.args_of(prior);row=next(r for r in fresh(11989)['scan'] if r['prior_draw']==3 and r['kappa']==4)
    z=np.array(row['z'])+np.linspace(-.01,.015,19);v=np.cos(np.arange(19)+.2);v/=np.linalg.norm(v)
    analytic=m.joint_value_gradient(z,args,4)[1]@v
    fd=(m.joint_value_gradient(z+1e-6*v,args,4)[0]-m.joint_value_gradient(z-1e-6*v,args,4)[0])/2e-6
    assert abs(analytic-fd)<2e-7


def test_direct_45_field_uv_energy_has_the_reported_hessian():
    m=module(11989);prior=json.loads((ROOT/'data/w33_pass11981_cubic_mediator_cp.json').read_text())['third_triplet_determinant_probe']['draws'][3]
    args=m.args_of(prior);row=next(r for r in fresh(11989)['scan'] if r['prior_draw']==3 and r['kappa']==4)
    z=np.array(row['z']);mass2=np.r_[args[0]**2,np.ones(9)];chi=-m.heavy_sources(z,args)/mass2
    point=np.r_[z,chi.real,chi.imag]
    def energy(y):
        light=y[:19];heavy=y[19:32]+1j*y[32:45]
        norms=[np.vdot(v,v).real for v in m.fields(light[:18])]
        radial=sum(10*(a-1)**2+.01*a**4 for a in norms)+(light[18]**2-1)**2
        return float(radial+np.sum(mass2*abs(heavy)**2+2*np.real(heavy.conj()*m.heavy_sources(light,args))))
    eps=2e-4;H=np.zeros((45,45));eye=np.eye(45);base=energy(point)
    for i in range(45):
        H[i,i]=(energy(point+eps*eye[i])-2*base+energy(point-eps*eye[i]))/eps**2
        for j in range(i):
            H[i,j]=H[j,i]=(energy(point+eps*(eye[i]+eye[j]))-energy(point+eps*(eye[i]-eye[j]))-energy(point+eps*(-eye[i]+eye[j]))+energy(point-eps*(eye[i]+eye[j])))/(4*eps**2)
    assert min(np.linalg.eigvalsh(H))>1e-3
    assert np.allclose(np.linalg.eigvalsh(H),row['all45_UV_eigenvalues'],atol=4e-4,rtol=2e-5)


def test_source_relaxation_preserves_stability_but_can_erase_weak_cp():
    d=fresh(11989);assert d['stable_local_witness_count']==20 and d['weak_CP_local_witness_count']==18
    for row in d['scan']:
        assert row['gradient_max']<1e-6 and min(row['all45_UV_eigenvalues'])>8e-4
        assert row['source_relaxed_Schur_curvature']>3.6
        assert abs(row['Jarlskog']+row['CP_partner_J'])<1e-8
    soft=next(r for r in d['scan'] if r['prior_draw']==9 and r['kappa']==1)
    stiff=next(r for r in d['scan'] if r['prior_draw']==9 and r['kappa']==4)
    assert abs(soft['Jarlskog'])<1e-6 and abs(stiff['Jarlskog'])>1e-4


def test_barr_matching_uses_real_couplings_on_the_relaxed_vacuum():
    m=module(11989);d=fresh(11989);r=next(r for r in d['scan'] if r['prior_draw']==3 and r['kappa']==4)
    b=d['matched_Barr_from_actual_relaxed_vacuum'];h=m.fields(np.array(r['z'])[:18])[0]
    B=np.array(b['real_C'])@h
    assert max(abs(B-(np.array(b['B_real'])+1j*np.array(b['B_imag']))))<1e-12
    assert abs(b['matched_J']-3.08e-5)<1e-11 and abs(b['matched_J']+b['conjugate_J'])<1e-11
    assert b['positive_full_mass_determinant_real']>0 and abs(b['full_mass_determinant_imag'])<1e-12
    assert abs(b['forbidden_zero_block_phase_derivative'])>.1


def test_kato_control_transports_the_actual_projector_without_dark_energy():
    m=module(11990);U=m.gates()[2][1]
    for t in (.23,.81,1.31,1.67,2.24,2.71):
        P,Pd=m.dark_path(U,t);H=m.hamiltonian(U,t)
        assert np.max(abs(Pd+1j*(H@P-P@H)))<1e-11
        assert np.max(abs(P@H@P))<1e-11


def test_full_schrodinger_evolution_realizes_all_five_gates():
    d=fresh(11990)
    for row in d['gate_checks']:
        assert row['encoded_operator_max_error']<1e-8 and row['leakage_operator_norm']<1e-8
        assert row['max_sampled_parity_commutator']>.5
        assert row['midpoint_Weyl_reconstruction_error']<1e-11
    assert d['no_counterdiabatic_controls'][0]['leakage_operator_norm']>.9


def test_adjoint_gate_has_an_independently_integrated_control_path():
    m=module(11990);U=m.gates()[1][1];result=m.propagate(U.conj().T)
    assert result['encoded_operator_max_error']<1e-8 and result['leakage_operator_norm']<1e-8


def test_new_peer_optical_compiler_realizes_the_actual_spinor_gates():
    m=module(11990)
    for (_,target),row in zip(m.gates(),fresh(11990)['gate_checks']):
        c=row['peer_TOE92_optical_compilation'];U=np.diag(np.exp(1j*np.array(c['first_operation_diagonal_phase_rad'])))
        for operation in c['subsequent_operations_in_state_application_order']:
            rails=operation['rails'];gate=np.array(operation['gate_real'])+1j*np.array(operation['gate_imag'])
            embedded=np.eye(4,dtype=complex);embedded[np.ix_(rails,rails)]=gate;U=embedded@U
        assert np.max(abs(U-target))<1e-10 and c['Givens_rotations']<=6


def test_native_four_cover_is_integral_primitive_and_face_closed():
    m=module(11991);d=fresh(11991);_,edges,B,F,_=m.native_geometry()
    V=s.Matrix(d['primitive_integer_edge_voltages']);assert F*V==s.zeros(99,4)
    C=s.Matrix(d['harmonic_voltages_Q']);assert B*C==s.zeros(27,4)
    assert C.T*C/27==s.Matrix(d['exact_acoustic_metric'])
    assert d['exact_harmonic_kernel_dimension']==26 and d['exact_full_group_fixed_dimension']==0
    assert d['raw_period_index']==81 and d['possible_H27_invariant_real_rank4_quotients']==6
    damaged=V.copy();damaged[0,0]+=1;assert F*damaged!=s.zeros(99,4)
    assert d['primitive_integer_edge_voltages']==saved(11991)['primitive_integer_edge_voltages']


def test_native_four_cover_cannot_keep_h27_and_a_lorentz_metric():
    d=fresh(11991);basis=d['invariant_metric_nullspace_in_character_coordinates'];assert len(basis)==2
    forms=[]
    for vector in basis:
        G=s.zeros(4)
        for value,(i,j) in zip(vector,itertools.combinations_with_replacement(range(4),2)):G[i,j]=G[j,i]=s.Rational(value)
        forms.append(G)
    for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
        eigen=np.linalg.eigvalsh(np.array(a*forms[0]+b*forms[1],float))
        assert sum(eigen>0) in (0,2,4) and min(abs(eigen))>.1


def test_parallel_logical_polarization_is_the_exact_lorentz_stabilizer():
    d=fresh(11991);repair=d['parallel_polarization_Lorentz_repair']
    eta=s.Matrix(repair['example_metric_in_primitive_deck_coordinates']);clock=s.Matrix(repair['clock_vector_primitive_coordinates'])
    assert (clock.T*eta*clock)[0]==-1
    eigen=np.linalg.eigvalsh(np.array(eta,float));assert sum(eigen<0)==1 and sum(eigen>0)==3
    preserved=[]
    for row in d['exact_deck_actions']:
        M=s.Matrix(row['matrix'])
        if M.T*eta*M==eta:preserved.append(row['h'])
    assert preserved==repair['selected_subgroup']==[[0,b,c] for b in range(3) for c in range(3)]
    assert repair['matches_TOE84_H1_and_TOE85_H2_polarization']


def test_native_four_period_overlap_has_dirac_scaling_and_gauge_covariance():
    d=fresh(11991);assert d['free_overlap_origin']['index']==0
    assert max(r['GW'] for r in d['Brillouin_corner_controls'])<1e-10
    assert min(r['smallest_D_singular'] for r in d['Brillouin_corner_controls'] if any(r['bits']))>1.7
    errors=[r['max_error'] for r in d['free_overlap_low_momentum']]
    assert errors[-1]<errors[0]/10 and d['gauge_covariance_max']<1e-10


def test_metric_curvature_implementation_against_de_sitter():
    m=module(11992);H=.7;t=1.2;a2=np.exp(2*H*t)
    g=np.diag([-1,a2,a2,a2]);dg=np.zeros((4,4,4));ddg=np.zeros((4,4,4,4))
    for j in (1,2,3):dg[0,j,j]=2*H*a2;ddg[0,0,j,j]=4*H*H*a2
    R,K=m.curvature(g,dg,ddg)
    assert np.max(abs(R-3*H*H*g))<1e-12 and abs(K-24*H**4)<1e-12


def test_nonlinear_einstein_metric_is_vacuum_but_not_flat():
    d=fresh(11992);assert d['exact_constraint_integrability_residual']=='0'
    assert d['local_physical_canonical_pairs']==2
    assert max(r['Ricci_max'] for r in d['metric_twojet_Ricci_checks'])<1e-12
    assert max(abs(r['Kretschmann']) for r in d['metric_twojet_Ricci_checks'])>.01
    assert max(d['remove_nonlinear_negative_control_Ricci_max'])>.1


def test_two_polarization_evolution_preserves_the_metric_constraint():
    d=fresh(11992);assert d['refinement_final_field_max']<3e-8
    assert max(r['metric_constraint_max'] for r in d['evolution64']['constraints'])<2e-11
    assert max(abs(r['momentum_mean']) for r in d['evolution64']['constraints'])<1e-12
    assert max(r['Ricci_max'] for r in d['evolution64']['Ricci_controls'])<1e-10
