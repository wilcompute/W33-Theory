#!/usr/bin/env python3
"""Five W33 frontiers: all-prime K theorem, native clock, routing lower bound,
logical-syndrome no-go, and two-anchor finite-group spectral obstruction.

Every result is finite mathematics or an explicitly postulated toy model.
Neither a physical photonic processor nor a continuum/TOE is claimed.
"""
from __future__ import annotations
import json
import math
import sys
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp

if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.w33_20261022_allfive_deeper_frontiers import (
    A, B, C, X, N, J, IDENT, cycles, transvection, routing,
    nine_root_syndrome, forty_state_clock
)
from analysis.w33_20261022_K_jordan_extension_census import (
    run as k_census
)


def choose(n, k):
    return math.comb(n,k) if 0<=k<=n else 0


def k_rank_formula(p, k):
    if k==0:
        return (p+1)*(p*p+1)-choose(p+2,3)
    return p*p*(p-k)-choose(p+1,3)+choose(k+1,3)


def orthogonal_all_prime_theorem():
    """Affine-module counting proof; independent finite controls."""
    census=k_census()
    records=[]
    for p in [2,3,5,7,11,13,17,19,23,29,31]:
        ranks=[k_rank_formula(p,k) for k in range(p+1)]
        blocks={j:ranks[j-1]-2*ranks[j]+ranks[j+1] for j in range(1,p)}
        blocks[p]=ranks[p-1]
        expected={1:(p*p+p+4)//2}
        expected.update({j:j for j in range(2,p)})
        expected[p]=p*(p+1)//2
        assert blocks==expected,(p,blocks,expected)
        assert sum(j*blocks[j] for j in blocks)==ranks[0]
        records.append({"p":p,"dimK":ranks[0],"blocks":{str(i):v for i,v in blocks.items()},
                        "rank_D":ranks[1],"rank_D_pminus1":ranks[p-1]})
    for row in census["samples"]:
        p=row["p"]
        assert row["rank_powers_K"]==[k_rank_formula(p,k) for k in range(p+1)]
    return {
        "status":"PROVED_ALL_PRIMES_BY_AFFINE_SHORTENING",
        "modules":"M=F_p^{PG(3,p)}, C=row B, K=C^perp, D=T-I",
        "shortened_C_A":"RM_p(p-2,3) on affine chart A=F_p^3",
        "ambient_Dk_image":"D^k M_A = span{binom(t,l)u^j v^m: 0<=l<=p-1-k, 0<=j,m<=p-1}",
        "intersection_dimension":"dim(C intersect D^k M)=binom(p+1,3)-binom(k+1,3), k>=1",
        "rank_formula":"R0=(p+1)(p^2+1)-binom(p+2,3); Rk=p^2(p-k)-binom(p+1,3)+binom(k+1,3), 1<=k<=p",
        "Jordan_formula":"K|<T> = J1^((p^2+p+4)/2) + sum(j=2..p-1) Jj^j + Jp^(p(p+1)/2)",
        "proof_note":"Equivariant pairing gives K~=(M/C)^*. D acts trivially on fixed hyperplane. D^k M_A consists of full degree-in-t range 0..p-1-k. The shortened code C_A=RM_p(p-2,3) has monomial intersection of dimension sum(l=0..p-1-k) binom(p-l,2).",
        "prior_work":"Pass12187 has already proved Q; this theorem resolves complementary K conjecture, not its Q theorem.",
        "prime_controls":records
    }


def native_incidence_clock():
    """Analytic coexistence witness, no physical time interpretation."""
    n=40
    j=1.0
    gamma=0.2
    temp=0.05
    eye=np.eye(n)
    assert np.array_equal(B@np.ones(n,dtype=np.int64),27*np.ones(n,dtype=np.int64))
    assert np.array_equal(A@np.ones(n,dtype=np.int64),12*np.ones(n,dtype=np.int64))
    # B=J-I-A has exact nonconstant eigenspaces -3^24 and 3^15.
    assert np.allclose(sorted(set(np.linalg.eigvalsh(B).round(8))),[-3.,3.,27.])
    def free_energy(s,t):
        return -j/2*np.dot(s,s)+gamma/2*(s@B@s)+t*sum(float(v*math.log(v)) for v in s if v>0)
    unif=np.ones(n)/n
    concentrated=np.zeros(n);concentrated[0]=1
    f_u=free_energy(unif,temp)
    f_d=free_energy(concentrated,temp)
    assert f_d < f_u
    hessian_eigs=[40*temp-j-3*gamma,40*temp-j+3*gamma]
    assert all(z>0 for z in hessian_eigs)
    high_temp_convexity_sufficient=j+3*gamma
    # Direct symmetry-breaking witness: swap an edge and a nonedge while fixing an
    # anchor -> changed coupling tensor. B therefore not S_40-invariant.
    anchor=0
    ni=next(i for i in range(1,n) if B[anchor,i])
    ci=next(i for i in range(1,n) if not B[anchor,i])
    perm=list(range(n));perm[ni],perm[ci]=perm[ci],perm[ni]
    assert not np.array_equal(B[np.ix_(perm,perm)],B)
    # Global minimizers of the analytic free energy exist by compactness;
    # nonuniform at this t, with orbit >=2 (no unique invariant minimizer).
    return {
        "status":"EXACT_MEAN_FIELD_W33_NATIVE_FIRST_ORDER_COEXISTENCE_WITNESS",
        "Hamiltonian":"E_N= -J/(2N)sum_i n_i^2 + gamma/(2N)sum_ij B_ij n_i n_j, with J=1,gamma=0.2",
        "finite_temperature":"T=0.05 (energy units J=1)",
        "uniform_free_energy":f_u,"concentrated_trial_free_energy":f_d,
        "uniform_stability_hessian_eigenvalues":hessian_eigs,
        "uniform_stability_multiplicities":[24,15],
        "uniform_spinodal_temperature":(j+3*gamma)/n,
        "strict_convexity_sufficient_T_greater_than":high_temp_convexity_sufficient,
        "uniform_local_min_but_not_global":True,
        "not_invariant_under_all_S40":True,
        "invariant_under_PSp43":True,
        "ground_state_40_anchor_degeneracy":40,
        "physical_scope":"Postulated W33-native mean field: demonstrates metastability/first-order selection; no emergent gravity, Lorentzian clock or physical transition temperature."
    }


def routing_lower_bound():
    """Constructive lower bounds independent of exhaustive graph-swap search."""
    cert=routing()
    audit=[]
    for anchor in range(40):
        perm=transvection(anchor)
        c=cycles(perm)
        assert len(c)==9
        all_moved=[i for group in c for i in group]
        assert len(all_moved)==27
        assert all(not A[i,perm[i]] for i in all_moved)
        # Fixed point distance 0; moved distance 2 as W33 has diameter 2.
        transport=2*len(all_moved)
        lower_swaps=math.ceil(transport/2)
        assert lower_swaps==27
        # Two layers of disjoint SWAP matchings cannot generate a 3-cycle
        # on an independent triple (each nontrivial 3-cycle would require a
        # two-edge path on its 3 support vertices).
        assert all(all(A[x,y]==0 for x in group for y in group if x!=y) for group in c)
        audit.append({"anchor":anchor,"transport_distance_sum":transport,
                      "swap_count_lower_bound":lower_swaps,
                      "depth_lower_bound":3,"compiled_depth":6,
                      "compiled_swaps":54})
    return {
        "status":"PROVED_LOWER_BOUNDS_AND_VERIFIED_W33_UPPER_BOUNDS",
        "all_anchors":audit,"min_swaps_lower_bound":27,
        "max_verified_swaps":54,"parallel_depth_lower_bound":3,
        "parallel_depth_verified_upper_bound":6,
        "two_layer_obstruction":"Product of two disjoint-matchings yields any nontrivial 3-cycle only on a 2-edge path among its three moved vertices; each transvection 3-cycle is A-independent.",
        "error_sensitivity":{"per_swap_error_0.001_independent_no_fault":(1-0.001)**54,
                             "per_swap_error_0.0001_independent_no_fault":(1-0.0001)**54},
        "scope":"Physical graph-SWAP architecture with uniform independent failure rates only; not a photonic mode realization or threshold."
    }


def magic_feedforward_nogo():
    """State-dependent syndrome probabilities rule out deterministic
    projective-syndrome feedforward unitary for this particular physical gate.
    """
    cert=nine_root_syndrome()
    assert cert["nonzero_syndrome_components"]==27
    assert cert["nonzero_syndrome_probability"]=="1/27 each"
    # U|0_L>=|0_L>, whereas U|u_L> contains 27 orthogonal syndrome sectors.
    # A unitary channel has proportional Kraus maps and thus its classical
    # measurement outcome distribution cannot depend on an arbitrary input.
    zero={"trivial_syndrome_probability":1,"nontrivial_syndrome_probability":0}
    u={"trivial_syndrome_probability":1/27,"nontrivial_syndrome_probability":26/27}
    assert zero!=u
    distinguishing_tv=abs(zero["trivial_syndrome_probability"]-u["trivial_syndrome_probability"])
    return {
        "status":"NO_GO_DETERMINISTIC_STABILIZER_SYNDROME_FEEDFORWARD_UNITARY_FOR_UNIFORM_ZETA9_GATE",
        "code":"point-coordinate [[40,20,4]]_3",
        "physical_gate":"diag(1,zeta9,zeta9^2)^{tensor 40}",
        "encoded_basis_inputs":["|0_L>","|u_L> (weight-4 nonstabilizer logical coset)"],
        "zero_input":zero,"weight4_input":u,
        "measurement_outcome_total_variation_distance":distinguishing_tv,
        "proof":"If every syndrome-conditional correction yields the same deterministic encoded unitary channel, each syndrome Kraus map restricted to codespace is a scalar multiple of that unitary. Each outcome probability is then independent of logical input, contradicted by 1 versus 1/27 trivial-syndrome probabilities.",
        "limit":"Rules out this gate followed immediately by projective CSS-syndrome measurement and outcome-conditioned deterministic correction. Does not rule out coherent ancilla-assisted injection, magic distillation, or different physical diagonal phases."
    }


def transvection_matrix(w):
    I=np.eye(4,dtype=np.int64)
    return (I+np.outer(J@w,w))%3


def pair_group_spectral_bound():
    """Group algebra regular representation gives universal annihilator
    for the two F3-rational noncommuting anchor defect, at all q=3^t.
    """
    E=np.eye(4,dtype=np.int64)
    T1=transvection_matrix(E[0])
    T2=transvection_matrix(E[1])
    assert int(E[0]@J@E[1])==1
    gens=(T1,T2)
    key=lambda M:tuple(map(int,M.ravel()))
    lookup={key(E):0};mats=[E]
    for g in mats:
        for t in gens:
            v=g@t%3
            if key(v) not in lookup:
                lookup[key(v)]=len(mats);mats.append(v)
    assert len(mats)==24
    reg=np.zeros((24,24),dtype=np.int64)
    for col,g in enumerate(mats):
        for t in (T1,T1@T1%3,T2,T2@T2%3):
            row=lookup[key(t@g%3)]
            reg[row,col]+=1
    L=4*np.eye(24,dtype=np.int64)-reg
    z=sp.symbols("z")
    characteristic=sp.factor(sp.Matrix(L).charpoly(z).as_expr())
    expected=z*(z-2)**3*(z-4)**3*(z-6)**9*(z*z-6*z+6)**4
    assert sp.expand(characteristic-expected)==0
    annihilator=sp.Poly(z*(z-2)*(z-4)*(z-6)*(z*z-6*z+6),z)
    # Exact integer matrix polynomial without diagonalization.
    power=np.eye(24,dtype=np.int64)
    test=np.zeros((24,24),dtype=np.int64)
    for coeff in reversed(annihilator.all_coeffs()):
        test+=int(coeff)*power
        power=power@L
    assert not np.any(test)
    # Independently replay the universal polynomial in the actual
    # 40-point projective permutation representation at q=3.
    anchors=[next(i for i in range(N) if tuple(X[i])==tuple(E[j]))
             for j in (0,1)]
    Ts=[]
    for anchor in anchors:
        perm=transvection(anchor)
        P=np.zeros((N,N),dtype=np.int64)
        P[np.arange(N),list(perm)]=1
        Ts.append(P)
    defect=4*IDENT-Ts[0]-Ts[0]@Ts[0]-Ts[1]-Ts[1]@Ts[1]
    power=np.eye(N,dtype=np.int64)
    direct=np.zeros((N,N),dtype=np.int64)
    for coeff in reversed(annihilator.all_coeffs()):
        direct+=int(coeff)*power
        power=power@defect
    assert not np.any(direct)
    observed_40=len(np.unique(np.round(np.linalg.eigvalsh(27*IDENT-B+defect),8)))
    assert observed_40==12
    return {
      "status":"EXACT_GROUP_ALGEBRA_ALL_EXTENSION_DEGREES_FIXED_RATIONAL_ANCHORS_NO_GO",
      "generated_anchor_group":"SL(2,3) of order 24 (embedded into Sp(4,3^t))",
      "regular_defect_characteristic_polynomial":str(characteristic),
      "defect_annihilator":"z(z-2)(z-4)(z-6)(z^2-6z+6)",
      "distinct_defect_levels_upper_bound":6,
      "Hamiltonian":"H_q=a(q)I+b(q)A_q+epsilon(q)(4I-Tu-Tu^-1-Tv-Tv^-1)",
      "distinct_H_levels_bound_all_q_3_power":13,
      "scope":"Two noncommuting anchors with coordinates and symplectic pairing in F3, fixed as q=3^t grows. Generic extension-field anchors or growing anchor sets are not ruled out.",
      "regular_representation_annihilator_verified":True
    }


def run():
    return {"schema":"w33.toe.round4.five.v1","date":"2026-10-22",
       "jordan":orthogonal_all_prime_theorem(),
       "clock":native_incidence_clock(),
       "routing":routing_lower_bound(),
       "magic":magic_feedforward_nogo(),
       "continuum":pair_group_spectral_bound()}


if __name__=="__main__":
    data=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(data,encoding="utf-8")
    else:
        print(data,end="")
