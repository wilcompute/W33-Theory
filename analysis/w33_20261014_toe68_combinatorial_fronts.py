"""TOE68: native W33 disorder, symmetry-equivariant pairings, and zero-mode lifting.

Uses frozen TOE65 native winding-cycles and TOE67 canonical Levi graph.
Exact integer/symbolic statements are separated from numerical diagnostics.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import json,sys,math
import numpy as np
from scipy.optimize import linear_sum_assignment

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1081_1086_core import build_w33, transvection_perm, line_perm
from w33_20261013_toe65_edge_product_adversary import C,W,SGN
from w33_20261014_toe67_continuous_all_beta_determinant import native_three_chords

BITS=(30,31,49,51,59,62,63,82,83,93,95,118,119,138,139,142,143)
Q=np.array([0,-1,1],dtype=int)

def disorder_corner():
    assert C.shape==(238,160) and W.shape==(238,3)
    bits=np.zeros(160,dtype=int);bits[list(BITS)]=1
    coeff=SGN*(W@Q)**2
    high=(C@bits).astype(int)
    d,n=1000,245
    def ray(bits):
        hs=(C@bits).astype(int)
        return sum(int(coeff[i])*(d+n)**int(h)*(d-n)**(8-int(h))
                   for i,h in enumerate(hs))
    base=ray(bits)
    assert base<0
    improvements=[]
    for j in range(160):
        other=bits.copy();other[j]^=1
        improvements.append(ray(other)-base)
    assert all(x>0 for x in improvements)
    polynomial=[sum(int(coeff[i]) for i,h in enumerate(high) if h==k)
                for k in range(9)]
    assert polynomial==[0,0,72,46,34,0,0,0,-12]
    return dict(status="EXACT_ONE_FLIP_LOCAL_MINIMUM_AT_245_PERMILLE",
       tested_edge_flips=160,all_flips_strictly_increase_rayleigh=True,
       native_high_edges=list(BITS),phase_direction=Q.tolist(),
       rayleigh_numerator=base,min_positive_flip_numerator=min(improvements),
       polynomial_coefficient_by_high_count=polynomial,
       epsilon_fraction="245/1000",
       scope="A strict single-bit local minimizer of one chosen Hessian Rayleigh quotient, not a global edge-corner minimum, optimal disorder threshold or all-beta instability theorem.")

def pairs(neighbors):
    a,b,c,d=sorted(neighbors)
    return {frozenset((frozenset((x,y)),frozenset((z,w))))
            for x,y,z,w in ((a,b,c,d),(a,c,b,d),(a,d,b,c))}

def matching_and_bundle():
    pts,ix,lines,li,point_lines,*rest=build_w33()
    flags=[(p,l) for p in range(40) for l in point_lines[p]]
    assert len(flags)==160
    fi={v:i for i,v in enumerate(flags)}
    B=np.zeros((40,40),dtype=int)
    for p,l in flags:B[p,l]=1
    a,b=linear_sum_assignment(-B)
    matching=[fi[(int(p),int(l))] for p,l in zip(a,b)]
    assert len(matching)==40 and all(B[p,l]==1 for p,l in zip(a,b))
    _,selected=native_three_chords()
    assert selected==(59,93,139)
    sign=(-1)**sum(b[i]>b[j] for i in range(40) for j in range(i+1,40))
    for j in matching:
        if j in selected:sign*=-1
    assert abs(sign)==1
    numerical={}
    for t in (1.,1.0001,1.001,1.01):
        A=B.astype(complex)
        for j in selected:
            p,l=flags[j];A[p,l]=-1
        for j in matching:
            p,l=flags[j];A[p,l]*=t
        s=np.linalg.svd(A,compute_uv=False)
        numerical[str(t)]=float(s[-1])
    assert numerical["1.0"]<1e-11
    assert all(numerical[str(t)]>1e-10 for t in (1.0001,1.001,1.01))
    # det(B(t)) has degree 40 with leading coefficient +/-1. It has
    # finitely many roots and hence is nonzero for generic t arbitrarily
    # near 1. This removes 24 zero one-particle energies at pi.
    neighbors={p:{40+l for l in point_lines[p]} for p in range(40)}
    neighbors.update({40+l:set(line) for l,line in enumerate(lines)})
    bundles={x:pairs(neighbors[x]) for x in range(80)}
    assert all(len(q)==3 for q in bundles.values())
    ncheck=0
    for center in (0,1,4,5,13):
        g=transvection_perm(pts[center],pts,ix)
        gp=line_perm(g,lines,li)
        nodeperm={v:g[v] if v<40 else 40+gp[v-40] for v in range(80)}
        for v in range(80):
            images={frozenset(frozenset(nodeperm[x] for x in pair) for pair in pairing)
                    for pairing in bundles[v]}
            assert images==bundles[nodeperm[v]]
            ncheck+=1
    g=transvection_perm(pts[4],pts,ix)
    gp=line_perm(g,lines,li)
    assert g[0]==0
    assert all(frozenset(frozenset(40+gp[a-40] for a in pair) for pair in pairing)!=pairing
               for pairing in bundles[0])
    return {
      "zero_mode_lifting":{
         "status":"EXACT_PERFECT_MATCHING_POLYNOMIAL_FULL_RANK",
         "matching_40_edge_indices":matching,
         "determinant_polynomial_degree":40,
         "leading_integer_coefficient":int(sign),
         "smallest_singular_values_at_pi":numerical,
         "theorem":"The determinant of a 40-edge matching-rescaled B_pi(t) has top coefficient +/-1, hence is not identically zero. Arbitrarily small generic positive changes t>1 break all exact free zero modes, giving a unique canonical half-filled free Fock ground state at fixed pi.",
         "scope":"Does not prove simultaneous all-temperature flux selection or a dynamical many-body interaction gap."},
      "symmetry_bundle":{
         "status":"EXACT_AUTOMORPHISM_EQUIVARIANT_PAIRING_BUNDLE",
         "Levi_vertices":80,"local_degree":4,"opposite_pairings_per_vertex":3,
         "automorphism_checks":ncheck,
         "full_group_invariant_single_ribbon_selection":False,
         "three_pairing_set_is_equivariant":True,
         "theorem":"At each degree-four vertex the unordered three opposite pairings are a canonical automorphism-equivariant fiber; the point-fixing order-three transvection permutes that fiber with no fixed pairing.",
         "scope":"Symmetric family rather than an actual manifold, unique ribbon, metric, or Einstein constraint algebra."}}
def certificate():
    return {"status":"PASS_TOE68_COMBINATORIAL_FRONTS",
       "native_edge_disorder":disorder_corner(),
       **matching_and_bundle()}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe68_combinatorial.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],c["native_edge_disorder"]["rayleigh_numerator"])
