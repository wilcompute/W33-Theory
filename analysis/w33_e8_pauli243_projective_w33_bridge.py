#!/usr/bin/env python3
"""Project the newly explicit E8 Pauli243 subgroup to W33 objectwise.

Parent theorem:
    G = H27_int o H27_ext = 3_+^(1+4) <= E8,
with the internal H27 coming from E6 trinification and the external H27 from
the physical A2/FI construction.

Write one H27 element in normal form Z^a X^b z^c.  After identifying the two
centers in the central product, the projective quotient G/Z(G) is coordinatized
by
    v = (b_int, b_ext, a_int, a_ext) in F3^4.

This script does not merely invoke the abstract fact that a two-qutrit Pauli
quotient is F3^4.  It computes the commutator in the *parent central-product
group* and proves that, in the E8-derived basis above,
    [g(v),g(w)] = z^{-omega(v,w)}
with
    omega(v,w)=b_i a_i' - a_i b_i' + b_e a_e' - a_e b_e'.

Projectivizing the 80 nonzero quotient vectors by v~2v gives 40 points.
Commutation/omega=0 gives exactly SRG(40,12,2,4), with 40 maximal isotropic
projective lines of size 4: W(3,3).

Hence this is an explicit E8 -> Pauli243 -> W33 map, not only an abstract
post-hoc isomorphism.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_pauli243_projective_w33_bridge.json"

def load(path:Path,name:str):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

P=3

def norm(v):
    v=tuple(x%P for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple(inv*y%P for y in v)
    raise ValueError("zero")

def omega(v,w):
    bi,be,ai,ae=v; BI,BE,AI,AE=w
    return (bi*AI-ai*BI + be*AE-ae*BE)%P

def points():
    return sorted({norm(v) for v in itertools.product(range(P),repeat=4) if any(v)})

def add(u,v): return tuple((u[i]+v[i])%P for i in range(4))
def scale(a,u): return tuple((a*x)%P for x in u)

def lines(pts):
    idx={p:i for i,p in enumerate(pts)}
    out=set()
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            if omega(pts[i],pts[j])!=0: continue
            members=set()
            for a,b in itertools.product(range(P),repeat=2):
                if a==b==0: continue
                members.add(norm(add(scale(a,pts[i]),scale(b,pts[j]))))
            assert len(members)==4
            out.add(tuple(sorted(idx[x] for x in members)))
    return sorted(out)

def main(write=True):
    parent=json.loads((ROOT/"data/w33_e8_trinification_two_qutrit_pauli243.json").read_text())
    assert parent["status"]=="PASS_E8_CONTAINS_TRINIFICATION_CENTRAL_PRODUCT_TWO_QUTRIT_PAULI243"

    mod=load(ROOT/"analysis/w33_e8_trinification_two_qutrit_pauli243.py","pauli243_parent")
    H=mod.H; I=mod.I
    z=(0,0,1)
    # Embed quotient vector v=(b_i,b_e,a_i,a_e) as the central-product class
    # of ((a_i,b_i,0),(a_e,b_e,0)).
    def lift(v):
        bi,be,ai,ae=v
        return mod.canonical_coset(((ai,bi,0),(ae,be,0)))

    # Extract central exponent k from a central coset by comparison with z^k.
    central_reps={mod.canonical_coset(((0,0,k),(0,0,0))):k for k in range(3)}
    assert len(central_reps)==3

    vectors=list(itertools.product(range(3),repeat=4))
    assert len({lift(v) for v in vectors})==81

    comm_table={}
    for v in vectors:
        for w in vectors:
            gv,gw=lift(v),lift(w)
            c=mod.canonical_coset(mod.pmul(mod.pmul(mod.pmul(gv,gw),mod.pinv(gv)),mod.pinv(gw)))
            k=central_reps[c]
            # Parent convention gives the negative of the repository's
            # standard (b,b,a,a) symplectic form; zero locus is identical.
            assert k==(-omega(v,w))%3
            comm_table[(v,w)]=k

    pts=points()
    assert len(pts)==40
    # Every nonzero vector belongs to exactly one projective ray {v,2v}.
    ray_members={p:{p,scale(2,p)} for p in pts}
    assert len(set().union(*ray_members.values()))==80
    assert all(len(s)==2 for s in ray_members.values())

    L=lines(pts)
    assert len(L)==40 and all(len(x)==4 for x in L)

    # W33 point graph from parent-group commutation.
    neigh=[set() for _ in pts]
    for i,j in itertools.combinations(range(40),2):
        # Lift canonical ray reps and use actual group commutator.
        if comm_table[(pts[i],pts[j])]==0:
            neigh[i].add(j); neigh[j].add(i)
    deg=Counter(len(x) for x in neigh)
    assert deg==Counter({12:40})
    lam=set(); mu=set()
    for i,j in itertools.combinations(range(40),2):
        n=len(neigh[i]&neigh[j])
        (lam if j in neigh[i] else mu).add(n)
    assert lam=={2} and mu=={4}

    # Lines are exactly maximal 4-cliques in the commuting graph.
    line_sets={frozenset(x) for x in L}
    four_cliques=set()
    for comb in itertools.combinations(range(40),4):
        S=set(comb)
        if all(j in neigh[i] for i,j in itertools.combinations(comb,2)):
            four_cliques.add(frozenset(S))
    assert four_cliques==line_sets

    # Literal comparison with the repository's canonical two-qutrit verifier:
    generic=load(ROOT/"tools/verify_w33_two_qutrit_pauli_geometry.py","generic_w33_pauli")
    gpts=sorted(generic._construct_points())
    assert pts==gpts
    assert all(omega(v,w)==generic._omega(v,w) for v in pts for w in pts)

    out={
      "schema":"w33.e8_pauli243_projective_w33_bridge.v1",
      "status":"PASS_EXPLICIT_E8_PAULI243_PROJECTIVE_QUOTIENT_IS_CANONICAL_W33",
      "headline":"The newly constructed E8 subgroup 3_+^(1+4) projects objectwise to the repository's canonical W33 coordinates. In the basis (X_int,X_ext,Z_int,Z_ext), G/Z(G)=F3^4 and the actual parent-group commutator is the standard two-qutrit symplectic form up to an irrelevant global sign. Projectivizing the 80 nonzero quotient elements gives 40 rays; commuting rays form SRG(40,12,2,4) and exactly 40 maximal isotropic 4-point lines. The resulting point and form tables are literally the same as the canonical W33 two-qutrit verifier.",
      "E8_generators":{
        "basis_order":["X_int","X_ext","Z_int","Z_ext"],
        "internal_H27":"trinification X_int=(X,X,I), Z_int=(Z^2,Z,I) with center Z(E6)",
        "external_H27":"physical external-A2 qutrit shift/clock with center FI/Qpsi Z3",
        "common_center":"identified in (E6 x SU3_ext)/Z3 <= E8"
      },
      "projective_quotient":{
        "group_order":243,
        "center_order":3,
        "quotient_order":81,
        "vector_space":"F3^4",
        "nonzero_vectors":80,
        "projective_rays":40,
        "ray_size":2
      },
      "commutator_form":{
        "coordinates":"(b_int,b_ext,a_int,a_ext)",
        "omega":"b_int*a_int' - a_int*b_int' + b_ext*a_ext' - a_ext*b_ext' mod 3",
        "parent_group_commutator":"[g(v),g(w)] = z^(-omega(v,w))",
        "all_81x81_pairs_checked":True
      },
      "W33":{
        "points":40,
        "degree":12,
        "lambda":2,
        "mu":4,
        "isotropic_lines":40,
        "points_per_line":4,
        "lines_equal_maximal_commuting_4_cliques":True,
        "literal_point_table_equals_repo_canonical_two_qutrit_W33":True,
        "literal_symplectic_form_equals_repo_canonical":True
      },
      "map":"E8-derived central-product element -> quotient vector (b_int,b_ext,a_int,a_ext) -> projective ray {v,2v} -> W33 point; W33 collinearity iff the original E8 Pauli representatives commute.",
      "boundary":"This is an exact finite subgroup/projective-incidence bridge. It does not identify individual E8 roots with all Pauli operators, derive dynamics, or prove a heterotic vacuum.",
      "parents":[
        "data/w33_e8_trinification_two_qutrit_pauli243.json",
        "tools/verify_w33_two_qutrit_pauli_geometry.py"
      ],
      "checks":{
        "81_projective_quotient_elements":True,
        "commutator_matches_symplectic_form":True,
        "40_projective_rays":True,
        "SRG_40_12_2_4":True,
        "40_isotropic_lines":True,
        "canonical_W33_table_match":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__": main(True)
