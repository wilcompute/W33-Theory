#!/usr/bin/env python3
"""Exact Albert RA,B,C R^-1 cyclic clock in the ORIGINAL signed E6 cubic
basis, transport seven sign flips and all 27 matrix coordinates.

Census all 216 maximal 5-coordinate and 72 maximal 6-coordinate
sections; check setwise invariant and 3-cycles and restricted spectra.
Test continuous generator S=(U-U^T)/sqrt(3) against infinitesimal
signed cubic rather than ASSUMING every finite cubic gate has a
cubic-preserving continuous logarithm.
"""
from pathlib import Path
from itertools import permutations,combinations
from collections import Counter,defaultdict
import json,sys
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_E6_exft_generalized_closure_affine as L
OUT=ROOT/"data/toe_20261113_Albert_cyclic_clock_sections.json"

def main():
    desc=json.loads((ROOT/"data/toe_20261113_h27_albert_cubic_coordinate_reconstruction.json").read_text())
    c={int(k):tuple(map(int,v)) for k,v in desc["explicit_E6_index_to_sector_matrix_coordinate"].items()}
    assert sorted(c)==list(range(27)) and len(set(c.values()))==27
    ix={a:i for i,a in c.items()}
    negative=set(map(int,desc["signed_rephasing_negative_E6_indices"]))
    _,triads,_,_,roots=R.load()
    U=np.zeros((27,27),dtype=np.int64)
    for i,(sector,a,b) in c.items():
        if sector==0:
            out=(0,(a+1)%3,b)
        elif sector==1:
            out=(1,a,b)
        else:
            out=(2,a,(b+1)%3)
        j=ix[out]
        U[j,i]=(-1 if (i in negative)^(j in negative) else 1)
    assert np.array_equal(U.T@U,np.eye(27,dtype=np.int64))
    assert np.array_equal(U@U@U,np.eye(27,dtype=np.int64))
    assert int(np.trace(U))==9
    perm=np.argmax(np.abs(U),axis=0).tolist()
    # A signed monomial gate preserves N exactly if every monomial
    # lands on a monomial with the right resulting sign.
    signedterms={}
    for term,s in triads.items():
        image=tuple(sorted(perm[i] for i in term))
        factor=np.prod([U[perm[i],i] for i in term])
        assert image not in signedterms
        signedterms[image]=int(s*factor)
    assert signedterms==triads,[(w,signedterms.get(w),triads.get(w)) for w in triads if signedterms.get(w)!=triads[w]][:5]
    cycles=[]
    seen=set()
    for i in range(27):
        if i in seen:continue
        ring=[];j=i
        while j not in seen:
            seen.add(j);ring.append(j);j=perm[j]
        assert j==i
        cycles.append(ring)
    assert Counter(map(len,cycles))==Counter({1:9,3:6})
    # Image of every section under finite clock
    T,Y,S5,S6=L.setup()
    G=nx.Graph();G.add_nodes_from(range(27))
    for t in triads:G.add_edges_from(combinations(t,2))
    sections=sorted(tuple(sorted(q)) for q in nx.find_cliques(nx.complement(G)))
    results={}
    for size in (5,6):
        pool={s for s in sections if len(s)==size}
        fixed=[s for s in pool if tuple(sorted(perm[i] for i in s))==s]
        assert len(fixed)==(18 if size==5 else 12),len(fixed)
        n3=(len(pool)-len(fixed))//3
        assert len(pool)==(216 if size==5 else 72)
        for s in fixed:
            restricted=U[np.ix_(s,s)]
            assert np.array_equal(restricted@restricted@restricted,np.eye(size,dtype=np.int64))
            assert int(np.trace(restricted))==size-3,(s,int(np.trace(restricted)))
        results[str(size)]={"total_maximal_sections":len(pool),
          "fixed_setwise":len(fixed),"period_three_section_orbits":n3,
          "restricted_eigen_multiplicities":[size-2,1,1],
          "fixed_sections":[list(s) for s in sorted(fixed)]}
    A=U-U.T
    assert np.array_equal(A.T,-A)
    assert np.array_equal(A@A@A,-3*A)
    # If V=U and S=(U-U.T)/sqrt3, infinitesimal
    # preservation of N would require contraction of A to vanish
    # (scalar 1/sqrt3 irrelevant).
    deriv=R.inf_check(A,triads) if False else None
    coeff=defaultdict(int)
    for term,sgn in triads.items():
        for p,source in enumerate(term):
            for target in np.flatnonzero(A[source,:]):
                tr=list(term);tr[p]=int(target)
                coeff[tuple(sorted(tr))]+=int(sgn)*int(A[source,int(target)])
    bad={k:v for k,v in coeff.items() if v}
    # U finite is valid even if this PARTICULAR skew logarithm is
    # not in the 36-dimensional compact E6 Lie algebra.
    compatible_infinitesimal=(len(bad)==0)
    if compatible_infinitesimal:
        _,Ks=R.pack_roots(roots)
        # Report extra-support burden for this generator.
        certificate=json.loads((ROOT/"data/toe_20261113_e6_root_matching_projection_clock.json").read_text())
        # Correct original null support from R.load
        _,_,D,_,_=R.load()
        old={(i,j) for i,j in combinations(range(27),2) if D[i,j]}
        new={(i,j) for i,j in combinations(range(27),2) if A[i,j]}
        new_edges=len(new-old)
    else:new_edges=None
    out={
       "status":"PASS_FINITE_ALBERT_RA_C_RINV_COMPATIBLE_SECTIONS",
       "source_signed_cubic_terms":45,
       "signed_E6_clock_matrix_27_sparse_entries":[[int(i),int(j),int(U[i,j])] for i,j in zip(*np.nonzero(U))],
       "clock_is_signed_order3_orthogonal":True,
       "clock_exactly_preserves_all_45_signed_cubic_terms":True,
       "clock_trace":int(np.trace(U)),
       "clock_eigen_multiplicities":[15,6,6],
       "coordinate_cycle_histogram":dict(Counter(str(len(z)) for z in cycles)),
       "fixed_sections":results,
       "skew_matrix_A_equal_UminusUT_has_infinitesimal_cubic_invariance":compatible_infinitesimal,
       "skew_A_nonzero_derivative_monomials":len(bad),
       "skew_A_extra_edges_outside_original_108":new_edges,
       "physical_boundary":"Three-step cubic-preserving signed-permutation clock has nonunique fixed sections of both sizes; it is not a dynamic vacuum selection or Lorentzian time mechanism."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","clock_eigen_multiplicities","coordinate_cycle_histogram","fixed_sections","skew_matrix_A_equal_UminusUT_has_infinitesimal_cubic_invariance","skew_A_nonzero_derivative_monomials","skew_A_extra_edges_outside_original_108"] if k!="fixed_sections"}|
               {"fixed_sections":{k:{x:v[x] for x in ["fixed_setwise","period_three_section_orbits","restricted_eigen_multiplicities"]} for k,v in results.items()}},indent=2),flush=True)
    return out
if __name__=="__main__":main()
