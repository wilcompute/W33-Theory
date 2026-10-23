#!/usr/bin/env python3
"""Five deeper W33 frontiers. Exact algebra, explicit routing, and physical claim firewalls."""
from __future__ import annotations
from collections import Counter
from itertools import product
from math import comb, log
from pathlib import Path
import json
import numpy as np
import sympy as sp

try:
    from analysis.w33_20261022_pascal_css_logical_transvection_jordan import (
        projective_points, normalize, rref, rank, right_kernel
    )
except ImportError:
    from w33_20261022_pascal_css_logical_transvection_jordan import (
        projective_points, normalize, rref, rank, right_kernel
    )

P=3
X=np.array(projective_points(3), dtype=np.int64)
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=np.int64)
N=len(X)
IDENT=np.eye(N,dtype=np.int64)
B=((X@J@X.T)%3!=0).astype(np.int64)
A=1-IDENT-B
C,_=rref(B,3)
INDEX={tuple(z):i for i,z in enumerate(X)}
assert N==40 and len(C)==10
assert np.array_equal(A@A, 8*IDENT-2*A+4*np.ones((N,N),dtype=np.int64))


def transvection(anchor):
    w=X[anchor]
    return tuple(INDEX[normalize(x+(int(x@J@w)%3)*w,3)] for x in X)


def cycles(g):
    vis=set(); cs=[]
    for i in range(N):
        if i in vis:continue
        c=[];j=i
        while j not in vis:
            vis.add(j);c.append(j);j=g[j]
        assert j==i
        if len(c)>1:assert len(c)==3;cs.append(c)
    return cs


def match_paths(pairs):
    """Injectively assign unused common collinearity neighbours to remote SWAPs."""
    ends=set(k for u,v in pairs for k in (u,v))
    choices={i:[h for h in range(N) if h not in ends and A[u,h] and A[v,h]]
             for i,(u,v) in enumerate(pairs)}
    matched={}
    def augment(i,seen):
        for h in choices[i]:
            if h in seen:continue
            seen.add(h)
            if h not in matched or augment(matched[h],seen):
                matched[h]=i
                return True
        return False
    for i in sorted(choices,key=lambda t:len(choices[t])):
        assert augment(i,set()), ("NO_COLLISION_FREE_ROUTING",pairs,i)
    return {i:h for h,i in matched.items()}


def routing():
    summaries=[]
    edges=Counter()
    for anchor in range(40):
        g=transvection(anchor)
        cyc=cycles(g)
        assert len(cyc)==9
        swaps=[[ (b,c) for a,b,c in cyc],[(a,b) for a,b,c in cyc]]
        positions=list(range(N))
        layers=[]
        for stage,pairs in enumerate(swaps):
            assignment=match_paths(pairs)
            triples=[(u,assignment[i],v) for i,(u,v) in enumerate(pairs)]
            assert len({x for tr in triples for x in tr})==27
            assert all(A[u,h]==1 and A[h,v]==1 and A[u,v]==0 for u,h,v in triples)
            # Remote SWAP through path u-h-v: SWAP(u,h), SWAP(h,v), SWAP(u,h).
            for k in range(3):
                simultaneous=[]
                for u,h,v in triples:
                    i,j=((u,h) if k!=1 else (h,v))
                    simultaneous.append((i,j))
                    positions[i],positions[j]=positions[j],positions[i]
                    edges[tuple(sorted((i,j)))] += 1
                assert len({x for i,j in simultaneous for x in (i,j)})==18
                layers.append(simultaneous)
        destinations=[None]*N
        for dest,label in enumerate(positions):destinations[label]=dest
        assert tuple(destinations)==g
        assert len(layers)==6 and sum(len(z) for z in layers)==54
        summaries.append({"anchor":anchor,"layers":len(layers),"swap_count":54,
                          "swap_layers":[[[int(i),int(j)] for i,j in layer] for layer in layers],
                          "intermediate_indices_per_stage":[
                              sorted(match_paths(pairs).values()) for pairs in swaps]})
    return {
        "status":"EXACT_40_OF_40_COLLINEARITY_ROUTING_FIDELITY_UNMEASURED",
        "transvections":40,"parallel_A_graph_swap_depth_upper_bound":6,
        "physical_SWAPS_per_transvection":54,
        "independent_swap_no_fault_probability":"(1-epsilon_swap)^54",
        "union_bound_gate_error_probability":"<= 54*epsilon_swap",
        "remote_pairs_per_stage":9,"stages":2,
        "W33_A_degree":12,"all_40_assignments":summaries,
        "edge_use_count_over_all_transvections":len(edges),
        "caveat":"SWAP-only abstract 40-physical-qutrit circuit; no demonstrated photonic mode coupling or error threshold"}


def jordan_extension():
    g=transvection(0)
    T=np.zeros((40,40),dtype=np.int64)
    T[np.arange(N),list(g)]=1
    D=(T-IDENT)%3
    # K = C^perp is isomorphic to (M/C)^* under ambient invariant dot product;
    # therefore K and M/C have identical Jordan types for cyclic order 3.
    ranks=[N-len(C)]
    power=IDENT.copy()
    for k in range(1,4):
        power=power@D%3
        ranks.append(rank(np.vstack((C,power)),3)-len(C))
    blocks={j:int(ranks[j-1]-2*ranks[j]+ranks[j+1]) for j in (1,2)}
    blocks[3]=int(ranks[2])
    expected={1:8,2:2,3:6}
    assert blocks==expected and ranks==[30,14,6,0]
    Cblocks={1:3,2:2,3:1}
    Qblocks={1:3,2:4,3:3}
    split={j:Cblocks[j]+Qblocks[j] for j in (1,2,3)}
    assert split!={1:8,2:2,3:6}
    return {"status":"EXACT_NONSPLIT_CYCLIC_MODULE_EXTENSION_AT_P3",
            "logical_Q_Jordan":Qblocks,"stabilizer_C_Jordan":Cblocks,
            "orthogonal_K_Jordan":blocks,"orthogonal_K_rank_powers":ranks,
            "hypothetically_split_C_plus_Q":split,"sequence_splits":False,
            "derivation":"ker(B) is equivariantly dual to M/C; compute rank((T-I)^k) on M/C via rank([C;(T-I)^k])-rank(C)",
            "boundary":"This non-splitting at p=3 is not yet a proof of all-prime Q Jordan law; check Pass12187 separately"}


def forty_state_clock():
    q=40
    betaJ=2*(q-1)/(q-2)*log(q-1)
    selected=(q-1)/q
    remaining=1/(q*(q-1))
    uniform=1/q
    def f(probs, b):
        return -0.5*sum(t*t for t in probs)+sum(t*log(t) for t in probs)/b
    symmetric=f([uniform]*q,betaJ)
    ordered=f([selected]+[remaining]*(q-1),betaJ)
    assert abs(symmetric-ordered)<1e-12
    assert betaJ<q
    return {"status":"EXACT_MEAN_FIELD_40_STATE_POTTS_TOY_THERMODYNAMIC_LIMIT",
            "Hamiltonian":"E_N=-J/(2N)*sum_(a=1)^40 n_a^2; N replicas selecting anchors a",
            "symmetry":"S40 enhancement contains PSp(4,3): no uniquely W33-geometric dynamics",
            "critical_beta_J":betaJ,
            "critical_beta_J_formula":"(2*(q-1)/(q-2))*log(q-1), q=40",
            "ordered_occupancy":selected,"other_occupancy":remaining,
            "free_energy_equal_at_transition":True,
            "uniform_local_instability_beta_J":q,
            "transition":"first-order in N->infinity; no finite-N spontaneous symmetry breaking",
            "physical_claims":"phenomenological order-parameter model, NOT a derived time arrow or Einstein dynamics"}


def nine_root_syndrome():
    coeff=np.asarray(list(product(range(3),repeat=len(C))),dtype=np.int64)
    code=coeff@C%3
    u=np.zeros(40,dtype=np.int64);u[:4]=1
    assert np.all(B@u%3==0) and rank(np.vstack((C,u)),3)==11
    rel=(((code+u)%3).sum(axis=1)-code.sum(axis=1)-u.sum())%9
    assert np.all(rel%3==0)
    f=(rel//3)%3
    # Exact degree-2 phase polynomial in the fixed reduced stabilizer coordinates.
    c0,c1,c2=coeff[:,0],coeff[:,1],coeff[:,2]
    quadratic=2*(c0*c0+c1*c1+c2*c2+c0*c1+c0*c2+c1*c2)%3
    assert np.array_equal(f,quadratic)
    Hess=np.array([[0,2,2],[2,0,2],[2,2,0]],dtype=np.int64)
    assert rank(Hess,3)==3
    z=np.exp(2j*np.pi/3)
    phase=np.power(z,f).reshape((3,)*10)
    spectral=np.fft.fftn(phase).ravel()
    probabilities=np.abs(spectral/len(f))**2
    support=np.flatnonzero(probabilities>1e-10)
    assert len(support)==27
    assert np.allclose(probabilities[support],1/27,atol=1e-12)
    assert np.isclose(probabilities.sum(),1)
    assert np.isclose(probabilities[0],1/27)
    return {"status":"EXACT_RANK3_QUADRATIC_PHASE_FLAT_FOURIER_SYNDROMES",
      "codewords_enumerated":len(f),"logical_rep_support":[0,1,2,3],
      "phase_polynomial":"f(c)=2(c0^2+c1^2+c2^2+c0*c1+c0*c2+c1*c2) mod3",
      "phase_quadratic_rank":3,"nonzero_syndrome_components":27,
      "nonzero_syndrome_probability":"1/27 each",
      "total_probability":1,
      "implication":"Physical 9th-root gate on this one logical coset coherently spreads into 27 Pauli-Z syndrome sectors. Postselection is not deterministic logical gate.",
      "feedback_decoder_or_threshold_proved":False}


def double_anchor():
    mats=[]
    for g in [transvection(i) for i in range(40)]:
        T=np.zeros((40,40),dtype=np.int64)
        T[np.arange(40),list(g)]=1
        mats.append(2*IDENT-T-T.T)
    H0=27*IDENT-B
    kA=next(i for i in range(1,40) if A[0,i])
    kB=next(i for i in range(1,40) if B[0,i])
    cases=[]
    lam=sp.symbols("lambda")
    for i in (kA,kB):
        h=sp.Matrix((H0+mats[0]+mats[i]).tolist())
        poly=sp.factor(h.charpoly(lam).as_expr())
        eigs=h.eigenvals()
        assert sum(eigs.values())==40
        cases.append({"anchor_0":0,"anchor_second":i,"relation":"collinear" if A[0,i] else "noncollinear",
                     "distinct_eigenvalues":len(eigs),"characteristic_polynomial_factorization":str(poly),
                     "integer_trace":int(sp.trace(h))})
    assert cases[0]["distinct_eigenvalues"]==6
    assert cases[1]["distinct_eigenvalues"]==12
    return {"status":"EXACT_DOUBLE_ANCHOR_40D_SYMMETRY_SPLITTING_NOT_CONTINUUM",
            "model":"H=27I-B + (2I-Tu-Tu^-1) + (2I-Tv-Tv^-1)",
            "prior_single_anchor_distinct_eigenvalues":5,
            "cases":cases,
            "caveat":"Two-anchor 12-level finite splitting escapes single-anchor p+2 bound, but 40-dimensional spectrum has no continuum/Weyl limit"}


def run():
    return {"schema":"w33.allfive_deeper.20261022.v1",
            "jordan":jordan_extension(),
            "clock":forty_state_clock(),
            "routing":routing(),
            "magic":nine_root_syndrome(),
            "continuum":double_anchor()}

if __name__=="__main__":
    import sys
    raw=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(raw,encoding="utf-8")
    else:print(raw,end="")
