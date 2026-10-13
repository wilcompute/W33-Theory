from pathlib import Path
import json
import sys
import numpy as np
import sympy as sp
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11965_11966_cp_transmission_soft_modulus as cp
import w33_pass11967_flavour_orientation_selector as flavour
import w33_pass11968_native_spin2_constraint_completion as gravity
import w33_pass11969_quantum_gauge_fermion as quantum
import w33_pass11969_full_native_gauss_compiler as native


def stored(name):
    return json.loads((ROOT/'data'/name).read_text())


def test_physical_weak_cp_obstruction_and_tree_strong_cp_are_distinct():
    r=stored('w33_pass11965_11966_cp_transmission_soft_modulus.json')['11965']['records']
    assert [sp.Rational(x['weak_basis_Im_trace_commutator_cubed']) for x in r]==[sp.Rational(1071,800000),-sp.Rational(1071,800000)]
    assert all(sp.Rational(x['tree_full_determinant'])==sp.Rational(7,5000) for x in r)
    assert r[0]['J_decoupling']*r[1]['J_decoupling']<0
    assert all(x['heavy_decoupling_checks'][-1]['error_vs_decoupling']<1e-7 for x in r)


def test_weak_basis_invariant_survives_second_basis():
    m=sp.Matrix([[1,1,0],[0,2,1],[1,0,3]])/10
    B=sp.Matrix([[1+sp.I,2-sp.I,1+2*sp.I]])/10
    Hd=m*(sp.eye(3)-B.conjugate().T*B/(sp.Rational(1,25)+(B*B.conjugate().T)[0]))*m.T
    Hu=sp.diag(1,4,9)
    U=sp.Matrix([[sp.Rational(3,5),sp.Rational(4,5),0],[-sp.Rational(4,5),sp.Rational(3,5),0],[0,0,sp.I]])
    A=U*Hu*U.conjugate().T;C=U*Hd*U.conjugate().T
    assert sp.simplify(sp.im(sp.trace((A*C-C*A)**3)))==sp.Rational(1071,800000)


def test_tiny_mass_is_positive_at_high_precision():
    d=stored('w33_pass11965_11966_cp_transmission_soft_modulus.json')['11966']
    assert .58<d['canonical_light_mass_GeV_if_Lambda_1e16']<.59
    assert d['precision_recheck_relative_error']<1e-45
    assert all(float(x)>0 for x in d['constraint_J_singular_values'])


def test_positive_soft_mass_can_erase_selected_minimum():
    assert cp.radial_minima(.1)[0]['x']>.99
    assert cp.radial_minima(4.)==[]
    # Independent leading-limit coexistence/spinodal equations.
    y=sp.Rational(10,11);x=y**sp.Rational(1,12)
    k2=12*x**10*(1-y)
    assert sp.simplify((y-1)**2+k2*x*x-1)==0
    y=sp.Rational(5,11)
    assert 10*(1-y)-12*y==0


def test_extra_abelian_charge_cannot_add_a_direction_on_existing_fields():
    d=stored('w33_pass11965_11966_cp_transmission_soft_modulus.json')['11966']['no_new_Abelian_D_direction']
    assert d['charge_constraint_rank']==5 and d['charge_kernel_dimension']==2
    assert sp.Matrix.hstack(sp.Matrix(d['basis_X']),sp.Matrix(d['basis_Z'])).rank()==2


def test_orientation_potential_is_checked_against_actual_variation():
    d=flavour.orientation_control()
    assert abs(d['mixed_potential_variation_analytic']-d['finite_difference_variation'])<1e-8
    assert d['alignment_global_minimum']<d['random_mixed_potential']<d['opposite_extremum']


def test_counterterm_prevents_unqualified_branch_selection():
    d=stored('w33_pass11967_flavour_orientation_selector.json')['lepton_branches']
    assert len(d['branches'])==5
    assert d['rankings'][0]['ordering']!=d['rankings'][1]['ordering']
    for c in d['counterterm_crossings']:
        a=d['branches'][c['branch_i']];b=d['branches'][c['branch_j']]
        delta=a['Majorana_CW_eV_fourth']-b['Majorana_CW_eV_fourth']
        delta+=c['allowed_counterterm_crossing']*(a['quartic_invariant_eV_fourth']-b['quartic_invariant_eV_fourth'])
        assert abs(delta)<1e-20


def test_majorana_invariant_supplies_a_distinct_orientation_mechanism():
    d=flavour.majorana_orientation_positive_control()
    assert sp.Rational(d['invariant_at_minimum'])==sp.Rational(8,81)
    assert sp.Rational(d['invariant_at_diagonal_orientation'])==sp.Rational(17,81)
    assert 'does not predict an observable mixing angle' in d['boundary']


def test_gravity_obstruction_has_exact_rational_witness():
    d=stored('w33_pass11968_native_spin2_constraint_completion.json')
    assert sp.Rational(d['exact_poisson_witness']['bracket'])==sp.Rational(8667,4096000)
    assert d['completed_constraint_bracket_max']<1e-12
    assert d['physical_configuration']==168
    assert d['offsite_projector_norm_fraction']>0


def test_projection_completion_works_for_independent_noncommuting_derivatives():
    rng=np.random.default_rng(4)
    D=[]
    for _ in range(3):
        A=rng.normal(size=(5,5));D.append(A-A.T)
    H,M=gravity.constraints(D);PM,_=gravity.row_projector(M)
    HC=H@(np.eye(30)-PM)
    assert np.linalg.norm(H@M.T)>1
    assert np.max(abs(HC@M.T))<1e-10
    # Orthogonal rotation of the derivative labels preserves the total
    # commutator norm; failure is not removed by a second axis drawing.
    R=np.array([[.6,.8,0],[-.8,.6,0],[0,0,1]])
    rotated=[sum(R[i,j]*D[j] for j in range(3)) for i in range(3)]
    energy=lambda ds:sum(np.linalg.norm(ds[i]@ds[j]-ds[j]@ds[i])**2 for i,j in ((0,1),(0,2),(1,2)))
    assert abs(energy(D)-energy(rotated))<1e-10


def test_coupled_quantum_basis_solves_gauss_with_static_charges():
    charge=np.array([1,0,0,-1,0,0])
    _,flux,occ=quantum.physical_basis(6,2,charge)
    assert np.array_equal(np.roll(flux,1,axis=1)-flux+occ-np.arange(6)%2+charge,np.zeros_like(flux))


def test_actual_jordan_wigner_operator_fixes_hopping_signs():
    N=4;ann=[]
    for a in range(N):
        C=np.zeros((2**N,2**N))
        for bits in range(2**N):
            if bits&(1<<a):C[bits^(1<<a),bits]=(-1)**sum((bits>>j)&1 for j in range(a))
        ann.append(C)
    H,basis,_,_,transitions=quantum.matrix(N,2,electric=0,mass=0,magnetic=0,hopping=.7)
    for i,j,a,direction in transitions:
        b=(a+1)%N
        fock=-.7*(ann[b].T@ann[a]+ann[a].T@ann[b])
        assert H[i,j]==fock[basis[j][0],basis[i][0]]


def test_native_fermion_rotor_cutoff_converges():
    d=stored('w33_pass11969_quantum_gauge_fermion.json')['native']
    rows=d['flux_cutoff_sweep']
    assert d['native_Gauss_max_residual']==0
    assert d['full_fermion_pattern_count']==70
    assert abs(rows[-1]['gap']-rows[-2]['gap'])<1e-7
    assert rows[-1]['dimension']==630


def test_mass_matching_has_exact_energy_and_hopping_control():
    d=quantum.shifted_mass_symmetry()
    assert d['exact_energy_difference']=='0'
    assert d['projected_kinetic_intertwiner_bulk_residual']<1e-12
    assert 'distinct theta theories' in d['theta_interpretation']


def test_matching_improves_known_continuum_gap_without_fitting_it():
    d=stored('w33_pass11969_quantum_gauge_fermion.json')
    old=d['one_dimensional_refinement']['samples'][-1]['cutoff_sweep'][-1]['gap']
    matched=d['mass_matched_refinement'];new=matched['samples'][3]['gap'];target=matched['benchmark']
    assert abs(new/target-1)<.004
    assert abs(old/target-1)>.2
    assert matched['samples'][-1]['sites']==12


def test_charge_extraction_retains_a_held_out_distance():
    d=stored('w33_pass11969_quantum_gauge_fermion.json')['matched_static_screening']
    assert [x['sites'] for x in d['samples']]==[8,10,12]
    assert all(x['held_out_separation']==4. for x in d['samples'])
    assert all(abs(x['extracted_screening_charge']-.7)<.04 for x in d['samples'])
    assert all(x['held_out_error']<.02 for x in d['samples'])


@pytest.fixture(scope='module')
def native_compiler():return native.NativeGaussCompiler()


def test_full_native_integer_coordinate_map_is_bijective(native_compiler):
    c=native_compiler
    bits=sum(1<<i for i in range(40));l=tuple(i%5-2 for i in range(81))
    n=c.flux((bits,l))
    assert np.array_equal(n[c.chords],l)
    assert np.array_equal(c.B.T@n+c.occupation(bits)-c.background,np.zeros(80))
    assert len(c.chords)==160-80+1


def test_full_native_action_has_hermitian_reverse_moves(native_compiler):
    c=native_compiler;state=(sum(1<<i for i in range(40)),tuple([0]*81))
    action=c.apply_H(state)
    edge=next(e for e in range(160) if c.hop(state,e) is not None)
    target,_,direction=c.hop(state,edge)
    assert action[target]==c.apply_H(target)[state]
    delta=c.flux(target)-c.flux(state)
    assert np.count_nonzero(delta)==1 and delta[edge]==-direction


def test_full_native_plaquette_map_preserves_all_gauss_generators(native_compiler):
    c=native_compiler;state=(sum(1<<i for i in range(40)),tuple([0]*81))
    n=c.flux(state)
    for row in (0,250,1000,1384):
        shifted=c.plaquette(state,row)
        assert np.array_equal(c.flux(shifted)-n,c.P[row])
        assert c.plaquette(shifted,row,-1)==state
