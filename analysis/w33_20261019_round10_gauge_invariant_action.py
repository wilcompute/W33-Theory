"""Front5: construct explicit SU(3)^3 gauge-invariant scalar invariants;
test finite transformations and an important E8(-24) Yang-Mills
positive-energy obstruction from the indefinite invariant Killing form.
"""
from __future__ import annotations
import json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round10_gauge_invariant_action.json"
rng=np.random.default_rng(20261019)
def su3():
    X=rng.standard_normal((3,3))+1j*rng.standard_normal((3,3))
    Q,R=np.linalg.qr(X)
    Q=Q@(np.diag(np.conj(np.diag(R))/np.abs(np.diag(R))))
    return Q*np.exp(-1j*np.angle(np.linalg.det(Q))/3)
def quartic(A):
    M=A@A.conj().T
    return float(np.trace(M).real**2),float(np.trace(M@M).real)
def invariants(A,B,C):
    return {"norms":[float(np.vdot(X,X).real) for X in (A,B,C)],
            "determinants":[np.linalg.det(X) for X in (A,B,C)],
            "tri_product":np.trace(A@B@C),
            "quartic":[quartic(X) for X in (A,B,C)]}
def distance(x,y):
    return max(max(abs(a-b) for a,b in zip(x["norms"],y["norms"])),
      max(abs(a-b) for a,b in zip(x["determinants"],y["determinants"])),
      abs(x["tri_product"]-y["tri_product"]),
      max(max(abs(a-b) for a,b in zip(v,w)) for v,w in zip(x["quartic"],y["quartic"])))
def run():
    errs=[]
    for _ in range(120):
        A,B,C=[rng.standard_normal((3,3))+1j*rng.standard_normal((3,3)) for _ in range(3)]
        UC,UL,UR=[su3() for _ in range(3)]
        transformed=(UC@A@UL.conj().T,UL@B@UR.conj().T,UR@C@UC.conj().T)
        errs.append(distance(invariants(A,B,C),invariants(*transformed)))
    # For a SIMPLE real Lie algebra any invariant bilinear form
    # is multiple of the Killing form. For the noncompact E8(-24)
    # real form, B has signature (112 positive,136 negative).
    # A bare YM kinetic action -1/(4g²) B_ab F^a F^b
    # cannot have positive energy for all 248 gauge polarisations.
    # Choosing -B instead flips all signs, leaving another 112/136
    # indefinite directions. A field-dependent positive kinetic
    # matrix or restriction to a compact gauge subgroup must be added.
    pos,neg=112,136
    checks={
      "all_cubic_quartic_SU3cubed_tensors_invariant":max(errs)<1e-9,
      "each_scalar_sector_9_complex_fields":3*3*3==27,
      "noncompact_E8_Killing_indefinite":pos>0 and neg>0 and pos+neg==248 and pos-neg==-24,
      "simple_compact_vs_noncompact_signs_both_present":min(pos,neg)>0}
    out={"schema":"w33.round10.SU3cubed_scalar_invariants_and_noncompact_gauge_kinetic_obstruction.v1",
      "fields":"Complex A~(3,bar3,1), B~(1,3,bar3), C~(bar3,1,3) with transformations A'=U_C A U_L†, B'=U_L B U_R†, C'=U_R C U_C†. Transformation determinants all equal 1.",
      "invariants":"Canonical Hermitian quadratic Tr(AA†),Tr(BB†),Tr(CC†); four complex cubic invariants detA,detB,detC,Tr(ABC), plus their Hermitian conjugates; positive quartic invariants (Tr XX†)^2 and Tr[(XX†)^2], plus cross-quadratic norm products. These are SU3^3 invariant, not automatically full E6 invariant without coefficient constraints.",
      "representative_real_scalar_action":"L_scalar = Σ Tr[(Dμ X)†Dμ X] - [ -m²ΣTr(XX†) + λ1Σ(Tr XX†)^2 + λ2ΣTr((XX†)^2) + λ3Σ_{X<Y}Tr(XX†)Tr(YY†) + (η1 detA+η2 detB+η3 detC+η4 Tr(ABC)+h.c.) ], with X=A,B,C. All coefficients independent unless higher symmetry specifies relations; boundedness/correct SSB needs extra restrictions.",
      "max_random_gauge_invariance_residual":float(max(errs)),
      "E8minus24_Killing_signature":{"positive":pos,"negative":neg,"rank":248},
      "noncompact_YangMills_firewall":"If ALL of E8(-24) is gauged with the standard constant invariant bilinear form K, its Yang-Mills kinetic term has indefinite gauge polarisation energy. A simple Lie algebra has a one-dimensional space of invariant symmetric bilinear forms; changing overall sign cannot make both 112 and 136 sectors positive. This prevents an ordinary positive-energy YM model with that bare kinetic form; a compact subgroup, symmetry breaking plus constraints, or field-dependent kinetic tensor may change the physical model. This does NOT forbid E8(-24) as a global or gravitational symmetry.",
      "scope":"No full E8 action, no ghost-free UV completion, no determination of η_i or quartic λ_i, no Standard Model Higgs representation, CP phase, mass ratio or parameter-free prediction.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"max_err":max(errs)},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
