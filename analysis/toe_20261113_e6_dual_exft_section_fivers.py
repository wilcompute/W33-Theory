#!/usr/bin/env python3
"""Exact E6(6) dual d-symbol and coordinate solution census for ExFT section.

Construct both symmetric 27^3 invariant tensors directly from canonical
signed 45 triads. Normalize d_{MNK} d^{PNK}=delta_M^P, test all 78 Lie
generators under covariant and contragredient actions, enumerate 72 sixers
and the 216 inclusion-maximal five-coordinate sections, then classify the
latter under the 648 Fermat automorphisms.

The coordinate subspaces solve the genuine algebraic E6(6) section
condition d^{MNK} partial_M f partial_N g = 0. Coordinate solutions
do not alone identify all global continuous sections or physical dynamics.
"""
from collections import Counter,defaultdict
from itertools import combinations, permutations
from pathlib import Path
import sys,json
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_fermat_cubic_h27_sixers as F
OUT=ROOT/"data/toe_20261113_e6_exft_dual_d_symbol_sections.json"

def exact_cubic_action(X,triads):
    """Return residual monomial coefficients for induced infinitesimal X."""
    coeff=defaultdict(int)
    row_nz={i:np.flatnonzero(X[i]) for i in range(27)}
    for term,s in triads.items():
        for pos,a in enumerate(term):
            for b in row_nz[a]:
                word=list(term);word[pos]=int(b)
                coeff[tuple(sorted(word))]+=s*int(X[a,b])
    return {k:v for k,v in coeff.items() if v}

def d_symbol_checks(triads,root_generators,diags):
    # Z tensor t_{ijk}=s_ijk for all permutations (and 0 otherwise),
    # d=t/sqrt(10), so pairing is integer 10*delta.
    t={}
    for term,s in triads.items():
        for perm in set(permutations(term)):
            assert perm not in t
            t[perm]=s
    assert len(t)==270
    D=np.zeros((27,27,27),dtype=np.int8)
    for (i,j,k),s in t.items():D[i,j,k]=s
    gram=np.einsum("imn,jmn->ij",D.astype(np.int64),D.astype(np.int64))
    assert np.array_equal(gram,10*np.eye(27,dtype=np.int64))
    assert np.array_equal(D,D.transpose(1,0,2))
    assert np.array_equal(D,D.transpose(0,2,1))
    # The original cubic is N(x)=(1/6) sum t_ijk x_i x_j x_k.
    # Tensor is 't' in the invariant (lower) dual pair; normalization
    # both upper and lower d=t/sqrt(10) uses the compact metric.
    checks=0
    transpose_checks=0
    for X in root_generators+diags:
        assert not exact_cubic_action(X,triads)
        checks+=1
        # The same tensor is contragredient-invariant only if X^T also
        # preserves the cubic (certified E6 root basis is transpose-stable).
        assert not exact_cubic_action(X.T,triads)
        transpose_checks+=1
    assert checks==78
    return {"ordered_nonzero_tensor_entries":270,
            "normalization":"d_{MNK}=d^{MNK}=s_{MNK}/sqrt(10) for 270 ordered triad entries, zero elsewhere",
            "contraction":"d_{MNK}d^{PNK}=delta_M^P",
            "integer_contraction_diagonal":10,
            "integer_contraction_offdiagonal":0,
            "covariant_invariance_generators_verified":checks,
            "contravariant_dual_invariance_generators_verified":transpose_checks,
            "metric_warning":"Using the same signed coordinate array for lower and upper d is a statement about this split real E6 Chevalley basis and compact Euclidean metric, not a metric identification valid in all E6 gauge frames."}

def section_census(triads):
    G=nx.Graph()
    G.add_nodes_from(range(27))
    for t in triads:G.add_edges_from(combinations(t,2))
    Q=nx.complement(G)
    maxcliques=sorted(tuple(sorted(c)) for c in nx.find_cliques(Q))
    sizes=Counter(map(len,maxcliques))
    assert sizes==Counter({5:216,6:72}),sizes
    sections5=[s for s in maxcliques if len(s)==5]
    sections6=[s for s in maxcliques if len(s)==6]
    for s in maxcliques:
        assert all(len(set(s)&set(t))<=1 for t in triads)
    # actual upper-index condition for ANY two basis derivatives in each
    # section: the d(t) bilinear polarization vanishes for all 27 K.
    assert all(not any(sum(i in s for i in t)>1 for t in triads) for s in maxcliques)
    # Reconstruct the Fermat isomorphism from its prior explicit certificate.
    bridge=json.loads((ROOT/"data/toe_20261113_fermat_cubic_h27_sixers.json").read_text())
    mapping={int(i):int(z) for i,z in bridge["E6_index_to_Fermat_line_id"].items()}
    images5=sorted(frozenset(mapping[i] for i in s) for s in sections5)
    images6=sorted(frozenset(mapping[i] for i in s) for s in sections6)
    Fermat=F.geometry()
    Aut=F.automorphisms(Fermat)
    def orbits(images):
        lookup={x:i for i,x in enumerate(images)}
        rest=set(range(len(images)))
        records=[]
        while rest:
            q=min(rest)
            orb={lookup[frozenset(p[i] for i in images[q])] for p in Aut}
            assert orb<=rest
            rest-=orb
            reps=sorted(images[q])
            records.append({"order":len(orb),
                            "group_stabilizer_size":648//len(orb),
                            "representative_fermat_lines":reps,
                            "representative_sectors":tuple(sum(i//9==b for i in reps) for b in range(3))})
        return sorted(records,key=lambda x:(x["order"],x["representative_fermat_lines"]))
    orbit5=orbits(images5)
    orbit6=orbits(images6)
    assert [x["order"] for x in orbit6]==[18,54]
    assert sum(x["order"] for x in orbit5)==216
    # Any subset of five of a sixer is extendible; a "maximal five"
    # is strictly distinguished from these by failure to extend.
    embedded5={tuple(sorted(set(s)-{p})) for s in sections6 for p in s}
    assert not any(s in embedded5 for s in sections5)
    return {
       "graph":"E6 Schlaefli line meeting graph SRG(27,10,1,5)",
       "coordinate_maximal_section_counts":{"5":216,"6":72},
       "coordinate_exact_E6_section_condition":True,
       "maximal_5_sections_not_subsets_of_any_6_section":True,
       "Fermat_projective_automorphism_order":len(Aut),
       "five_section_fermat_orbits":orbit5,
       "six_section_fermat_orbits":orbit6,
       "five_section_fibre_patterns":dict(Counter(str(tuple(sorted(sum(i//9==b for i in s) for b in range(3)))) for s in images5)),
       "all_maximal_five_sections_E6_indices":[list(s) for s in sections5],
       "fiver_vs_IIB_section_interpretation":"A 5D coordinate-maximal solution is a mathematically valid 5-coordinate solution to the same bilinear E6 section constraint. Identifying it with an inequivalent Type IIB orbit requires explicit GL5 x SL2 embedding or E6(6)-orbit invariant; cannot infer it from dimension alone."}

def main():
    _,triads,_,_,roots=R.load()
    certificate=json.loads((ROOT/"data/toe_20261108_exact_signed_cubic_stabilizer.json").read_text())
    diagonal=[]
    for rec in certificate["cubic_27"]["generators"]:
        mat=np.zeros((27,27),dtype=np.int64)
        for i,j,v in rec:mat[i,j]=v
        if np.count_nonzero(mat-np.diag(np.diag(mat)))==0:diagonal.append(mat)
    assert len(roots)==72 and len(diagonal)==6
    tensor=d_symbol_checks(triads,roots,diagonal)
    sections=section_census(triads)
    result={"schema":"toe.e6.ExFT.dual.d.section.fivers.v1",
            "status":"PASS_DUAL_E6_INVARIANT_AND_EXACT_72_SIX_216_FIVE_COORDINATE_SECTIONS",
            "tensor":tensor,"sections":sections,
            "physical_scope":"The genuine algebraic E6(6) ExFT bilinear section constraint is satisfied for coordinate-supported sixers and maximal fivers. It is not a proof that this finite geometry produces the supergravity equations of motion, nor an exhaustive classification of all continuous sections.",
            "literature":"Hohm Samtleben 2014 and Polyvector deformations of Type IIB backgrounds EPJC 2024, which state d^{MNK} partial_M(.) partial_N(.) = 0 and 6D M / 5D IIB solutions."}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],
     "normalized_dual":tensor["contraction"],
     "full_E6_invariance":tensor["covariant_invariance_generators_verified"],
     "five_orbits":[x["order"] for x in sections["five_section_fermat_orbits"]],
     "six_orbits":[x["order"] for x in sections["six_section_fermat_orbits"]],
     "five_patterns":sections["five_section_fibre_patterns"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
