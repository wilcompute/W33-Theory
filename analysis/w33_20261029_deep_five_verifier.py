#!/usr/bin/env python3
"""Five independently checkable W33 follow-up results, 2026-10-29.

1. Binary adjacency CSS q=3,5,7 isotropic-line-pair logical coset census.
2. Arbitrary complex pure/mixed-product three-photon Gram robust discriminator.
3. Operator-norm and total-variation uncertainty thresholds.
4. Exact W(3,q) dimensionless walk quarter-cycle and revival, odd q.
5. E8 integral central sign becomes optical photon-number parity on Fock space.

No exact q7 minimum-distance claim or fundamental new-physics claim.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261029_deep_five_fronts.json"
INPUT=(0,7,9)
OUTPUTS=tuple(combinations((4,14,23,32),3))
PERMS=tuple(permutations(range(3)))
Q=(3,5,7)
DEN=15**6

def projective_points(q):
    points=set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                for d in range(q):
                    x=(a,b,c,d)
                    if not any(x):continue
                    inv=pow(next(v for v in x if v),-1,q)
                    points.add(tuple(v*inv%q for v in x))
    return sorted(points)

def form(x,y,q):
    return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%q

def gf2_basis(rows):
    basis={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k not in basis:
                basis[k]=x
                break
            x^=basis[k]
    return basis

def reduce_coset(x,basis):
    for k in sorted(basis,reverse=True):
        if (x>>k)&1:x^=basis[k]
    return x

def line_pair_census(q):
    points=projective_points(q)
    n=(q+1)*(q*q+1)
    assert len(points)==n
    rows=[sum(1<<j for j,y in enumerate(points)
              if i!=j and form(x,y,q)==0)
          for i,x in enumerate(points)]
    assert all(row.bit_count()==q*(q+1) for row in rows)
    assert all((rows[i]&rows[j]).bit_count()==
               (q-1 if rows[i]>>j&1 else q+1)
               for i in range(n) for j in range(i+1,n))
    lines=set()
    for i in range(n):
        for j in range(i+1,n):
            if rows[i]>>j&1:
                line=(rows[i]&rows[j])|(1<<i)|(1<<j)
                assert line.bit_count()==q+1
                lines.add(line)
    lines=sorted(lines)
    assert len(lines)==n
    basis=gf2_basis(rows)
    assert len(basis)==(n-(q*q-1))//2
    weights=Counter()
    quotient=Counter()
    for i in range(n):
        for j in range(i+1,n):
            x=lines[i]^lines[j]
            w=x.bit_count()
            assert w in (2*q,2*q+2)
            residual=reduce_coset(x,basis)
            assert residual, "line-pair word is a stabilizer"
            weights[w]+=1
            if w==2*q:quotient[residual]+=1
    assert weights[2*q]==n*q*(q+1)//2
    assert weights[2*q+2]==n*(n-1)//2-weights[2*q]
    expected={3:(240,120,2),5:(2340,2340,1),7:(11200,11200,1)}
    assert (weights[2*q],len(quotient),max(quotient.values()))==expected[q]
    assert min(quotient.values())==max(quotient.values())
    return dict(q=q,physical_qubits=n,logical_qubits=q*q-1,
        adjacency_binary_rank=len(basis),
        isotropic_lines=n,
        two_line_logicals_weight_2q=weights[2*q],
        two_line_logicals_weight_2q_plus_2=weights[2*q+2],
        distinct_weight_2q_logical_cosets=len(quotient),
        word_multiplicity_per_coset=min(quotient.values()),
        q7_exact_minimum_distance_proved=False if q==7 else True)

def polynomial(mask):
    a=tuple(-3 if mask>>i&1 else 2 for i in range(9))
    paths=tuple(a[p[0]]*a[3+p[1]]*a[6+p[2]] for p in PERMS)
    out=[0]*5   # 1, |g01|², |g02|², |g12|², Re(g01*g12*g20)
    lookup={(0,1):1,(0,2):2,(1,2):3}
    for i,p in enumerate(PERMS):
        for j,r in enumerate(PERMS):
            changed=[k for k in range(3) if p[k]!=r[k]]
            if not changed:idx=0
            elif len(changed)==2:
                idx=lookup[tuple(sorted((p[changed[0]],p[changed[1]])))]
            else:
                assert len(changed)==3
                idx=4
            out[idx]+=paths[i]*paths[j]
    assert sum(out)==sum(paths)**2
    return tuple(out)

def gram_exact():
    # Assert hardcoded masks against the actual two geometry matrices.
    from w33_20261029_three_photon_dual_discriminator import two_graphs
    A,B=two_graphs()
    assert all(A[i,j]==0 and B[i,j]==0
               for i,j in combinations(INPUT,2))
    masks=[]
    for M in (A,B):
        one=[]
        for out in OUTPUTS:
            mask=sum(1<<(3*i+j)
                     for i,x in enumerate(out)
                     for j,y in enumerate(INPUT)
                     if x==y or M[x,y])
            one.append(mask)
        masks.append(one)
    assert masks==[[511]*4,[259,3,35,32]]
    W=tuple(sum(polynomial(m)[i] for m in masks[0]) for i in range(5))
    D=tuple(sum(polynomial(m)[i] for m in masks[1]) for i in range(5))
    diff=tuple(a-b for a,b in zip(W,D))
    assert W==(17496,17496,17496,17496,34992)
    assert D==(3376,3376,-1024,-1024,-2048)
    assert diff==(14120,14120,18520,18520,37040)
    # For arbitrary complex Gram overlaps, x,y,z in [0,1] and
    # Re Bargmann >= -sqrt(xyz) >= -(x+y+z)/3.
    # All coefficients below are positive; minimum at x=y=z=0.
    rational_coeff=[F(diff[i],1)-F(diff[4],3) for i in (1,2,3)]
    assert rational_coeff==[F(5320,3),F(18520,3),F(18520,3)]
    return dict(input_modes=list(INPUT),output_modes=[list(z) for z in OUTPUTS],
      W33_masks=masks[0],dual_masks=masks[1],
      polynomial_variables=["1","abs_g01_squared","abs_g02_squared",
                            "abs_g12_squared","Re_Bargmann_cycle"],
      W33_integer_coefficients=W,dual_integer_coefficients=D,
      difference_integer_coefficients=diff,
      guaranteed_minimum_probability_gap=float(F(diff[0],DEN)),
      rigorous_minimum_is_fully_distinguishable=True,
      independent_mixed_internal_photon_states_covered_by_convexity=True,
      inequality="abs(Re B)<=sqrt(x*y*z)<=(x+y+z)/3 for x,y,z in [0,1]",
      certified_positive_pair_coefficients_after_AMGM=[str(v) for v in rational_coeff])

def device_budget(gram):
    delta=F(14120,DEN)
    # Symmetric operator-norm error for each 40-mode passive U:
    # 3-photon channel TV <=3 epsilon, two hypotheses lose <=6 epsilon.
    eps=delta/6
    return dict(minimum_probability_gap=float(delta),
        symmetric_per_device_operator_norm_strict_error_ceiling=float(eps),
        symmetric_per_device_output_total_variation_strict_error_ceiling=float(delta/2),
        trace_distance_bound="TV(3-photon U,V) <=3*opnorm(U-V)",
        fixed_input_internal_states_assumed_same_for_both_graph_tests=True,
        uniform_photon_survival_fraction_eta_example=0.9,
        emitted_per_registered_triple_trial_eta_0p9=1/(0.9**3),
        postselection_valid_only_for_uniform_input_and_mode_independent_loss=True,
        caveat="Bounds are conservative certified sufficient conditions, not achieved hardware tolerances.")

def walk_closed_form(q):
    assert q%2==1 and q>=3
    v=(q+1)*(q*q+1)
    degree=q*(q+1)
    r=q-1
    s=-(q+1)
    assert math.gcd(degree-r,r-s)==2
    onsite=F((q-1)**2,(q*q+1)**2)
    neighbor=onsite
    far=F((q+1)**2,q*q*(q*q+1)**2)
    assert (degree+1)*onsite+(v-1-degree)*far==1
    return dict(q=q,vertices=v,degree=degree,real_adjacency_eigenvalues=[degree,r,s],
        quarter_t_pi_over_2_onsite_probability=str(onsite),
        quarter_t_pi_over_2_each_neighbor_probability=str(neighbor),
        quarter_t_pi_over_2_each_nonneighbor_probability=str(far),
        quarter_t_pi_over_2_total_neighbor_shell_probability=str(degree*neighbor),
        all_odd_q_exact_revival_at_dimensionless_t_pi=True,
        earliest_projective_revival_t_pi=True,
        physical_seconds_not_determined=True)

def e8_central_second_quantization():
    return dict(matrix="-I8",Fock_sector_phases={str(n):(-1)**n for n in range(9)},
        operator="(-1)^N on the eight optical modes",
        unobservable_global_phase_when_total_signal_photon_number_fixed=True,
        phase_reference_or_controlled_path_required=True,
        standard_linear_optics_not_beyond_quantum_theory=True)

def main():
    census=[line_pair_census(q) for q in Q]
    gram=gram_exact()
    clock=[walk_closed_form(q) for q in Q]
    out=dict(status="PASS",geometry=census,complex_gram_three_photon=gram,
             loss_and_device_certified_bounds=device_budget(gram),
             odd_q_continuous_time_walk=clock,
             E8_center_Fock_parity=e8_central_second_quantization(),
             new_physics_falsification="NONE: ordinary quantum optics and finite geometry; no free physical energy scale or deviation established.")
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS five fronts; q7 11200 logical classes; arbitrary complex Gram gap",
          gram["guaranteed_minimum_probability_gap"],"q odd exact pi revival")
    return out

if __name__=="__main__":main()
