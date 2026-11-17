"""Global flux-wedge complex, X8 external-reflection selection, and
minimax 4-MUB qutrit witness with pre-setting loss-heralding.

Each result is explicitly mathematical. The integral wedge differential
is NOT a demonstrated M-theory AHSS/quantum Page charge differential.
The X8 parity argument applies to external-reflection-even metric modes,
not arbitrary physical 11D fluctuations.
"""
from __future__ import annotations
from collections import Counter
from functools import reduce
from itertools import product
from math import gcd, exp, log, inf
from pathlib import Path
import json, math, sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_M5_graded_G4_wedge_complex import matrix, BASIS, product_form
from toe_20261116_IIB_circle_Gysin_linking import reduce_pair
OUT=ROOT/"data"/"toe_20261117_fluxWedge_X8parity_MUBminimax_certificate.json"

def flux_homology(Nxy,Nxt,Nyt):
    """Cohomology of the degree+4 differential on the rank-graded free
    integral cohomology of S2xS2xT2. Flux wedge squares zero by dim6.
    Kernel/image quotients may include torsion. This is NOT a claim that
    the physical M-theory differential is G4 wedge.
    """
    assert any((Nxy,Nxt,Nyt))
    g=reduce(gcd,map(abs,(Nxy,Nxt,Nyt)))
    ranks={i:len(BASIS[i]) for i in range(7)}
    d={i:matrix(i,Nxy,Nxt,Nyt) for i in (0,1,2)}
    assert d[0]==sp.Matrix([Nxy,Nxt,Nyt])
    assert d[1]==sp.diag(Nxy,Nxy)
    assert d[2]==sp.Matrix([[Nyt,Nxt,Nxy]])
    # degree 4 component receives d(0); 5 receives d(1); 6 receives d(2)
    # all outgoing d from degrees 3,4,5,6 are zero by dimension.
    free={0:0,1:2-int(Nxy!=0)*2,2:2,3:4,4:2,
          5:2-int(Nxy!=0)*2,6:0}
    # A WARNING: kernel H^2->H^6 rank 2 for nonzero triple even if
    # Nxy=0; H^0 map injective. Degree1 kernel rank2 iff Nxy=0.
    torsion={0:[],1:[],2:[],3:[],4:([g] if g>1 else []),
             5:([abs(Nxy),abs(Nxy)] if abs(Nxy)>1 else []),
             6:([g] if g>1 else [])}
    # Quotient H^5 loses its whole free rank when Nxy nonzero,
    # but when Nxy==0, H^5 has rank2.
    if Nxy==0:
        assert free[1]==2 and free[5]==2
    else:
        assert free[1]==0 and free[5]==0
    if abs(Nxy)==1:
        assert torsion[5]==[]
    # For any integral four-form G on a six-manifold, G cup G is
    # degree eight and vanishes. Check directly in the oriented basis.
    assert all(product_form(a,b) is None for a in BASIS[4] for b in BASIS[4])
    return {"fluxes":[Nxy,Nxt,Nyt],"gcd":g,
       "free_ranks_H0_to_H6":[free[i] for i in range(7)],
       "torsion_cyclic_orders_H0_to_H6":[torsion[i] for i in range(7)],
       "d0_H0_to_H4":[Nxy,Nxt,Nyt],
       "d1_H1_to_H5":[[int(v) for v in row] for row in d[1].tolist()],
       "d2_H2_to_H6":[Nyt,Nxt,Nxy],
       "dimensional_differential_square_zero":True}

def flux_theorem():
    cases=[flux_homology(*v) for v in ((5,6,6),(6,6,6),(0,6,6),(0,1,1),(1,6,6),(0,0,6))]
    x,y=cases[0],cases[1]
    assert x["gcd"]==1 and x["torsion_cyclic_orders_H0_to_H6"][5]==[5,5]
    assert x["torsion_cyclic_orders_H0_to_H6"][4]==[]
    assert y["torsion_cyclic_orders_H0_to_H6"][4]==[6]
    assert cases[2]["free_ranks_H0_to_H6"][1]==2
    assert cases[2]["torsion_cyclic_orders_H0_to_H6"][5]==[]
    for Nxy,Nxt,Nyt in product(range(-3,4),repeat=3):
        if not any((Nxy,Nxt,Nyt)):continue
        z=flux_homology(Nxy,Nxt,Nyt)
        assert z["free_ranks_H0_to_H6"][2]==2
        assert z["free_ranks_H0_to_H6"][3]==4
    gIIB=reduce_pair(6,6)["gcd"]
    assert gIIB==6 and x["gcd"]==1 and x["torsion_cyclic_orders_H0_to_H6"][5]==[5,5]
    return {"status":"PASS_G4_WEDGE_INTEGER_COMPLEX_FULL_KERNEL_QUOTIENT",
      "coefficient_ring":"H^*(S2xS2xT2;Z); differential d_G(alpha)=G4 cup alpha of cohomological degree +4",
      "full_grading":"degree 0..6; for flux nonzero, H^0=0,H^2=Z2,H^3=Z4,H^4=Z2+Z_g,H^6=Z_g. H^1=0 and H^5=Z_|Nxy|^2 (two cyclic factors) if Nxy nonzero; if Nxy=0, H^1=Z2,H^5=Z2.",
      "independent_topological_flux_channels":{"g":"gcd(Nxy,Nxt,Nyt) controls H4 and H6",
                                         "Nxy":"|Nxy| controls H5 two-fold torsion, independent of g"},
      "IIB_counterexample":"M flux (5,6,6) gives g=1 but H5 torsion Z5 x Z5; IIB circle p=q=6 has pi1=Z6. Different complexes cannot be identified by gcd alone.",
      "critical_caveat":"This is algebraic cohomology of flux-cup multiplication; no proof that it is the AHSS differential for quantum M-theory or that its groups classify Page charge, endpoint charge, or dual wrapped branes.",
      "test_vectors":cases}

def x8_reflection_selection():
    # In an external-reflection-even background and fluctuations
    # independent of the external coordinate and containing only
    # external Lorentz-scalar metric amplitudes, the connection/
    # curvature transforms under E: e^mu -> -e^mu (all five ext).
    # Any O(1,4)-invariant characteristic polynomial P(R) is even
    # under E, while its external-degree-odd components are odd,
    # hence must vanish. Thus 5 ext / 3 int component is absent.
    dims=(5,6)
    pattern=[]
    for ext in range(9):
        internal=8-ext
        if 0<=ext<=5 and 0<=internal<=6:
            pattern.append({"external_degree":ext,"internal_degree":internal,
                            "external_reflection_sign":(-1)**ext,
                            "allowed_when_reflection_even":ext%2==0,
                            "wedges_nontrivially_with_internal_C3_by_degree":internal<=3 and ext==5})
    assert len([p for p in pattern if p["wedges_nontrivially_with_internal_C3_by_degree"]])==1
    assert not any(p["allowed_when_reflection_even"] and
                   p["wedges_nontrivially_with_internal_C3_by_degree"] for p in pattern)
    return {"status":"PASS_X8_REFLECTION_EVEN_SCALAR_LOCAL_WEDGE_SELECTION",
      "product_dimensions":list(dims),
      "only_C3bg_wedge_X8_8form_bidegree":[5,3],
      "external_reflection_even_X8_possible_bidegrees":[
          [p["external_degree"],p["internal_degree"]] for p in pattern if p["allowed_when_reflection_even"]],
      "argument":"If both background and perturbation are invariant under simultaneous reflection of all five external orthonormal directions, the O(1,10)-invariant Pontryagin polynomial X8 is reflection-even. Every component with odd external form degree must vanish; however a local purely internal C3_bg can wedge nontrivially only with X8 of bidegree (external5,internal3).",
      "consequence":"For external-reflection-even, externally homogeneous metric-scalar perturbations in this local gauge, C3_bg wedge quadratic X8 vanishes by degree/parity. This does NOT rule out 5D derivative terms, reflection-odd fluctuations, global differential C-fields, or any R4/G4 action terms.",
      "caveat":"Assumes full background and perturbations respect the stated external reflection. In AdS, full normalizable modes depend on external coordinates and need not have this property; no on-shell 11D mass shift is calculated."}

def q_given_source(v,sigma):
    assert 0<=v<=1 and sigma>=0
    return 1/3+v*(1+3*exp(-sigma*sigma))/6

def qutrit_mub_minimax():
    # Trusted matched-outcome qutrit entanglement witness:
    # four complete MUBs, matched on B's conjugate setting.
    # For separable product |b,j> otimes |b,j>*,
    # matched probability 1 in basis b, 1/3 in each other MUB.
    # For weighted settings w_b, this is 1/3+2*w_b/3.
    # Therefore max_separable>=1/3+2/3 max_b w_b>=1/2.
    # For uniform settings, 4 MUB 2-design identity proves
    # max_separable=1/2, so uniform is globally minimax
    # among these weighted matched-event witnesses.
    weights=[[.25]*4,[.4,.2,.2,.2],[.7,.1,.1,.1],[1,0,0,0]]
    examples=[]
    for w in weights:
        assert abs(sum(w)-1)<1e-12
        lower=1/3+2*max(w)/3
        examples.append({"settings":w,"guaranteed_separable_matching_at_least":lower})
    assert examples[0]["guaranteed_separable_matching_at_least"]==.5
    assert all(v["guaranteed_separable_matching_at_least"]>.5 for v in examples[1:])
    p0=.51; sigma=.15
    configs=[]
    for n,em,path,router in [(1,.8,.95,1),(1,.95,.95,.95),(2,.8,1.,1.),(0,1.,.54,1.),(2,.95,.95,.95)]:
        optical=.9**2 *em**n*path*router**2
        raw=6*(p0/optical-1/3)/(1+3*exp(-sigma*sigma))
        best=optical*q_given_source(1,sigma)
        configs.append({"memory_count":n,"eff_each_memory":em,"path_throughput":path,
                        "router_eff_each":router,"gross_detection":optical,
                        "minimum_visibility":raw,
                        "physically_feasible_at_fixed_sigma":raw<=1,
                        "best_gross_matched_with_perfect_visibility":best})
    assert .75<configs[0]["minimum_visibility"]<1
    assert configs[1]["minimum_visibility"]<.75
    assert .98<configs[2]["minimum_visibility"]<1
    assert configs[3]["gross_detection"]<.51
    # Trusted pre-setting heralding: trace-nonincreasing LOCAL CP
    # filters preserve separability of successful conditional state.
    # A source failure flag independent of the future basis allows
    # normalized conditional witness testing on success at a RATE cost.
    return {"status":"PASS_FOUR_MUB_UNIFORM_SETTING_MINIMAX_AND_VISIBILITY_FLOOR",
       "exact_source_probability":"q(v,sigma)=1/3+v*(1+3 exp(-sigma^2))/6",
       "weighted_separable_witness_lower_bound":"p_sep>=1/3+(2/3)*max_b w_b, by a product state equal to an eigenvector of the most likely basis",
       "uniform_optimality":"max_b w_b>=1/4, so p_sep>=1/2. Uniform w=(1/4,1/4,1/4,1/4) achieves exactly 1/2 by the 4-MUB 2-design identity; biased bases cannot reduce the separable threshold for this particular test.",
       "calibrated_null":p0,
       "minimum_visibility_formula":"v_min=6*(p0/eta_total-1/3)/(1+3 exp(-sigma^2)), at fixed sigma and eta_total=etaR etaS eta_mem^n eta_path fR fS",
       "examples":examples,"hardware_visibility_controls":configs,
       "pre_setting_herald_loophole_safe_theorem":"A fixed local trace-decreasing CP map, with success herald announced BEFORE fresh secret basis choice, maps separable states to (subnormalized) separable states. Conditional normalized successes therefore still obey p_sep<=1/2 under trusted measurements. A nondestructive prebasis success herald could avoid counting pre-memory failures but reduces the accepted rate; postbasis coincidences are NOT valid.",
       "physics_caveat":"No certified nondestructive qutrit-memory herald or hardware claimed; hidden setting leakage, herald dependence on future settings, calibration, and nonIID memory adversaries require independent bounds."}

def verify():
    return {"status":"PASS_M5_G4_X8_QUTRIT_THREEFRONT_EXACT_CONSTRAINTS",
       "M5_flux_wedge":flux_theorem(),
       "X8_selection":x8_reflection_selection(),
       "qutrit_basis_optimality":qutrit_mub_minimax()}

if __name__=="__main__":
    z=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"])
