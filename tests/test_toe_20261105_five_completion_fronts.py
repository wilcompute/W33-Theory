import importlib.util,pathlib,math,json
import numpy as np
import sympy as s
R=pathlib.Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,R/'analysis'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load('toe_20261105_five_fronts_model_completion')

def test_all_triangle_anomalies_of_concrete_protection_variant():
    for n in [2,13,20]:
        # Independent explicit Weyl inventory, including conjugate SM charges.
        fermions=[]
        for count,x in [(n,-1),(1,n)]:
            for _ in range(count):fermions.extend([(3,s.Rational(-1,3),x),(3,s.Rational(1,3),x)])
        fermions.extend([(1,0,1)]*(6*n)+[(1,0,-n)]*6)
        assert sum(dc*x for dc,Y,x in fermions)==0
        assert sum(dc*x**3 for dc,Y,x in fermions)==0
        assert sum(dc*Y**2*x for dc,Y,x in fermions)==0
        assert sum(dc*Y*x*x for dc,Y,x in fermions)==0
        assert sum(s.Rational(1,2)*x for dc,Y,x in fermions if dc==3)==0

def test_physical_axion_phase_and_metric():
    n=13;FS=3.;FT=4.
    gauge=np.array([2*FS,2*n*FT]);phase_grad=np.array([n/FS,-1/FT])
    assert abs(gauge@phase_grad)<1e-13
    assert math.gcd(n,1)==1 # primitive period, not n domain walls.
    assert math.isclose(1/np.linalg.norm(phase_grad),FS*FT/math.sqrt(n*n*FT*FT+FS*FS))

def test_quality_cost_not_unchanged_inventory():
    d=m.protected_variant();r=d['first_quality_row']
    assert r['n']==13 and r['leading_scalar_operator_dimension']==14
    assert r['colored_Dirac_pairs']==14 and r['singlet_Dirac_pairs']==42
    assert abs(r['third_inverse_coupling_mismatch_at_12'])>1

def test_complete_SU5_multiplets_cannot_fix_the_original_anomaly_combination():
    # Independent anomaly functional on original LH pair-charge sums.
    d,a,b,q=s.symbols('d a b q')
    A3=d/2+a+b;A2=3*(a+b)/2;AY=d/3+(a+b)/6
    C=s.expand(AY+A2-s.Rational(8,3)*A3)
    assert C==-d-a-b
    assert C.subs({d:-q,a:-q,b:q})==q
    for row in m.complete_SU5_protection_obstruction()['exact_trace_controls']:
        assert s.Rational(row['TrY2'])+s.Rational(row['SU2_index'])-s.Rational(8,3)*s.Rational(row['SU3_index'])==0

def test_yukawa_tensor_correction_and_single_multiplet_limit():
    d=m.tensor_yukawa_control()
    assert np.allclose(d['expected'],d['actual_real_scalar_tensor_beta'],rtol=1e-13)
    assert d['single_color_triplet_coefficient']==4
    assert d['common_y_cubic_coefficient_D15']==16

def test_portal_threshold_from_eliminating_radial_invariant():
    h,lH,lS,p=s.symbols('h lH lS p',positive=True);x=s.symbols('x',real=True)
    V=lH*h*h+lS*x*x+p*h*x
    xmin=s.solve(s.diff(V,x),x)[0]
    assert s.simplify(V.subs(x,xmin)-(lH-p*p/(4*lS))*h*h)==0

def test_threshold_events_have_canonical_mass_and_matching():
    row=m.running(1e11,.03,.02)
    events=row['threshold_events'];scalar=next(x for x in events if x['event']=='scalar')
    assert math.isclose(scalar['state_after'][6]**2/(4*scalar['state_after'][5]),.02)
    for e in events:
        if e['event']=='fermion':assert math.isclose(e['state_after'][7+e['species']]*1e11/math.sqrt(2),e['scale_GeV'])
    bad=m.running(1e11,.3,.02)
    assert not bad['reaches_MU'] and bad['threshold_events']==[]
    assert bad['termination']=='UNSUPPORTED_RADIAL_FERMION_ORDER_NEEDS_BROKEN_PHASE_MATCHING'

def test_warped_repair_does_not_preserve_flat_KK():
    for row in m.warped_gravity()['rows']:
        assert row['k_over_M5']<1e-4
        assert row['kL']>1e19
        assert row['required_brane_EH_mass_squared_if_flat_GeV2']<0
        assert math.isclose(row['k_GeV'],m.MU**3/(2*m.MP**2))

def test_actual_geometry_certificates():
    d=json.loads((R/'data/toe_20261105_global_measure_and_lorentz_branches.json').read_text())
    rows=d['toron_rows']
    assert all(x['kernel_gap_min']>1e-4 and x['frame_neighbor_min_singular']>1e-5 for x in rows)
    assert all(abs(x['first_Chern_sum']-round(x['first_Chern_sum']))<1e-8 for x in rows)
    assert math.isclose(abs(rows[0]['first_Chern_sum']),1.,abs_tol=1e-8)
    assert abs(rows[0]['first_Chern_sum']+rows[2]['first_Chern_sum'])<1e-8
    assert rows[-1]['whole_parameter_torus_gap_lower_bound']>.03
    r=d['Regge']
    assert r['flat_hinge_max_deficit']<1e-8
    assert r['raw_action_flat_FD_gradient_norm']<1e-5
    assert r['continuation_160_vs_320_action_error']<1e-8
    assert max(x['action_change']for x in r['flat_vertex_motion_controls'])<1e-8
    assert r['off_flat_max_deficit']>1e-4
    flat,curved=r['flat_and_offshell_Hessian_controls']
    assert sum(x<1e-5 for x in flat['Hessian_singular_values'])==4
    assert min(curved['Hessian_singular_values'])>1e-4
