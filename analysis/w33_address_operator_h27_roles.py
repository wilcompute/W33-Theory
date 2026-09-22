#!/usr/bin/env python3
"""Address H27 versus operator H27: two exact, non-identifiable roles.

ADDRESS H27
-----------
Use H27 normal form (a,b,c)=Z^a X^b omega^c with ZX=omega XZ.
In the fixed physical Clifford-648 gauge select the five C3 directions
    <omega>, <omega X>, <omega Z>, <Z X>, <omega^2 Z X^2>.
Their 45 right cosets form GQ(2,4) on the 27 group elements.  An anchored graph
isomorphism sends these 45 cosets to the 45 tritangents on the repository's
27 complete factorisation-frame carrier.

Adjoin an external phase C3.  For each base direction d and slope s=+1,-1,
the subgroup <(d,s)> in H27 x C3 has 27 right cosets.  Across five directions
and two slopes this gives 270 triples.  Under the frame isomorphism these are
exactly the 45*3! lifted matter cubic triples, one of each external phase.

The full physical Clifford-648 affine action preserves the 45-line address
geometry.  Its line orbits are 9+36.  Holding external phase labels fixed, its
action on the 270 lifted instructions has orbits 27+27+216.

OPERATOR H27
------------
Inside E6 trinification, on
    27=(3,3bar,1)+(1,3,3bar)+(3bar,1,3),
the center-correct generators X_int=(X,X,I), Z_int=(Z^2,Z,I) admit a basis
chart (m,q), m in F3^2, q in F3, with
    X_int |m,q> = |m,q+1>,
    Z_int |m,q> = omega^q |m,q>.
After tensoring with the external A2 qutrit p,
    C^81 ~= C^9_multiplicity tensor C^3_internal tensor C^3_external.
The central product Pauli243 acts as I9 tensor the irreducible 9D two-qutrit
Schrodinger representation.  Its generated complex algebra is
    I9 tensor M9(C),
and its commutant is
    M9(C) tensor I9.

The two H27s cannot be identified as permutation actions: the center of the
regular address H27 is fixed-point-free on its 27 addresses, whereas the
operator H27 center is scalar and fixes every basis ray.

Boundary: no root-gauge intertwiner between the frozen E8 roots and this
trinification tensor basis is constructed here.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import networkx as nx
from sympy.combinatorics import Permutation, PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
OUT=ROOT/"data/w33_address_operator_h27_roles.json"

from w33_exact_eisenstein import (
    ZERO,
    kronecker,
    matrix_dagger,
    matrix_rank,
    omega_power,
    zero_matrix,
)
from w33_pass1054_1059_core import build_w33_bundle, permutation_images

def load(path:Path,name:str):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

# Physical H27 convention Z^a X^b omega^c, ZX=omega XZ.
def hmul(g,h):
    a,b,c=g; A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)

H=tuple(itertools.product(range(3),repeat=3))
ID=(0,0,0)

def hpowers(d):
    return (ID,d,hmul(d,d))

def right_coset(g,d):
    return frozenset(hmul(g,h) for h in hpowers(d))

DIRECTIONS=(
    (0,0,1), # omega
    (0,1,1), # omega X
    (1,0,1), # omega Z
    (1,1,0), # Z X
    (1,2,2), # omega^2 Z X^2
)
DIRECTION_NAMES=("omega","omega X","omega Z","Z X","omega^2 Z X^2")

def srg_params(G):
    deg=set(dict(G.degree()).values())
    lam=set(); mu=set()
    for u,v in itertools.combinations(G.nodes(),2):
        n=len(set(G[u])&set(G[v]))
        (lam if G.has_edge(u,v) else mu).add(n)
    return (G.number_of_nodes(),next(iter(deg)),next(iter(lam)),next(iter(mu)))

def sorted_elements(group,degree=40):
    return sorted(group.generate_schreier_sims(),key=lambda e:tuple(permutation_images(e,degree)))

def commutator(left,right): return left**-1*right**-1*left*right

def main(write=True):
    # ---------- address theorem ----------
    assert len(H)==27 and len(set(H))==27
    assert all(len(set(hpowers(d)))==3 for d in DIRECTIONS)

    lines=[]
    line_direction=[]
    for di,d in enumerate(DIRECTIONS):
        cosets=sorted({right_coset(g,d) for g in H},key=lambda C:sorted(C))
        assert len(cosets)==9
        lines.extend(cosets)
        line_direction.extend([di]*9)
    assert len(lines)==45 and len(set(lines))==45
    incidence=Counter(p for L in lines for p in L)
    assert incidence==Counter({p:5 for p in H})

    A=nx.Graph(); A.add_nodes_from(H)
    for L in lines:
        for u,v in itertools.combinations(L,2): A.add_edge(u,v)
    assert srg_params(A)==(27,10,1,5)

    # Cross to the independent 27 complete-frame / cubic-surface carrier.
    common=load(ROOT/"analysis/w33_pass4992_4999_common.py","common_address")
    base=common.build_base()
    G27=base["G27"]
    tritangents={frozenset(t) for t in base["tritangents"]}
    assert G27.number_of_nodes()==27 and G27.number_of_edges()==135 and len(tritangents)==45

    # Anchored incidence gauge: address identity -> frame 0.  There are 1920
    # such maps, the order of the W(D5) point stabilizer; choosing the first
    # map is deterministic bookkeeping, not a canonical physical gauge.
    nx.set_node_attributes(A,{p:(p==ID) for p in A},"anchor")
    nx.set_node_attributes(G27,{i:(i==0) for i in G27},"anchor")
    GM=nx.algorithms.isomorphism.GraphMatcher(A,G27,node_match=lambda x,y:x["anchor"]==y["anchor"])
    anchored_isomorphisms=list(GM.isomorphisms_iter())
    assert len(anchored_isomorphisms)==1920
    addr_to_frame=anchored_isomorphisms[0]
    assert addr_to_frame[ID]==0
    transported={frozenset(addr_to_frame[p] for p in L) for L in lines}
    assert transported==tritangents

    # Lift to H27 x external C3 with slopes +/-1.
    def pmul(P,Q):
        g,t=P; h,u=Q
        return (hmul(g,h),(t+u)%3)
    PTS=tuple((g,t) for g in H for t in range(3))
    lifted=[]
    lift_meta=[]
    for di,d in enumerate(DIRECTIONS):
        for slope in (1,2):
            gen=(d,slope)
            subgroup=( (ID,0), gen, pmul(gen,gen) )
            cosets=set()
            for P in PTS:
                C=frozenset(pmul(P,h) for h in subgroup)
                cosets.add(C)
            assert len(cosets)==27
            for C in sorted(cosets,key=lambda X:sorted(X)):
                lifted.append(C); lift_meta.append((di,slope))
    assert len(lifted)==270 and len(set(lifted))==270
    assert all({t for _,t in C}=={0,1,2} for C in lifted)

    lifted_frames={
        frozenset((addr_to_frame[g],t) for g,t in C)
        for C in lifted
    }
    expected_lifted={
        frozenset((f,p) for f,p in zip(sorted(T),perm))
        for T in tritangents
        for perm in itertools.permutations((0,1,2))
    }
    assert len(expected_lifted)==270
    assert lifted_frames==expected_lifted

    # Full Clifford-648 affine action from Pass1054, in the physical H27 gauge.
    bundle=build_w33_bundle()
    stabilizer=bundle.point_stabilizer
    elements=sorted_elements(stabilizer)
    center=stabilizer.center(); center_elements=set(center.generate_schreier_sims())
    normal_27=None
    for e in elements:
        if e.is_identity or e in center_elements or e.order()!=3: continue
        N=stabilizer.normal_closure(PermutationGroup([e]))
        if N.order()==27: normal_27=N; break
    assert normal_27 is not None
    normal_elements=sorted_elements(normal_27)
    normal_set=set(normal_elements)
    gens=None
    for x in normal_elements:
        if x.is_identity or x in center_elements: continue
        for y in normal_elements:
            if y.is_identity or y in center_elements: continue
            z=commutator(x,y)
            if not z.is_identity and z in center_elements and PermutationGroup([x,y]).order()==27:
                gens=(x,y,z); break
        if gens: break
    assert gens is not None
    x,y,zp=gens
    coordinate_of={}
    ordered=[None]*27
    for u,v,w in itertools.product(range(3),repeat=3):
        e=x**u*y**v*zp**w
        coordinate_of[e]=(u,v,w); ordered[9*u+3*v+w]=e
    normal_index={e:i for i,e in enumerate(ordered)}

    syl2=stabilizer.sylow_subgroup(2); complement=None
    for e in elements:
        if e.order()!=3 or e in normal_set: continue
        C=PermutationGroup(list(syl2.generators)+[e])
        if C.order()==24 and len(set(C.generate_schreier_sims())&normal_set)==1:
            complement=C; break
    assert complement is not None
    complement_elements=sorted_elements(complement)
    decomposition={}
    for n in normal_elements:
        for l in complement_elements: decomposition[n*l]=(n,l)
    assert len(decomposition)==648
    def affine_perm(e):
        n,l=decomposition[e]
        return Permutation([normal_index[n*l*s*l**-1] for s in ordered])
    affine=[affine_perm(e) for e in elements]
    assert len(set(affine))==648

    # physical H27 -> Pass1054 index
    def pass_index(g):
        a,b,c=g
        u,v,w=b,a,(-a*b-c)%3
        return 9*u+3*v+w
    line_idx={frozenset(pass_index(g) for g in L) for L in lines}
    assert len(line_idx)==45
    for p in affine:
        assert {frozenset(p(i) for i in L) for L in line_idx}==line_idx

    unseen=set(line_idx); line_orbits=[]
    while unseen:
        L=next(iter(unseen))
        O={frozenset(p(i) for i in L) for p in affine}
        line_orbits.append(O); unseen-=O
    line_orbit_sizes=sorted(map(len,line_orbits))
    assert line_orbit_sizes==[9,36]

    instr_idx={
        frozenset((pass_index(g),t) for g,t in C)
        for C in lifted
    }
    assert len(instr_idx)==270
    for p in affine:
        assert {frozenset((p(i),t) for i,t in C) for C in instr_idx}==instr_idx
    unseen=set(instr_idx); instr_orbits=[]
    while unseen:
        C=next(iter(unseen))
        O={frozenset((p(i),t) for i,t in C) for p in affine}
        instr_orbits.append(O); unseen-=O
    instr_orbit_sizes=sorted(map(len,instr_orbits))
    assert instr_orbit_sizes==[27,27,216]

    # Address center is fixed-point-free in regular action.
    center_gen=(0,0,1)
    center_perm={g:hmul(center_gen,g) for g in H}
    assert all(center_perm[g]!=g for g in H)

    # ---------- operator theorem ----------
    internal=[(B,u,v) for B in "ABC" for u in range(3) for v in range(3)]
    def xint(s):
        B,u,v=s
        if B=="A": return (B,(u+1)%3,(v+1)%3)
        if B=="B": return (B,(u+1)%3,v)
        return (B,(u+1)%3,v)
    def qexp(s):
        B,u,v=s
        if B=="A": return (2*u-v)%3
        return u%3
    assert all((qexp(xint(s))-qexp(s))%3==1 for s in internal)

    # Build nine X-orbits, label them by m in F3^2, q by the clock exponent.
    unseen=set(internal); orbits=[]
    while unseen:
        seed=min(unseen); O=[]; t=seed
        while t not in O:
            O.append(t); t=xint(t)
        unseen-=set(O); orbits.append(O)
    assert len(orbits)==9 and all(len(O)==3 for O in orbits)
    mlabels=list(itertools.product(range(3),repeat=2))
    chart={}
    for m,O in zip(mlabels,sorted(orbits)):
        for s in O:
            q=qexp(s)
            assert (m,q) not in chart.values()
            chart[s]=(m,q)
    assert len(chart)==27
    assert all(chart[xint(s)]==(chart[s][0],(chart[s][1]+1)%3) for s in internal)

    # Tensor basis C^9_m x C^3_q x C^3_p.
    matter_basis=[(m,q,p) for m in mlabels for q in range(3) for p in range(3)]
    assert len(matter_basis)==81
    # Operator center is scalar.  It fixes all 27 internal E6 rays and, after
    # adjoining the external qutrit, all 81 matter rays projectively.  The
    # like-for-like permutation obstruction compares the two 27-point sets.
    operator_center_fixed_internal_rays=27
    operator_center_fixed_matter_rays=81

    # Exact two-qutrit Pauli basis over Q(omega).  The earlier certificate used
    # a floating SVD here even though every entry is cyclotomic.  Work in the
    # Fraction-pair field model a+b*omega, omega^2+omega+1=0, instead.
    def qutrit_pauli(a,b):
        # Z^a X^b |j> = omega^(a(j+b)) |j+b>.
        W=zero_matrix(3,3)
        for j in range(3):
            W[(j+b)%3][j]=omega_power(a*(j+b))
        return W

    paulis=[]
    for aq,bq,ap,bp in itertools.product(range(3),repeat=4):
        W=kronecker(qutrit_pauli(aq,bq),qutrit_pauli(ap,bp))
        paulis.append(W)

    # The exact Hilbert-Schmidt Gram is 9 I_81, which already proves linear
    # independence; exact Gaussian elimination independently returns rank 81.
    gram=[]
    for U in paulis:
        Ud=matrix_dagger(U)
        gram.append([
            sum(
                (Ud[i][j]*V[j][i] for i in range(9) for j in range(9)),
                ZERO,
            )
            for V in paulis
        ])
    assert all(
        gram[i][j]==(9 if i==j else 0)
        for i in range(81) for j in range(81)
    )
    span=[[entry for row in W for entry in row] for W in paulis]
    pauli_span_rank=matrix_rank(span)
    assert pauli_span_rank==81

    out={
      "schema":"w33.address_operator_h27_roles.v1",
      "status":"PASS_ADDRESS_AND_OPERATOR_H27_ROLES_SEPARATED_AND_EXECUTABLE",
      "headline":"The regular/Payne H27 and the center-correct trinification H27 are two different exact roles. The address H27 supplies a simply-transitive 27-address space whose five order-three directions have 45 right cosets forming GQ(2,4); after adding an external C3 with slopes +/-1 these become exactly the 270 lifted E8 cubic instructions. The physical Clifford-648 preserves the 45-line geometry with line orbits 9+36 and, with phase labels held fixed, instruction orbits 27+27+216. The operator H27 instead acts on the E6 27 as nine copies of its 3D Schrodinger irrep, giving C81=C9_mult tensor C3_int tensor C3_ext and Pauli algebra I9 tensor M9 with commutant M9 tensor I9.",
      "address":{
        "H27_order":27,
        "directions":[{"name":n,"generator":list(d)} for n,d in zip(DIRECTION_NAMES,DIRECTIONS)],
        "right_cosets":45,
        "incidence_per_address":5,
        "collinearity_SRG":[27,10,1,5],
        "identified_geometry":"GQ(2,4) / cubic-surface 45 tritangents",
        "complete_frame_isomorphism_anchor":"identity address -> complete frame 0",
        "anchored_incidence_isomorphism_count":len(anchored_isomorphisms),
        "anchored_gauge_scope":"the first of 1920 incidence isomorphisms is chosen deterministically; no canonical root-gauge intertwiner is inferred",
        "lifted_group":"H27 x C3_external",
        "lifted_directions":10,
        "lifted_cosets":270,
        "lift_rule":"five base directions times slopes +1,-1; every lifted triple uses external phases {0,1,2}",
        "equals_45_times_3_factorial_lifted_cubics":True,
        "Clifford648_preserves_45_lines":True,
        "line_orbit_sizes":line_orbit_sizes,
        "phase_fixed_instruction_orbit_sizes":instr_orbit_sizes,
        "center_action_on_27_addresses":"fixed-point-free"
      },
      "operator":{
        "trinification_27":"(3,3bar,1)+(1,3,3bar)+(3bar,1,3)",
        "generators":{"X_int":"(X,X,I)","Z_int":"(Z^2,Z,I)"},
        "chart":"(m,q), m in F3^2, q in F3",
        "X_action":"|m,q> -> |m,q+1>",
        "Z_action":"|m,q> -> omega^q |m,q>",
        "matter_tensor_basis":"C^81 ~= C^9_multiplicity tensor C^3_internal tensor C^3_external",
        "Pauli243_action":"I9 tensor H9(two-qutrit Schrodinger)",
        "two_qutrit_Pauli_span_rank":pauli_span_rank,
        "Pauli_span_field":"Q(omega), omega^2+omega+1=0, exact Fraction pairs",
        "Pauli_Hilbert_Schmidt_Gram":"9 I_81 exactly",
        "generated_algebra":"I9 tensor M9(C)",
        "generated_algebra_dimension":81,
        "commutant":"M9(C) tensor I9",
        "commutant_dimension":81,
        "multiplicity_noiseless_subsystem_dimension":9,
        "center_action_on_basis_rays":"scalar; fixes all 27 internal E6 rays and all 81 matter rays projectively",
        "center_fixed_internal_ray_count":operator_center_fixed_internal_rays,
        "center_fixed_matter_ray_count":operator_center_fixed_matter_rays
      },
      "nonidentification":{
        "same_permutation_action":False,
        "witness":"address center fixes 0 of 27 addresses; operator center is scalar and fixes all 27 internal E6 basis rays projectively",
        "address_role":"combinatorial/coset address space and cubic instruction support",
        "operator_role":"noncommutative operator algebra on two active qutrits with 9D multiplicity subsystem"
      },
      "open_boundary":"An explicit root-gauge intertwiner from the frozen E8 root coordinates to the displayed trinification tensor basis remains open. No family, Yukawa, vacuum, or hardware claim is made.",
      "checks":{
        "five_direction_cosets_are_45_GQ24_lines":True,
        "address_lines_map_exactly_to_45_complete_frame_tritangents":True,
        "anchored_incidence_gauge_has_1920_choices":True,
        "ten_sloped_directions_give_exactly_270_lifted_cubics":True,
        "all_648_preserve_address_line_geometry":True,
        "line_orbits_9_36":True,
        "instruction_orbits_27_27_216":True,
        "operator_chart_exact":True,
        "two_qutrit_paulis_span_M9":True,
        "two_qutrit_pauli_gram_is_exactly_9I81":True,
        "address_operator_centers_have_incompatible_permutation_behavior":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ("status","address","operator","nonidentification")},indent=2))
    return out

if __name__=="__main__": main(True)
