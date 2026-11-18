"""Audit AdS dimension of the conditional winding dispersion and correct
BF-correction windows. The repo's D9 IIB conifold-dual source derives the
lambda-2-sqrt(4+16lambda) branch for an AdS5/type-IIB system;
-4 is NOT the scalar BF threshold for AdS4.

The AdS4 arithmetic below is a FORMAL mass-formula transplant only,
NOT a physical AdS4 KK or flux spectrum.
"""
import math,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
lam,c=s.symbols("lam c",real=True)
m=lam-2-s.sqrt(4+16*lam)

def analysis(D,cval,r=1.0,y=1000.):
    B=s.Rational((D-1)**2,4) # stability is m>= -B
    max_def=s.Rational(25,4)-B
    assert max_def>0 and 0<=cval<float(max_def)
    C=s.Rational(str(cval))
    W=s.Rational(25,4)-B-C
    lo=s.simplify(10-B-C-4*s.sqrt(W))
    hi=s.simplify(10-B-C+4*s.sqrt(W))
    assert hi>lo
    vlo=max(0,float(lo));vhi=float(hi)
    scale=3*math.pi*r/y
    n=sum(2 for u in range(1,int(math.sqrt(vhi/scale))+2)
          if vlo<scale*u*u<vhi)
    return dict(AdS_dimension=D,scalar_BF_bound=str(-B),
       correction_budget=cval,
       maximum_deficit=str(max_def),
       formal_lambda_lower=str(lo),
       formal_lambda_upper=str(hi),
       physically_allowed_lambda_min=0,
       oriented_unstable_horizontal_winding_count_at_y=y and n,
       exact_mass_formula_transferred_only_formally_to_different_D=D!=5)

def run():
    assert s.simplify(m.subs(lam,0))==-4
    assert s.simplify(m.subs(lam,s.Rational(15,4)))==-s.Rational(25,4)
    assert s.simplify(m.subs(lam,12))==-4
    assert s.simplify(m.subs(lam,s.Rational(63,4)))==-s.Rational(9,4)
    # Original IIB/AdS5 threshold -4: 0<lambda<12
    # Hypothetical AdS4 threshold -9/4: 0<=lambda<63/4
    cases=[analysis(D,v) for D,values in
           ((5,(0,1,2)),(4,(0,1,2,3))) for v in values]
    a={(p["AdS_dimension"],p["correction_budget"]):p for p in cases}
    assert a[5,0]["formal_lambda_lower"]=="0"
    assert a[5,0]["formal_lambda_upper"]=="12"
    assert a[4,0]["formal_lambda_lower"]=="-1/4"
    assert a[4,0]["formal_lambda_upper"]=="63/4"
    assert a[4,1]["oriented_unstable_horizontal_winding_count_at_y"] >= a[5,1]["oriented_unstable_horizontal_winding_count_at_y"]
    out=dict(status="PASS",true_scalar_BF_bounds={"AdS4":"-9/4","AdS5":"-4","AdS7":"-9"},
        original_correct_IIB_mode_dimension=5,
        report_misattributions=["analysis/2026-11-18_W33_dual_parabolics_H27_E6_gamma_GS_Hodge_BF_memory.md:115",
        "analysis/2026-11-18_sixfront_H27_min7ancilla_two_wire_E6_EFT_BF_multitime_commoncone.md:59"],
        source="analysis/2026-11-16_D9_iib_conifold_dual.md, section The finite-momentum instability lies in a winding sector; this is an 11D-on-T2 dual of TYPE IIB AdS5 x Tpq, not an independent 11D AdS4 spectrum.",
        BF_general="for scalar m^2 L^2 >= -(D-1)^2/4 in AdS_D",
        assumed_dispersion="m_minus^2 L^2=lambda-2-sqrt(4+16lambda)",
        dispersion_min_lambda="15/4",dispersion_min_mass="-25/4",
        exact_correction_window="V=25/4-(D-1)^2/4-c; lambda_±=10-(D-1)^2/4-c±4 sqrt(V); intersect with lambda>=0; c<25/4-(D-1)^2/4; robust modes if lambda in open window.",
        corrected_AdS4_formal_interval_at_c0="[0,63/4), compared to actual AdS5 (0,12); in AdS4 the assumed lambda=0 mass -4 is already below -9/4",
        cases=cases,
        warning="DO NOT use formal AdS4 recomputed roots as M-theory instability. The spectrum, field content, AdS radius normalization, fermion/boson mixing, flux and dimension must be rederived. Correct the two cited wording errors in future reports, but leave others' historical commit files intact.",
        primary_physics_reference="Gubser and Mitra, Some interesting violations of the Breitenlohner-Freedman bound (2002) arXiv:hep-th/0108239, studies AdS5 x Tpq; BF scalar formula in dimension D.")
    f=ROOT/"data/toe_20261118_AdS_dimension_BF_provenance_falsifier.json"
    f.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS provenance: actual source AdS5, BF5=-4 BF4=-9/4; AdS4 formal cutoff63/4; dimensional transfer is NOT physical")
    print("COUNTS",[(t["AdS_dimension"],t["correction_budget"],t["oriented_unstable_horizontal_winding_count_at_y"]) for t in cases])
    return out
if __name__=="__main__":run()
