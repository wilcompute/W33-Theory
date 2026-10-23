#!/usr/bin/env python3
"""Five independent W33 TOE frontiers: exact theorems, finite controls, and no-go tests."""
from __future__ import annotations
import collections
import itertools
import json
import math
from math import comb
from pathlib import Path
import numpy as np

try:
    from analysis.w33_20261022_pascal_css_logical_transvection_jordan import (
        normalize, projective_points, rref, right_kernel, rank
    )
    from analysis.w33_20261022_css_logical_sp43_generators import J, perm_of_direction, DIRECTIONS
except ModuleNotFoundError:
    from w33_20261022_pascal_css_logical_transvection_jordan import (
        normalize, projective_points, rref, right_kernel, rank
    )
    from w33_20261022_css_logical_sp43_generators import J, perm_of_direction, DIRECTIONS


def point_geometry(p=3):
    x = np.asarray(projective_points(p), dtype=np.int64)
    B = ((x @ J @ x.T) % p != 0).astype(np.int64)
    C, _ = rref(B, p)
    return x, B, C


def apply_permutation_rows(matrix, perm):
    result = np.empty_like(matrix)
    result[:, list(perm)] = matrix
    return result


def stabilizer_jordan(primes=(2,3,5,7)):
    """Prove by symmetric powers, and separately verify modular ranks."""
    records = []
    for p in primes:
        x, B, C = point_geometry(p)
        perm = perm_of_direction_generic(x,p)
        assert len(set(perm)) == len(x)
        assert np.array_equal(B[np.ix_(perm,perm)], B)
        assert np.all(B@B%p==0)
        assert len(C) == comb(p+2,3)
        M=C.copy()
        ranks=[len(C)]
        for k in range(1,p+1):
            M=(apply_permutation_rows(M,perm)-M)%p
            ranks.append(rank(M,p))
        blocks={j:p-j+1 for j in range(1,p+1)}
        target=[sum(m*max(0,j-k) for j,m in blocks.items())
                for k in range(p+1)]
        assert ranks==target, (p,ranks,target)
        records.append(dict(p=p,C_dimension=len(C),
             rank_powers=ranks, jordan_blocks={str(j):int(m) for j,m in blocks.items()}))
    return {"status":"THEOREM_C_MODULE_LOGICAL_Q_OPEN",
       "module":"C=Sym^(p-1)(F_p^4)^*, restricted to order-p transvection",
       "all_prime_formula":"sum_(j=1)^p J_j^(p-j+1)",
       "proof":"V^*=J2 + 1 + 1; degree p-1 monomials split as sum_t Sym^t(J2) tensor Sym^(p-1-t)(1+1), with Sym^t(J2)=J_(t+1) for t<p",
       "finite_regressions":records}


def perm_of_direction_generic(coords, p):
    lookup={tuple(z):i for i,z in enumerate(coords.tolist())}
    w=coords[0]
    return tuple(lookup[normalize(z+(int(z@J@w)%p)*w,p)] for z in coords)


def anchored_clock_selection():
    """Rigorous toy energy / finite ensemble firewall; no claim of fundamental dynamics."""
    n=40
    a=2
    gamma=3
    x, B, C = point_geometry()
    assert n == len(x)
    assert np.all(B.sum(axis=1)==27)
    rng=np.random.default_rng(20261022)
    samples=1000
    best=1000.0
    for _ in range(samples):
        z=rng.normal(size=n);z/=np.linalg.norm(z)
        s=z*z
        potential=-a*np.sum(s*s)+gamma*(s@B@s)/2
        assert potential>=-a-1e-10
        best=min(best,float(potential))
    # V=-a sum x_i^4+gamma sum_(i<j)B_ij x_i² x_j² on S^39.
    # Both inequalities saturated only at +/- basis vectors.
    return {"status":"EXACT_TOY_MINIMA_FINITE_T_NO_SPONTANEOUS_SELECTION",
        "energy":"V(x)=-a*sum(x_i^4)+gamma*sum_(i<j)B_ij*x_i^2*x_j^2; norm(x)=1; a>0 gamma>=0",
        "global_minimum":"-a", "minimizers":"{+e_i,-e_i : i=1..40}",
        "projective_minima":40,
        "group_transitive":"PSp(4,3) permutes all 40 anchor choices",
        "tangent_Hessian":"diag(4*a + 2*gamma*B_ij, j!=i): 12 directions 4a and 27 directions 4a+2gamma",
        "finite_temperature_exact":"Gibbs measure is PSp-invariant, hence E[x_i^2]=1/40 for every beta finite",
        "temperature_zero_ensemble":"Symmetric mixture remains unselected unless one adds a seed/thermodynamic limit",
        "numerical_nonviolations":samples,"sample_lowest_V_a2_gamma3":best}


def physical_routes():
    """One projective transvection = 9 disjoint 3-cycles, two SWAP layers on B."""
    X, B, C = point_geometry()
    A=np.ones_like(B)-np.eye(40,dtype=np.int64)-B
    total=[]
    edge_incidence=collections.Counter()
    for anchor in range(40):
        w=X[anchor]
        lookup={tuple(v):i for i,v in enumerate(X.tolist())}
        perm=tuple(lookup[normalize(z+(int(z@J@w)%3)*w,3)] for z in X)
        seen=set();cycles=[]
        for start in range(40):
            if start in seen:continue
            c=[];j=start
            while j not in seen:
                seen.add(j);c.append(j);j=perm[j]
            assert j==start and len(c) in (1,3)
            cycles.append(c)
        active=[c for c in cycles if len(c)==3]
        assert len(active)==9 and len(cycles)==22
        for a,b,c in active:
            assert B[a,b]==B[b,c]==B[a,c]==1
            assert A[a,b]==A[b,c]==A[a,c]==0
            for u,v in ((a,b),(b,c),(a,c)):
                edge_incidence[tuple(sorted((u,v)))]+=1
        # Position-swap convention: send labels initially at position i to destination perm[i].
        labels=list(range(40))
        for b,c in [(c[1],c[2]) for c in active]:labels[b],labels[c]=labels[c],labels[b]
        for a,b in [(c[0],c[1]) for c in active]:labels[a],labels[b]=labels[b],labels[a]
        destinations=[None]*40
        for pos,label in enumerate(labels):destinations[label]=pos
        assert tuple(destinations)==perm
        total.append({"anchor":anchor,"fixed_points":13,"triangles":9,"swap_gates":18,"parallel_layers":2})
    counts=collections.Counter(edge_incidence.values())
    return {"status":"EXACT_ABSTRACT_B_COUPLER_ROUTING_NOT_PHOTONIC_HARDWARE",
       "transvections_certified":len(total),"each_transvection":total[0],
       "permutation_circuits":"9 disjoint SWAPs then 9 disjoint SWAPs",
       "B_topology_degree":27,"A_topology_degree":12,
       "A_coupler_pair_within_any_moving_cycle":False,
       "distinct_B_edges_exercised":len(edge_incidence),
       "edge_anchor_multiplicities":dict(counts),
       "physical_device_assumed":False}


def nine_root_phase_nogo():
    """Complete enumeration of the 3^10 stabilizer code and one logical coset."""
    X, B, C=point_geometry()
    assert len(C)==10
    basis=right_kernel(B,3)
    u=np.zeros(40,dtype=np.int64)
    u[:4]=1
    assert np.all(B@u%3==0)
    assert rank(np.vstack((C,u)),3)==11
    coeff=np.asarray(list(itertools.product(range(3),repeat=10)),dtype=np.int64)
    codewords=coeff@C%3
    s0=codewords.sum(axis=1)%9
    assert np.all(s0==0)
    su=(codewords+u)%3
    relative=(su.sum(axis=1)-int(u.sum()))%9
    dist={int(k):int(v) for k,v in collections.Counter(relative.tolist()).items()}
    assert dist=={0:19683,3:13122,6:26244},dist
    # amplitude A=1/3+2 omega/9+4 omega²/9 = -i sqrt(3)/9
    omega=np.exp(2j*np.pi/3)
    amplitude=(dist[0]+dist[3]*omega+dist[6]*omega**2)/len(codewords)
    assert abs(abs(amplitude)**2-1/27)<1e-12
    return {"status":"EXACT_ZERO_LOGICAL_PRESERVED_OTHER_COSET_LEAKS",
        "physical_gate":"diag(1,zeta9,zeta9^2) on each of 40 qutrits",
        "non_clifford":True,"all_stabilizer_codewords":int(len(codewords)),
        "zero_logical_phase_distribution_mod9":{"0":59049},
        "logical_coset_u_support":[int(i) for i in np.nonzero(u)[0]],
        "relative_phase_distribution_mod9":{str(k):v for k,v in sorted(dist.items())},
        "code_projector_survival_probability":"1/27",
        "abstract_injection_conclusion":"Uniform transversal ninth-root gate does not preserve all encoded states. Syndrome measurement + postselection gives nonunitary state-dependent channel.",
        "encoded_non_clifford_unitary_obtained":False,
        "threshold_or_decoder_proved":False}


def continuum_fixed_characteristic(primes=(3,5,7), extensions=(1,2,3,4)):
    """Exact spectral-atom obstruction for single-tick perturbation at fixed p."""
    cases=[]
    for p in primes:
        for t in extensions:
            q=p**t
            n=(q+1)*(q*q+1)
            k=q*(q+1)
            f=q*(q+1)**2//2
            g=q*(q*q+1)//2
            assert 1+f+g==n
            r=q-1;s=-(q+1)
            lam_r=1-r/k
            lam_s=1-s/k
            distinct=(p+1)//2
            max_spec=1+2*distinct
            cases.append({"p":p,"t":t,"q":q,"n":n,
              "normalized_laplacian_nonzero_eigenvalues":[lam_r,lam_s],
              "multiplicities":[f,g],
              "anchor_perturbation_distinct_eigenvalue_upper_bound":max_spec})
    return {"status":"THEOREM_BOUNDED_ATOMIC_SPECTRUM_NO_WEYL_LAW_FIXED_CHARACTERISTIC",
       "source_prior_repo":"Pass11197 already proved uniform Laplacian collapse; this extends to ONE anchored transvection",
       "operator":"a(q)*I+b(q)*A_q + epsilon(q)*(2I-T-T^-1) with single order-p transvection",
       "nontrivial_eigenvalue_bound":"p+2 for odd fixed p, independent of t",
       "proof":"A_q has three eigenspaces and commutes with T. T has p-th roots of unity; 2-T-T^-1 has (p+1)/2 distinct eigenvalues for odd p. The constant sector contributes one point and two other A eigenspaces at most (p+1)/2 each.",
       "no_go":"This narrowly specified family cannot develop infinitely many distinct low-energy eigenvalues at fixed p. It is not a proof against interacting/tensor/graph-tower continuum models.",
       "cases":cases}


def run_all():
    return {"schema":"w33.toe.five_fronts.20261022.v1",
        "jordan":stabilizer_jordan(),
        "clock":anchored_clock_selection(),
        "routing":physical_routes(),
        "nonclifford":nine_root_phase_nogo(),
        "continuum":continuum_fixed_characteristic()}


if __name__=="__main__":
    import sys
    result=run_all()
    contents=json.dumps(result,indent=2)+"\n"
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(contents,encoding="utf-8")
    else:print(contents,end="")
