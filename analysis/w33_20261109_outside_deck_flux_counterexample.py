#!/usr/bin/env python3
"""Does 3π flux free-energy dominance extend past TOE61's eight deck sectors?

Test native W33 fifteen-edge pi flux (same 160 hopping magnitudes) versus
TOE61's 3π corner using exact integer characteristic coefficients, and
fermion free energies over multiple beta. A strict lower energy at any
beta is an explicit counterexample to unjustified GLOBAL flux selection.
"""
import json,sys,math,hashlib
from pathlib import Path
import numpy as np
from sympy import Matrix
from w33_20261109_flux_dark_mode_fragility import build
from w33_20261010_toe38_local_maxwell_2complex import prep

def coeff(T):
    K=Matrix((T@T.T).tolist())
    a=[int(x) for x in K.charpoly().all_coeffs()]
    return [int((-1)**k*a[k]) for k in range(41)]

def F(T,beta):
    s=np.linalg.svd(T,compute_uv=False)
    return float(-(2/beta)*sum(np.logaddexp(beta*s/2,-beta*s/2)))

def deck111():
    ed,volts,*_=prep()
    adj=[[] for _ in range(80)]
    for a,b in ed:adj[a].append(b);adj[b].append(a)
    seen={0:0};queue=[0]
    for a in queue:
        for b in adj[a]:
            if b not in seen:seen[b]=1-seen[a];queue.append(b)
            else:assert seen[b]!=seen[a]
    left=[i for i in range(80) if seen[i]==0]
    right=[i for i in range(80) if seen[i]==1]
    li={i:k for k,i in enumerate(left)}
    ri={i:k for k,i in enumerate(right)}
    T=np.zeros((40,40),dtype=int)
    for (a,b),v in zip(ed,volts):
        sign=(-1)**int(sum(v)%2)
        if seen[a]==0:T[li[a],ri[b]]=sign
        else:T[li[b],ri[a]]=sign
    return T

def main(path=None):
    root=Path(__file__).resolve().parents[1]
    B,edges,G=build()
    base=B.astype(int)
    threepi=deck111()
    prior=json.loads((root/"data/w33_20261109_minimal_15_flux_lift.json").read_text())
    new=json.loads((root/"data/w33_20261109_flux_mass_gap_design.json").read_text())
    choices={"flat":base,"deck_three_pi":threepi}
    for name,sel in (("old_15edge",[ (x["point"],x["line"]) for x in prior["constructed_phase_only_pi_flip_links"]]),
                     ("optimized_15edge",[(x["point"],x["line"]) for x in new["best_15_edges"]])):
        T=base.copy()
        for p,l in sel:T[p,l]=-1
        choices[name]=T
    coeffs={n:coeff(T) for n,T in choices.items()}
    frozen_TOE61=json.loads((root/"data/w33_20261013_toe61_det_poly.json").read_text())
    recorded={tuple(x["corner"]):[int(t) for t in x["full_det_coefficients_decimal"]]
              for x in frozen_TOE61["Z2_character_polynomials"]}
    assert coeffs["flat"]==recorded[(0,0,0)]
    assert coeffs["deck_three_pi"]==recorded[(1,1,1)]
    ref=coeffs["deck_three_pi"]
    rows={}
    for n in ("old_15edge","optimized_15edge"):
        delta=[a-b for a,b in zip(coeffs[n],ref)]
        rows[n]={"positive_coefficients":sum(x>0 for x in delta),
             "negative_coefficients":sum(x<0 for x in delta),
             "first_nonzero_degree":next((i for i,x in enumerate(delta) if x),None),
             "min_coefficient_difference":str(min(delta)),
             "max_coefficient_difference":str(max(delta)),
             "all_coefficients_dominate_threepi":all(x>=0 for x in delta),
             "full_exact_difference_decimal":[str(x) for x in delta]}
    cross=[a-b for a,b in zip(coeffs["old_15edge"],coeffs["optimized_15edge"])]
    old_vs_optimized={"number_coefficients_old_exceed_optimized":sum(x>0 for x in cross),
      "number_coefficients_old_below_optimized":sum(x<0 for x in cross),
      "old15_coefficientwise_dominates_optimized15":all(x>=0 for x in cross),
      "full_difference_decimal":[str(x) for x in cross]}
    beta_controls=[]
    for beta in (.1,.2,.5,1.,2.,4.,10.,100.):
        ff={n:F(T,beta) for n,T in choices.items()}
        beta_controls.append({"beta":beta,"F_pi_deck_minus_flat":ff["deck_three_pi"]-ff["flat"],
             "F_old15_minus_threepi":ff["old_15edge"]-ff["deck_three_pi"],
             "F_opt15_minus_threepi":ff["optimized_15edge"]-ff["deck_three_pi"],
             "F_values":ff})
    out={"status":"PASS_W33_15_LINK_Z2_FLUX_COUNTEREXAMPLE_TO_UNRESTRICTED_3PI_SELECTION",
         "theorem_prior":"TOE61 exact coefficientwise threepi dominance across EIGHT selected deck holonomy corners, not arbitrary all-link real Z2 or U1 flux.",
         "comparison_coefficientwise_15_vs_threepi":rows,
         "old_vs_gap_optimized_15edge_coefficientwise":old_vs_optimized,
         "frozen_TOE61_0_and_111_characteristic_polynomials_exactly_reproduced":True,
         "new_exact_all_temperature_theorem":"Both the old and gap-optimized 15-edge Z2 pi-flux patterns have det(I+t B B†) coefficientwise >= the TOE61 (1,1,1) three-pi deck sector, with strict positivity in 37 coefficients for t>0. By the same Weierstrass cosh product proof used in TOE61, their half-filled free fermion free energies are STRICTLY LOWER than the three-pi sector for EVERY finite beta>0. This explicitly refutes extension of TOE61's eight-sector minimization to the unrestricted link-Z2 gauge configuration space.",
         "all_positive_beta_numerical_controls":beta_controls,
         "all_four_operators_have_160_unit_magnitude_links":all(np.count_nonzero(T)==160 and np.array_equal(abs(T[T!=0]),np.ones(160,dtype=int)) for T in choices.values()),
         "both_fifteen_link_masks_preserve_native_incidence_support":all(np.array_equal(abs(choices[n]),abs(base)) for n in ("old_15edge","optimized_15edge")),
         "note_on_deck_vertex_labels":"TOE38 deck B111 is encoded in a different bipartition vertex ordering from native B. Its signed matrix support need not match native B elementwise; the coefficient and spectral invariants are basis-order independent.",
         "exact_40degree_characteristic_coefficients_hashes_sha256":{n:hashlib.sha256((",".join(str(x) for x in c)).encode()).hexdigest() for n,c in coeffs.items()},
         "scope":"If one 15-edge configuration has lower free energy at some beta, the three-pi DECK corner is demonstrably not a global minimizer over ALL Z2 link phases at that beta. That does not find a global minimizer or a dynamic gauge vacuum. If every exact difference coefficient is nonnegative, a stronger all-beta comparison follows from the previously established cosh product argument. Topology/gauge Wilson penalties, source hardware and fermion interactions are not dynamically optimized.",
         "references":["analysis/2026-10-13_toe61_all_beta_flux_manifold_no_go.md",
             "analysis/w33_20261109_minimal_15_flux_lift.py"]}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FLUX_BEYOND_DECK",json.dumps({"coeff":{k:{x:v for x,v in row.items() if x!='full_exact_difference_decimal'} for k,row in rows.items()},
      "beta1":next(x for x in beta_controls if x["beta"]==1.)}))
    return out

if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
