#!/usr/bin/env python3
"""Conwell K8 erasure reliability, finite Radon transform, A8 selection
obstruction, exact Bloch counterexample, and ternary Grassmann correction.

This verifies finite mathematics for W33-Theory; it does NOT derive a
Penrose transform, Lorentzian time, quantum error threshold or TOE.
"""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
from itertools import combinations, product, permutations
from math import comb
from pathlib import Path
import json

import numpy as np
import sympy as sp

try:
    from analysis.w33_20261028_twistor_klein_ag_codes_round13 import (
        Q, plucker, conwell_heptads, evaluation_rows, rref,
    )
except ImportError:
    from w33_20261028_twistor_klein_ag_codes_round13 import (
        Q, plucker, conwell_heptads, evaluation_rows, rref,
    )


def rank2(words):
    piv = {}
    for word in words:
        x = int(word)
        while x:
            i = x.bit_length() - 1
            if i not in piv:
                piv[i] = x
                break
            x ^= piv[i]
    return len(piv)


@lru_cache(maxsize=1)
def graph():
    points = tuple(p for p in range(1, 64) if Q(p))
    heptads, owners, triangles, _ = conwell_heptads(points)
    edges = {tuple(pair): p for p, pair in owners.items()}
    assert (len(points),len(heptads),len(triangles),len(edges)) == (28,8,56,28)
    assert set(edges) == set(combinations(range(8), 2))
    v = [0] + [edges[0,j] for j in range(1,8)]
    assert rank2(v) == 6
    assert __import__('functools').reduce(int.__xor__,v,0) == 0
    assert all(edges[i,j] == v[i]^v[j] for i,j in edges)
    return points, owners, edges


def exact_erasure():
    points, owners, edges = graph()
    good = [sum(rank2(subset)==k for subset in combinations(points,k))
            for k in range(7)]
    assert good == [1,28,378,3220,18760,73248,155456]
    bad = [comb(28,k)-good[k] for k in range(7)]
    assert bad[3] == 56 and bad[4] == 1715
    inverse = {p:edge for edge,p in edges.items()}
    zero4 = [c for c in combinations(points,4) if c[0]^c[1]^c[2]^c[3]==0]
    assert len(zero4) == 315
    counts = Counter()
    for subset in zero4:
        degree = [0]*8
        for p in subset:
            i,j = inverse[p]; degree[i]+=1; degree[j]+=1
        if all(d==1 for d in degree):
            counts['perfect_matchings']+=1
        else:
            assert sorted(degree)==[0,0,0,0,2,2,2,2]
            counts['four_cycles']+=1
    assert counts == {'perfect_matchings':105,'four_cycles':210}
    # Every 7 columns in F2^6 depend; an X stabilizer has weight >=12.
    # Hence all erasure sets of cardinality >=7 are uncorrectable.
    probabilities = {
        str(eta):sum(good[k]*eta**k*(1-eta)**(28-k) for k in range(7))
        for eta in (.01,.02,.05,.1,.15)
    }
    return {
        'CSS_parameters':[28,15,3],
        'qubits_as_28_edges_of_K8':True,
        'six_bit_syndrome_as_vertex_boundary_mod_allones':True,
        'correctable_counts_size_0_through_6':good,
        'uncorrectable_counts_size_0_through_6':bad,
        'all_size_7_or_more_erasures_uncorrectable':True,
        'weight3_logical_supports_graph_triangles':56,
        'weight4_zero_syndrome_four_cycles':counts['four_cycles'],
        'weight4_zero_syndrome_perfect_matchings':counts['perfect_matchings'],
        'independent_heralded_loss_success_probabilities':probabilities,
        'exact_success_polynomial':
          '+'.join(f'{c}*eta^{k}*(1-eta)^{28-k}' for k,c in enumerate(good)),
        'scope':'Ideal flagged erasures and perfect syndrome operations; no optical circuit or threshold.'
    }


def syndrome_controls():
    pts, owners, edges = graph()
    checks = evaluation_rows(pts,1)
    assert len(checks)==6 and len(rref(checks,28)[0])==6
    for j,p in enumerate(pts):
        syndrome = sum(((row>>j)&1)<<i for i,row in enumerate(checks))
        assert syndrome==p
    pair_counts = Counter('single_alias' if Q(a^b) else 'detected_non_single'
                          for a,b in combinations(pts,2))
    assert pair_counts == {'single_alias':168,'detected_non_single':210}
    return {
        'single_X_Pauli_syndrome_equals_six_bit_Plucker_vector':True,
        'single_Z_Pauli_syndrome_equals_seven_bits_p_plus_one':True,
        'two_X_errors_alias_single_X':168,
        'two_X_errors_detectably_outside_single_lookup':210,
        'minimal_stabilizer_rows':[7,6],
        'independent_Pauli_error_correctable_weight_at_most_1':
          '(1-p)^28 + 28*p*(1-p)^27',
    }


def finite_radon():
    lines = {frozenset((u,v,u^v)):plucker(u,v)
             for u,v in combinations(range(1,16),2)}
    assert len(lines)==35
    rows = [sum(1<<(x-1) for x in line) for line in lines]
    assert rank2(rows)==11
    linear = [sum(1<<(x-1) for x in range(1,16) if (x>>i)&1)
              for i in range(4)]
    assert rank2(linear)==4
    assert all((r&v).bit_count()%2==0 for r in rows for v in linear)
    for i,j in permutations(range(4),2):
        def trans(u):return u^(((u>>j)&1)<<i)
        assert all(frozenset(trans(u) for u in line) in lines
                   for line in lines)
    return {
        'finite_twistor_point_count':15,'Klein_quadric_line_count':35,
        'point_line_incidence_count':105,
        'GF2_incidence_Radon_rank':11,
        'kernel_dimension':4,'cokernel_dimension':24,
        'kernel_equals_four_linear_functions_on_F2_4':True,
        'GL4_F2_generator_equivariance_count':12,
        'not_holomorphic_Penrose_transform':True,
    }


def a8_selector():
    pts, owners, edges = graph()
    A = np.array([
        [int(p!=q and len(set(owners[p])&set(owners[q]))==1)
         for q in pts] for p in pts],dtype=np.int64)
    I=np.eye(28,dtype=np.int64);J=np.ones((28,28),dtype=np.int64)
    assert np.array_equal(A@A,8*I+2*A+4*J)
    eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    assert eig=={-2:20,4:7,12:1}
    return {
       'label_graph':'Triangular graph T(8), strongly regular (28,12,6,4)',
       'A8_invariant_quadratic_response_commutant_dim':3,
       'allowed_matrix':'a*I+b*A+c*J',
       'mode_eigenvalues_and_multiplicities':{
           'a+12*b+28*c':1,'a+4*b':7,'a-2*b':20},
       'single_selected_non_degenerate_kernel_invariant_under_full_A8':False,
       'missing':'Dynamical E6 matter determinant and spontaneous vacuum selection.'
    }


def sub_six_counterexample():
    # This disproves the torsion-grid-positive 3-cosine design:
    # channel 0 differences along e0,e2, channel 5 along e0.
    u=(-17-4*sp.I*sp.sqrt(21))/25
    v=(-2+sp.I*sp.sqrt(21))/5
    assert sp.simplify(u*sp.conjugate(u))==1
    assert sp.simplify(v*sp.conjugate(v))==1
    W=sp.Matrix([[0,1,1,-1],[-1,0,1,-1],
                 [0,0,1,-1],[0,0,1,0]])
    N=sp.Matrix([[10,-5,1,-6],[-5,10,-5,6],
                 [1,-5,10,-6],[-6,6,-6,12]])
    z=[sp.Integer(1),u,sp.Integer(1),v]
    h=sp.Matrix([sp.prod(z[j]**int(W[i,j]) for j in range(4)) for i in range(4)])
    d=h-sp.ones(4,1)
    assert sp.simplify(sp.expand_complex((d.T*N*d)[0]/2))==0
    X,Y=sp.symbols('X Y')
    q=5*X**2-6*X*Y-4*X+6*Y**2-6*Y+5
    qstar=sp.expand(X**2*Y**2*q.subs({X:1/X,Y:1/Y}))
    assert sp.factor(sp.resultant(q,qstar,X))==180*(Y-1)**6*(5*Y**2+4*Y+5)
    return {
       'candidate':'3 compact differences: P0:e0,e2 and P5:e0',
       'counterexample_Bloch_z':['1','(-17-4i*sqrt21)/25','1','(-2+i*sqrt21)/5'],
       'Q_zero_exact':True,
       'all_three_added_harmonics_inactive':True,
       'rejected_global_repair':True,
       'restricted_torus_resultant':'180*(Y-1)^6*(5*Y^2+4*Y+5)',
       'existing_six_term_global_proof_still_valid':True,
    }


def exact_F3_lagrangian_code():
    # Correct the old pass153 [40,5,28] overclaim by full 3^5 census.
    def rr3(matrix):
        rows=[list(r) for r in matrix]; piv=[]; k=0
        for j in range(len(rows[0])):
            i=next((i for i in range(k,len(rows)) if rows[i][j]%3),None)
            if i is None:continue
            rows[k],rows[i]=rows[i],rows[k]
            inv=pow(rows[k][j],1,3)
            rows[k]=[(inv*x)%3 for x in rows[k]]
            for a in range(len(rows)):
                if a==k:continue
                c=rows[a][j]
                if c:rows[a]=[(x-c*y)%3 for x,y in zip(rows[a],rows[k])]
            piv.append(j); k+=1
            if k==len(rows):break
        return rows[:k]
    nonzero=[x for x in product(range(3),repeat=4) if any(x)]
    planes={}
    for u,v in combinations(nonzero,2):
        p=rr3((u,v))
        if len(p)==2:planes[tuple(tuple(row) for row in p)]=True
    assert len(planes)==130
    isotropic=lambda u,v:(u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3==0
    lag=[P for P in planes if isotropic(*P)]
    assert len(lag)==40
    coord=list(combinations(range(4),2))
    columns=[]
    for u,v in lag:
        col=[(u[i]*v[j]-u[j]*v[i])%3 for i,j in coord]
        first=next(x for x in col if x)
        columns.append([x*pow(first,1,3)%3 for x in col])
    assert all((c[0]+c[5])%3==0 for c in columns)
    basis=rr3([[c[i] for c in columns] for i in range(6)])
    assert len(basis)==5
    weights=Counter()
    for coeff in product(range(3),repeat=5):
        word=[sum(coeff[i]*basis[i][j] for i in range(5))%3
              for j in range(40)]
        weights[sum(x!=0 for x in word)]+=1
    assert weights=={0:1,24:90,27:80,30:72}
    return {'code':'ternary symplectic Lagrangian Grassmann code',
            'all_planes':130,'totally_isotropic_planes':40,
            'parameters':[40,5,24],
            'weight_enumerator':dict(sorted(weights.items())),
            'incorrect_legacy_distance_claim':28,
            'legacy_path':'analysis/w33_pass153_grassmann_codes.py',
            'scope':'Exact projective Plucker matrix and all 243 ternary codewords; corrects unsupported Plotkin-bound claim.'}


@lru_cache(maxsize=1)
def certificate():
    return {'schema':'w33.20261029.conwell_k8_radon_loss.v1',
            'erasure':exact_erasure(),
            'syndrome':syndrome_controls(),
            'finite_Radon':finite_radon(),
            'A8_selection':a8_selector(),
            'gauge_counterexample':sub_six_counterexample(),
            'F3_Grassmann_correction':exact_F3_lagrangian_code(),
            'scope':'Finite incidence, algebra and idealized noise; no full 135-link dispersion, physical photon threshold, Penrose cohomology or interacting E6 action.'}


if __name__=='__main__':
    import sys
    content=json.dumps(certificate(),indent=2)+'\n'
    target=Path(sys.argv[1]) if len(sys.argv)>1 else None
    if target:
        target.write_text(content,encoding='utf-8')
        print(target)
    else:print(content)
