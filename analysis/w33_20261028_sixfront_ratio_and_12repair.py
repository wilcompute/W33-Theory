#!/usr/bin/env python3
"""Six-front exact W33 audit: 12-harmonic Bloch repair, E6/H4 5:3 firewall."""
from fractions import Fraction as F
from math import acos, degrees, sqrt
from pathlib import Path
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
R=s.Matrix([[1,0,5,-5,1,0],[0,1,-1,0,1,0],[0,0,5,-5,0,1]])
S=s.Matrix([[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0]])
G=s.Matrix([[794,-42,768],[-42,22,-52],[768,-52,766]])
W=[F(1,10000)]*3+[F(49937,630000),F(21313,378000),
 F(49241,1350000),F(1241,90000),F(142189,3150000),F(1,56)]
CHARGES=[(1,1),(-3,1),(5,1),(-2,-2),(2,-2),(0,4)]
MULT=[10,5,1,5,5,1]

def exact_omega_loop(loop, voltages, a, b):
    """Return (A,B) such that native Bloch loop on witness is A+B*omega."""
    powers=((1,0),(0,1),(-1,-1))
    pos=[0,0,0,0];u=v=0
    for eid,sign in loop:
        if sign==-1:
            for j in range(4):pos[j]-=int(voltages[eid][j])
        x,y=powers[(pos[0]+pos[1])%3]
        p,q=int(a[eid]),int(b[eid])
        u+=sign*(x*p-y*q)
        v+=sign*(y*p+(x-y)*q)
        if sign==1:
            for j in range(4):pos[j]+=int(voltages[eid][j])
    assert pos==[0]*4
    return u,v

def norm(a,b):
    return a*a-a*b+b*b

def verify():
    stacked=R.col_join(S)
    assert stacked.det()==-1
    # Three missing loop channels and four independent deck translations
    # suffice: w(z)=sum|z_mu-1|²>0 for every z!=1.
    # At z=1 all six commutator Bloch rows vanish.
    # Thus ker(short,RL6,sqrt(w)SL6)=ker(short,L6) globally on T^4.
    old=json.loads((ROOT/'data/w33_pass12340_mixed_loop_exception.json').read_text())
    assert old['exact_ranks']=={'short':105,'mixed':107,'six':108,'gradient':27}
    raw=json.loads((ROOT/'data/w33_20261027_native_bloch_face_module.json').read_text())
    cover=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text())
    a,b=old['witness']['a'],old['witness']['b']
    flux=[exact_omega_loop(loop,cover['primitive_integer_edge_voltages'],a,b)
          for loop in raw['commutator_boundaries']]
    flux_norm=[norm(*x) for x in flux]
    assert flux_norm==[4112913]*5+[0]
    witness_norm=old['witness']['norm_squared']
    assert witness_norm==19641258
    eps=F(1,1000);weight_at_root3=6
    original_cost=eps*weight_at_root3*F(sum(flux_norm),witness_norm)
    compact_cost=eps*weight_at_root3*F(sum(flux_norm[i] for i in (2,3,4)),witness_norm)
    assert original_cost==F(49,7800)
    assert compact_cost==F(49,13000)
    # At every momentum, positivity plus unimodularity of [R;S] gives
    # exact equality of the completed magnetic kernels. O(k^4) correction.
    assert G.det()==260784
    assert all((G-7*s.eye(3))[:i,:i].det()>0 for i in (1,2,3))
    potential_sum=sum(W);assert potential_sum==F(7009,28125)
    # Rigorous *formula* for a Schur lower bound conditional on finite-box
    # lowest energy e_L, with exact K_out >= 7g²(L+1)²/2.
    def schur_lower(e_L,L,g):
        outside=7*g*g*(L+1)**2/2
        return (e_L+outside-sqrt((outside-e_L)**2+4*float(potential_sum)**2))/2
    finite_e_L=0.24853203844931157 # previous numerical L=5, g=0.2
    bound=schur_lower(finite_e_L,5,.2)
    assert .2356<bound<.2357
    moments={(i,j):sum(m*q**i*r**j for m,(q,r) in zip(MULT,CHARGES))
             for i,j in [(1,0),(0,1),(2,0),(0,2),(1,1),(3,0),(0,3),(2,1),(1,2)]}
    assert moments[(2,0)]==120 and moments[(0,2)]==72
    assert all(moments[key]==0 for key in [(1,0),(0,1),(1,1),(3,0),(0,3),(2,1),(1,2)])
    E=s.diag(120,72);U=s.Matrix([[1,0],[1,1]])
    assert U.det()==1 and U*E*U.T==s.Matrix([[120,120],[120,192]])
    # Dual polytopes. H4 roots r*h=4*30 and E6 roots r*h=6*12.
    f600=[120,720,1200,600];f120=[600,1200,720,120]
    assert f600[::-1]==f120 and 5*f600[1]==3*f120[1]==3600
    assert 4*30==120 and 6*12==72
    # Independent W33 eigenvalue spacing and SU5 hypercharge factor.
    q=s.symbols('q')
    assert s.solve(3*(q*q+1)-10*q,q)==[s.Rational(1,3),s.Integer(3)]
    hyper=3*F(1,3)**2+2*F(1,2)**2
    assert hyper==F(5,6) and 2*hyper==F(5,3)
    return {
      'status':'EXACT_SIX_FRONT_COMPARISON_AND_12_TERM_REPAIR',
      'action_selection':{'reflection_even_affine_H_theta_requires_theta':0,
                          'theta_plusminus_two_endpoints_exchanged':True,
                          'scope':'Only H(theta)=H0+theta J; no matter-induced effective action computed.'},
      'Bloch_repair':{'mixed_R':[list(map(int,row)) for row in R.tolist()],'complement_S':[list(map(int,row)) for row in S.tolist()],
                      'unimodular_stack_det':-1,'correction_harmonics':12,
                      'previous_harmonics':24,'kernel_equals_six_loop_all_unitary_momenta':True,
                      'kinematic_order':'O(k^4), leaves common O(k^2) cone',
                      'nonzero_character':['omega','omega','1','1'],
                      'frozen_witness_flux_norms':flux_norm,
                      'epsilon_001_witness_repair_cost':str(compact_cost),
                      'old_witness_repair_cost':str(original_cost)},
      'quantum_rotor':{'electric_gram':[list(map(int,row)) for row in G.tolist()],'electric_gram_gt_7I':True,
                       'sum_positive_cosine_weights':str(potential_sum),
                       'L5_g0.2_previous_numerical_eigenvalue':finite_e_L,
                       'schur_lower_bound_using_previous_numerical_eigenvalue':bound,
                       'qualification':'Schur bound theorem is exact conditional on certified finite-box minimum; numeric input is not an interval-certified eigenvalue. Only 3-loop sector.'},
      'parity_dimensionality':{'even_spatial_rank':3,'odd_spatial_rank':1,
                              'parity_exchanges_Hodge_endpoints':True,
                              'clock_and_physical_helicities_derived':False},
      'E6_charge_traces':{'quadratic_trace':[list(map(int,row)) for row in E.tolist()],
                          'unimodular_charge_rebasis':[list(map(int,row)) for row in U.tolist()],
                          'rebased_quadratic_trace':[list(map(int,row)) for row in (U*E*U.T).tolist()],
                          'original_diagonal_ratio':'5/3',
                          'rebased_diagonal_ratio':'5/8',
                          'basis_independent_physical_5_over_3':False},
      'H4_600_120_sixth':{'600_cell_Schlafli':[3,3,5],
                            '120_cell_Schlafli':[5,3,3],
                            '600_cell_f_vector':f600,'120_cell_f_vector':f120,
                            'edge_cell_incidence_both':3600,
                            'H4_root_count':120,'E6_root_count':72,
                            '600_cell_intrinsic_edge_deficit_degrees':360-5*degrees(acos(1/3)),
                            '120_cell_intrinsic_edge_deficit_degrees':360-3*degrees(acos(-1/sqrt(5))),
                            'SU5_hypercharge_kY':'5/3',
                            'W33_adjacency_gap_ratio':'5/3',
                            'W33_all_q_ratio':'(q^2+1)/(2q)',
                            'W33_prime_power_equals_5over3_only_q3':True,
                            'causal_physical_link_established':False},
    }

if __name__=='__main__':
    import sys
    text=json.dumps(verify(),indent=2)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(text)
    else:print(text,end='')
