"""E6 27+bar27 mirror messenger selection: exact symmetry and no-go.

The actual renormalizable E6 gauge invariant couplings are
M (barF+ F+ + barF- F-) + y A^a
(barF+ T_a F+ - barF- T_a F-)
for two vectorlike 27+bar27 pairs, A in 78.
Mirror Z2 sends + <-> - and A -> -A; the entire coupling is
invariant. With a COMMON soft shift Delta, the complete multiplets
produce a quartic proportional Tr27 A^4, which is only (Tr27 A^2)^2/12.
Hence their one-loop quartic CANNOT select an E6 adjoint direction.

The SU5 quartic selector derived earlier therefore requires split
masses/reps, additional fields/VEVs, higher invariants or other
thresholds. A traditional Z4^R matter=1 Higgs=0 sector allows Yukawas
and Weinberg but forbids QQQL and UUDE, not dimension-six gauge
exchange. This is only modular operator arithmetic: GS anomaly
cancellation and E6 matter/Higgs realization remain unknown.
"""
import json,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_E6_full_cubic_SM_stabilizer import cubic_monomials
OUT=ROOT/"data"/"toe_20261117_E6_mirror_Z4R_quartic_nogo.json"
def cartan():
    mons=cubic_monomials()
    A=s.zeros(len(mons),27)
    for j,(tri,sgn) in enumerate(sorted(mons.items())):
        for ix in tri:A[j,ix]+=1
    b=A.nullspace()
    assert len(b)==6
    t=s.symbols("t0:6")
    h=s.Matrix.hstack(*b)*s.Matrix(t)
    tr2=s.expand(sum(v*v for v in h))
    tr3=s.expand(sum(v**3 for v in h))
    tr4=s.expand(sum(v**4 for v in h))
    tr5=s.expand(sum(v**5 for v in h))
    assert tr3==0
    assert s.expand(12*tr4-tr2**2)==0
    assert tr5!=0
    z,y=s.symbols("z y")
    for n in (1,3,5,7,9):
        assert s.expand((z+y)**n+(z-y)**n).coeff(y,n)==0
    # The cubic background invariant for 27 matter is unrelated to
    # the absent cubic pure adjoint trace.
    return {"exact_45_monomial_constraints":len(mons),
      "Cartan_dimension":len(b),
      "exact_complete_27_quartic_identity":"12 Tr27(H^4)=(Tr27(H^2))^2 for arbitrary six-variable E6 Cartan H",
      "Tr27_cubic_zero":True,
      "Tr27_quintic_nonzero_generic":True,
      "mirror_odd_powers_cancel":True,
      "no_go":"Two COMPLETE E6 27+bar27 mirror messenger pairs, equal M/y/soft Delta across all 27 components, yield a quartic only in [Tr27 H²]^2. No directional 3+2 selection at this order.",
      "escape":"Split multiplet thresholds using E6-breaking VEV, nonuniform soft masses compatible with gauge invariance, additional representations, or degree 5+ adjoint invariants; then calculate full F/D and one-loop operator."}
def operators():
    R={"Q":1,"U":1,"D":1,"L":1,"E":1,"N":1,
       "Hu":0,"Hd":0,"A78":0,"Fp":1,"Fm":1,"barFp":1,"barFm":1,
       "S2":2}
    ops={"up_Yukawa":("Q","U","Hu"),"down_Yukawa":("Q","D","Hd"),
      "lepton_Yukawa":("L","E","Hd"),
      "Weinberg":("L","Hu","L","Hu"),
      "neutrino_Yukawa":("L","N","Hu"),
      "Majorana_N":("N","N"),
      "mu_term":("Hu","Hd"),
      "QQQL":("Q","Q","Q","L"),
      "UUDE":("U","U","D","E"),
      "UDD":("U","D","D"),"LLE":("L","L","E"),
      "LQD":("L","Q","D"),"LH_u":("L","Hu"),
      "mirror_mass_p":("Fp","barFp"),
      "mirror_mass_m":("Fm","barFm"),
      "mirror_Yukawa_p":("Fp","barFp","A78"),
      "mirror_Yukawa_m":("Fm","barFm","A78"),
      "spurion_S2_HuHd":("S2","Hu","Hd")}
    q={key:sum(R[z] for z in v)%4 for key,v in ops.items()}
    allow={k:v==2 for k,v in q.items()}
    for k in ("up_Yukawa","down_Yukawa","lepton_Yukawa","Weinberg",
              "neutrino_Yukawa","Majorana_N","mirror_mass_p",
              "mirror_mass_m","mirror_Yukawa_p","mirror_Yukawa_m"):
        assert allow[k],k
    for k in ("mu_term","QQQL","UUDE","UDD","LLE","LQD","LH_u"):
        assert not allow[k],k
    assert allow["spurion_S2_HuHd"]
    # The Z2 exchange maps (+,A)->(-,-A), so an odd A insertion
    # exchanges sign of Yukawa; ordinary mass term is even.
    mirror={"exchange_Fp_Fm":True,"exchange_barFp_barFm":True,
            "A78_to_minus_A78":True,
            "mass_term_even":True,"opposite_sign_adjoint_Yukawa_even":True,
            "A78_nonzero_VEV_spontaneously_breaks_mirror_Z2":True}
    return {"Z4R_superpotential_charge":2,
            "charges":R,"monomial_charge_mod4":q,
            "allowed_by_Z4R":allow,"mirror_exchange":mirror,
            "proton_scope":"The Z4R forbids local holomorphic dimension-five QQQL and UUDE BEFORE R-breaking. Gauge-boson dimension-six exchange is not forbidden; anomalies, nonperturbative R-breaking, triplet mixing and UV consistency require separate analysis.",
            "potential_Z4R_spurion_issue":"S2 HuHd is allowed, so a charged spurion can reintroduce mu and other prohibited terms when its F/VEV breaks the symmetry.",
            "references":["https://arxiv.org/abs/1009.0905",
                          "https://link.springer.com/article/10.1007/JHEP02%282014%29058"]}
def verify():
    a=cartan();b=operators()
    return {"status":"PASS_E6_MIRROR_Z2_Z4R_OPERATOR_ARITHMETIC_AND_COMPLETE27_QUARTIC_NOGO",
            "group_theory":a,"operator_symmetry":b,
            "not_UV_completion":"The mirror-exchange invariant is concrete at the renormalizable E6 operator level; an exact full SUSY E6 vacuum, anomaly-free symmetry, split spectrum and proton lifetime are not established."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"])
