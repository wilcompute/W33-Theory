#!/usr/bin/env python3
"""Pass 1035: complex determinant becomes the S3 standard phase detector."""
from __future__ import annotations

import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1035_determinant_to_s3_realification.json"

ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
W = (Fraction(0), Fraction(1))
W2 = (Fraction(-1), Fraction(-1))


def eadd(x, y): return (x[0] + y[0], x[1] + y[1])
def escale(c, x): return (c * x[0], c * x[1])
def emul(x, y):
    a,b=x; c,d=y
    return (a*c-b*d, a*d+b*c-b*d)
def econj(x): return (x[0]-x[1], -x[1])
def estr(x):
    if x == ZERO: return "0"
    if x == ONE: return "1"
    if x == W: return "omega"
    if x == W2: return "omega^2"
    return f"({x[0]})+({x[1]})*omega"

def compose(p,q): return tuple(p[q[i]] for i in range(3))
def inverse(p):
    out=[0,0,0]
    for i,j in enumerate(p): out[j]=i
    return tuple(out)
def parity(p): return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2
def cycle_type(p):
    fixed=sum(p[i]==i for i in range(3))
    return "identity" if fixed==3 else "transposition" if fixed==1 else "three_cycle"


def main():
    detector=json.loads((DATA/"w33_pass1031_complex_determinant_phase_detector.json").read_text())
    fusion=json.loads((DATA/"w33_pass1032_selector_orbital_fusion_shadow.json").read_text())
    algebra=json.loads((DATA/"w33_pass1033_selector_orbital_algebra.json").read_text())
    S3=[tuple(p) for p in permutations(range(3))]
    identity=(0,1,2); rotation=(1,2,0); rotation2=compose(rotation,rotation)
    C3={identity,rotation,rotation2}
    chi={identity:ONE,rotation:W,rotation2:W2}
    chibar={g:econj(v) for g,v in chi.items()}
    induced={}
    for g in S3:
        total=ZERO
        for x in S3:
            conjugate=compose(inverse(x),compose(g,x))
            if conjugate in C3: total=eadd(total,chi[conjugate])
        induced[g]=escale(Fraction(1,3),total)
    induced_by_class={}
    for name in ["identity","transposition","three_cycle"]:
        values={induced[g] for g in S3 if cycle_type(g)==name}
        assert len(values)==1
        induced_by_class[name]=values.pop()
    standard={g:Fraction(sum(g[i]==i for i in range(3))-1) for g in S3}
    inner=ZERO
    for g in S3: inner=eadd(inner,emul(induced[g],econj(induced[g])))
    inner=escale(Fraction(1,6),inner)
    trivial={g:1 for g in S3}; sign={g:-1 if parity(g) else 1 for g in S3}
    one_dim_restrictions_trivial=all(trivial[g]==1 and sign[g]==1 for g in C3)
    reflection=next(g for g in S3 if cycle_type(g)=="transposition")
    inversion_exchange=all(chi[compose(inverse(reflection),compose(g,reflection))]==chibar[g] for g in C3)
    restriction_match=all(eadd(chi[g],chibar[g])==(standard[g],Fraction(0)) for g in C3)
    expected={"identity":(Fraction(2),Fraction(0)),"transposition":ZERO,"three_cycle":(Fraction(-1),Fraction(0))}
    checks={
        "source_determinant_certificate_passes":detector["status"]=="PASS",
        "source_fusion_certificate_passes":fusion["status"]=="PASS",
        "source_orbital_algebra_passes":algebra["status"]=="PASS",
        "S3_has_order_six":len(S3)==6,
        "C3_is_normal_order_three":len(C3)==3 and all(compose(inverse(x),compose(g,x)) in C3 for x in S3 for g in C3),
        "omega_satisfies_cyclotomic_relation":eadd(eadd(ONE,W),W2)==ZERO,
        "determinant_character_is_nontrivial_C3_character":set(chi.values())=={ONE,W,W2},
        "inversion_exchanges_chi_and_conjugate":inversion_exchange,
        "nontrivial_C3_character_has_no_1d_S3_extension":one_dim_restrictions_trivial,
        "induced_character_values_are_2_0_minus1":induced_by_class==expected,
        "induced_character_equals_standard_character":all(induced[g]==(standard[g],Fraction(0)) for g in S3),
        "induced_character_is_irreducible":inner==ONE,
        "standard_restricts_to_chi_plus_conjugate":restriction_match,
        "same_fibre_fusion_is_conjugate_pair":fusion["fusion_shadow"]["blocks"][1]==[1,1],
        "transport_fusion_is_conjugate_pair":fusion["fusion_shadow"]["blocks"][4]==[27,27],
        "selector_scheme_has_rank_five":len(algebra["relation_order"])==5,
    }
    if not all(checks.values()): raise AssertionError([k for k,v in checks.items() if not v])
    result={
        "schema":"w33.pass1035.determinant_to_s3_realification.python.v1","status":"PASS",
        "headline":"The complex determinant is the oriented C3 phase character. Under selector S3 inversion it is exchanged with its conjugate and cannot remain scalar. Its unique S3 completion is the irreducible two-dimensional standard representation, explaining 1+1->2 and 27+27->54.",
        "complex_phase_character":{"group":"C3","values":["1","omega","omega^2"],"source":"det_C on Z3 x Sp(4,3)","kernel":"Sp(4,3)","sign_blind":True},
        "s3_completion":{"one_dimensional_extension_exists":False,"reason":"S3_ab = C2, so every scalar character is trivial on C3","induced_character_by_class":{k:estr(v) for k,v in induced_by_class.items()},"irreducible_dimension":2,"representation":"standard real/quadrature representation of S3","restriction":"standard|C3 = chi + conjugate(chi)"},
        "fusion_interpretation":{"same_fibre":"omega and omega^2 directions fuse: 1+1=2","skew_transport":"two conjugate 27-orbitals fuse: 27+27=54","preserved_relations":"diagonal, one 27-orbital, and the 36-orbital"},
        "experimental_consequence":"A scalar intensity measurement cannot retain determinant phase under S3 inversion. The detector must preserve two real quadratures.",
        "checks":checks,"check_count":len(checks),
        "boundary":"This does not identify the Pass-1034 correction-exchange character with chirality or any global determinant character."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("Pass1035 PASS")


if __name__=="__main__": main()
