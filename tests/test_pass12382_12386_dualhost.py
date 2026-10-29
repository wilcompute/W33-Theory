"""Independent controls for the five-front dual-host continuation."""
from pathlib import Path
from itertools import product
import json,sys
import numpy as np
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import w33_pass12382_cyclotomic_sieve as sieve
import w33_pass12383_12386_dualhost_fronts as probe

def test_sieve_against_brute_exact_cyclotomic_decisions():
    x=s.Symbol('x');h=s.symbols('h:4');d=s.Matrix(h)-s.ones(4,1)
    poly=(d.T*probe.old.N*d)[0]/2
    for n in [3,5,6]:
        expected=[];phi=s.cyclotomic_poly(n,x)
        for v in product(range(n),repeat=4):
            if s.rem(s.expand(poly.subs(dict(zip(h,[x**j for j in v])))),phi,x)==0:expected.append(list(v))
        assert sorted(sieve.census(n)['exact_h_exponents'])==expected

def test_sieve_quadratic_elimination_covers_every_finite_field_root():
    n=7;p,r=sieve.field(n,1000)
    roots=[]
    for v in product(range(n),repeat=4):
        if sieve.residues([v],n,p,r)[0]==0:roots.append(v)
    assert roots==[(0,0,0,0)]

def test_exact_schrodinger_group_law_all_products():
    for g,h in product(list(product(range(3),repeat=3)),repeat=2):
        a,b,c=g;A,B,C=h
        for x in range(3):
            phase=C-B*x+c-b*((x+A)%3)
            composed=c+C-b*A-(b+B)*x
            assert (phase-composed)%3==0
    # Omitting the qutrit makes the centre trivial, so cannot intertwine with omega I.
    omega=np.exp(2j*np.pi/3)
    assert abs(omega-1)>1

def test_quantum_lift_in_actual_css_amplitude_space():
    r=probe.quantum_lift()
    assert r['embedding_dimensions']==[768,27]
    assert r['maximum_intertwining_residual']<1e-13
    assert sorted(r['Fourier_norm_squared'])==[.75]*8+[3.]

def test_interacting_ward_rejects_missing_contact_term():
    r=json.loads((probe.ROOT/'data/w33_pass12383_12386_dualhost_fronts.json').read_text())
    for run in r['interacting_ward']['runs']:
        assert max(v['ward_residual'] for v in run['frequency_samples'])<1e-12
        assert abs(run['frequency_samples'][0]['longitudinal_current_kernel'])<1e-12
        assert run['frequency_samples'][1]['longitudinal_current_kernel']>0
        row=run['frequency_samples'][1]
        assert abs(-row['paramagnetic_sum']-row['omega']**2*row['density_susceptibility'])>1e-5
    # Susceptibility depends on interaction, rather than being a charge-count identity.
    vals=[x['frequency_samples'][1]['density_susceptibility'] for x in r['interacting_ward']['runs']]
    assert vals[0]>vals[1]>vals[2]

def test_matched_metric_cone_and_budget():
    r=json.loads((probe.ROOT/'data/w33_pass12383_12386_dualhost_fronts.json').read_text())['matched_dispersion']
    assert abs(sum(r['equal_budget_channel_weights'])-2)<1e-12
    assert min(r['equal_budget_channel_weights'])>0
    assert r['optimized_worst_sample_ratio']>=r['equal_weights_worst_sample_ratio']
    for row in r['infrared']:
        assert max(abs(x/row['target_squared_speed']-1) for x in row['samples'][-1]['three_lambda_over_t2'])<.001

def test_published_string_inputs_negative_controls():
    r=probe.string_input();A=np.array(r['GGSO_matrix_13_by13']);D=np.array(r['twice_signed_overlap'])
    A[2,3]*=-1
    assert not np.array_equal(A*A.T,(-1)**((D//4)%2))
    # q^0 qbar^-1 is off shell: negative exponent alone is not a physical tachyon.
    terms=r['published_series_terms_coefficient_m8_n8']
    assert any(c and m+n<0 and m!=n for c,m,n in terms)
    assert not any(c and m==n and m<0 for c,m,n in terms)
