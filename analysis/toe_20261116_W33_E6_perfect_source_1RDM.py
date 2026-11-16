#!/usr/bin/env python3
"""Exact single-photon reduced density spectrum of the perfect 4-copy W33-E6
Kraus resource. Derives strict upper bound on ANY identical-product source
fidelity from 1RDM eigenvalue (monotonicity under partial trace).
"""
from collections import Counter,defaultdict
from itertools import combinations
from fractions import Fraction as F
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_W33_symmetry_minimal_fourcopy import build_geometry
OUT=ROOT/"data"/"toe_20261116_W33_E6_perfect_source_entanglement.json"

def run():
    pts,idx,octets,SI,cliques,LI,A,adj=build_geometry()
    owners=defaultdict(list)
    for i,s in enumerate(octets):
        for p in combinations(sorted(s),2):owners[p].append(i)
    assert Counter(len(x) for x in owners.values())=={1:540,3:240}
    pset=[[] for _ in range(45)]
    for p,ix in owners.items():
        if len(ix)==1:pset[ix[0]].append(p)
    assert all(len(x)==12 for x in pset)
    m=Counter()
    edge_count=0
    for i,j in combinations(range(45),2):
        if octets[i]&octets[j]:continue
        edge_count+=1
        for p in pset[i]:
            for q in pset[j]:
                subset=tuple(sorted((*p,*q)))
                assert len(set(subset))==4
                m[subset]+=1
    assert edge_count==270
    assert Counter(m.values())=={1:6480,2:16200}
    norm_squared=sum(x*x for x in m.values())
    assert norm_squared==71280
    # For 4 identical bosons, 1RDM[p,q] =
    # (1/(4*||m||²)) sum_{|T|=3} m(T+p)m(T+q).
    triples=defaultdict(dict)
    for subset,val in m.items():
        for p in subset:
            T=tuple(x for x in subset if x!=p)
            triples[T][p]=val
    H=[[0]*40 for _ in range(40)]
    for vals in triples.values():
        for p,v in vals.items():
            for q,w in vals.items():H[p][q]+=v*w
    diag={H[p][p] for p in range(40)}
    edge={H[p][q] for p,q in combinations(range(40),2) if adj[p][q]}
    nonedge={H[p][q] for p,q in combinations(range(40),2) if not adj[p][q]}
    assert diag=={7128} and edge=={1836} and nonedge=={2160}
    n,a,b=7128,1836,2160
    for i in range(40):
        for j in range(40):
            assert H[i][j]==(n if i==j else a if adj[i][j] else b)
            common=sum(adj[i][k] and adj[j][k] for k in range(40))
            assert common==(12 if i==j else 2 if adj[i][j] else 4)
    eig=[F(n+12*a+27*b,4*norm_squared),
         F(n+2*a-3*b,4*norm_squared),
         F(n-4*a+3*b,4*norm_squared)]
    assert eig==[F(27,88),F(1,66),F(29,1320)]
    purity=eig[0]**2+24*eig[1]**2+15*eig[2]**2
    assert purity==F(194,1815)
    assert eig[0]+24*eig[1]+15*eig[2]==1
    # For any |psi>^tensor4, monotonicity of fidelity under
    # tracing out three particles implies
    # |<psi^tensor4|Psi*>|² <= <psi|gamma1|psi>
    # <= lambda_max(gamma1) = 27/88.
    max_identical_product_fidelity_bound=max(eig)
    # |+40>^tensor4 has amplitude sqrt(24)/40² on each
    # four-distinct occupation basis state.
    uniform_overlap_squared=F(24*sum(m.values())**2,
                               40**4*norm_squared)
    assert uniform_overlap_squared==F(2187,11000)
    result={
      "status":"EXACT_W33_E6_FOURPHOTON_PERFECT_RESOURCE_1RDM_ENTANGLEMENT",
      "quartet_basis_support":len(m),"one_decomposition_count":6480,
      "two_decomposition_count":16200,
      "resource_amplitude":"m(S)/sqrt(71280), with m(S)=1 or 2",
      "resource_norm_squared_integer":norm_squared,
      "one_body_correlation_integer_denom":4*norm_squared,
      "one_body_correlation_diagonal_adj_nonadj":[n,a,b],
      "one_body_eigenvalues_by_multiplicity":[
        {"numerator":v.numerator,"denominator":v.denominator,"multiplicity":c}
        for v,c in zip(eig,(1,24,15))],
      "one_body_purity":{"numerator":purity.numerator,"denominator":purity.denominator},
      "one_body_rank":40,
      "max_identical_fourfold_product_source_fidelity_upper":{
        "numerator":max_identical_product_fidelity_bound.numerator,
        "denominator":max_identical_product_fidelity_bound.denominator},
      "uniform_coherent_fourfold_product_source_fidelity_exact":{
        "numerator":uniform_overlap_squared.numerator,
        "denominator":uniform_overlap_squared.denominator},
      "justification":"Pure-state fidelity monotonicity under partial trace: |<psi^4|Psi*>|^2 <= <psi|gamma1|psi> <= largest 1RDM eigenvalue 27/88. Bound is not claimed tight.",
      "scope":"Exact invariant of an abstract Fock-sector four-boson resource, not a successful optical preparation. It bounds overlap with identical single-mode product powers only, NOT with all separable four-mode inputs or any arbitrary 4-photon circuit."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result

if __name__=="__main__":
    d=run()
    print("PASS",d["status"],"1RDM purity",d["one_body_purity"],flush=True)
