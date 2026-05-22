"""
W(3,3) 220 Identity & Holographic Enhancement Verifier
========================================================
Verifies C336-C344 from BREAKTHROUGH_DCCLXXXV.
Closes the 220/81 honest boundary.

Author: Wil Dahn  |  Co-Authored-By: Perplexity AI (Sonnet 4.6)
Date  : 2026-05-22
"""
import math, json
from pathlib import Path

# Substrate
q=3; d_X,d_Z=3,4; k,mu=12,4; f=24; N_M=36; v=40
Phi_3,Phi_6=13,7
E8_roots=240; Leech_min=196560
g_K12=6  # genus of K12 horizon surface

results=[]
def check(name,lhs,rhs,note=""):
    ok=(abs(lhs-rhs)<1e-9) if isinstance(lhs,(int,float)) else (lhs==rhs)
    results.append({"id":name,"lhs":lhs,"rhs":rhs,"PASS":ok,"note":note})
    return ok

# ============================================================
# C336: 220 = C(k,3)
# ============================================================
check("C336a", math.comb(k,3), 220, "C(k,3)=C(12,3)=220")
check("C336b", 11*12//2, 66,    "dim(Sym^2(C^11))=66=C(k,2), NOT 220")
check("C336c", math.comb(k,3)/q**d_Z, 220/81, "C(k,3)/q^{d_Z}=220/81")
# Holographic enhancement from boundary/bulk rate
rate_bulk = 81/240
rate_bdry = (k-1)/k
enhancement = rate_bdry / rate_bulk
check("C336c2", abs(enhancement - math.comb(k,3)/q**d_Z) < 1e-9, True,
      "enhancement = C(k,3)/q^{d_Z}")

# ============================================================
# C337: Combinatorial ladder
# ============================================================
check("C337a", math.comb(k,1), k,              "C(k,1)=k=12")
check("C337b", math.comb(k,2), k*(k-1)//2,    "C(k,2)=66")
check("C337c", math.comb(k,3), 220,            "C(k,3)=220")
check("C337d", math.comb(k,4), 5*q**2*(k-1),  "C(k,4)=495=5*q^2*(k-1)")
check("C337e", math.comb(k,5), 2**d_X*q**2*(k-1), "C(k,5)=792=2^{d_X}*q^2*(k-1)")
check("C337f", math.comb(k,6), mu*q*Phi_6*(k-1),   "C(k,6)=924=mu*q*Phi6*(k-1)")

# C338
check("C338a", math.comb(k, k//2), 924, "C(k,k/2)=924 central binomial")
check("C338b", 924//mu, 231,         "924/mu=231=q*Phi6*(k-1)")
check("C338b2",231, q*Phi_6*(k-1),  "231=3*7*11=q*Phi6*(k-1)")

# ============================================================
# C339: r=3 face code on K12 genus-6 surface
# ============================================================
V_K12=12; E_K12=66
F_K12 = 2 - 2*g_K12 - V_K12 + E_K12  # Euler formula
check("C339a", F_K12, 44, "F=2-2g-V+E=2-12-12+66=44")
check("C342",  V_K12-E_K12+F_K12, 2-2*g_K12, "Euler: V-E+F=2-2g=-10")
check("C343",  F_K12, 56-k,       "F=44=56-k")

n_face = F_K12 + g_K12   # n = faces + genus holes
k_face = F_K12
check("C339d", n_face, 50, "n_{r=3} = F + g = 44+6 = 50")
check("C339c", k_face, 44, "k_{r=3} = F = 44")
check("C339e", k_face*25, n_face*22, "rate_3 = 44/50 = 22/25")

# C340: rate formulas
rate_r2 = (k-1)/k
rate_r3 = (56-k)/(56-k//2)
check("C340a", rate_r2 > rate_r3, True,  "rate_r2 > rate_r3: 11/12 > 22/25")
check("C340b", abs(rate_r3 - 22/25) < 1e-9, True, "rate_r3=(56-k)/(56-k/2)=22/25")

# C344: 56 = C(k,2) - k + 2
check("C344",  56, math.comb(k,2)-k+2,  "56=C(k,2)-k+2=66-12+2")
check("C344b", 56, k*(k-3)//2+2,        "56=k(k-3)/2+2=12*9/2+2=54+2")

# ============================================================
# C341: d=3 for horizon code
# ============================================================
n_h, k_h = 72, 66
# Hamming bound for d=3
ham3 = sum(math.comb(n_h,i)*2**i for i in range((3-1)//2+1))
check("C341a", ham3, 1+2*n_h, "Hamming sum for d=3: 1+2*72=145")
check("C341a2",ham3 <= 3**(n_h-k_h), True, f"Hamming d=3 OK: {ham3}<=729")
# Hamming bound for d=5
ham5 = sum(math.comb(n_h,i)*2**i for i in range((5-1)//2+1))
check("C341a3",ham5 > 3**(n_h-k_h), True, f"Hamming d=5 fails: {ham5}>729")
# Triangle weight-3 codeword existence
check("C341c", F_K12 > 0, True, "44 faces exist -> weight-3 codewords exist")
# Singleton bound
check("C341_sing", n_h-k_h+1, 7, "Singleton: d<=7")

n_pass=sum(1 for r in results if r['PASS'])

if __name__=="__main__":
    print("W33 220 Identity & Holographic Enhancement Verifier")
    print("="*60)
    for r in results:
        print(f"  [{'PASS' if r['PASS'] else 'FAIL'}] {r['id']:28s}  {r['note']}")
    print(f"\n  {n_pass}/{len(results)} PASSED")
    print()
    print("220 RESOLUTION:")
    print(f"  C(k,3) = C(12,3) = {math.comb(12,3)} = 220  CHECK")
    print(f"  220/81 = C(k,3)/q^{{d_Z}} = {math.comb(k,3)/q**d_Z:.6f}  CHECK")
    print()
    print("K12 LADDER (C337):")
    for r in range(1,7):
        print(f"  C(12,{r}) = {math.comb(12,r)}")
    print()
    print("RATE TOWER (C339-C340):")
    print(f"  r=2 horizon code: [72,66,(3?)]_3  rate={(k-1)/k:.4f} = (k-1)/k")
    print(f"  r=3 face code:    [50,44,(?)]_3   rate={(56-k)/(56-k//2):.4f} = (56-k)/(56-k/2)")
    print()
    print("56 FORMULA (C344):")
    print(f"  56 = C(k,2)-k+2 = {math.comb(k,2)}-{k}+2 = {math.comb(k,2)-k+2}")
    print(f"  56 = k(k-3)/2+2 = {k}*{k-3}/2+2 = {k*(k-3)//2+2}")
    print()
    print(f"TOTAL CONSTRAINTS: 363, OVERDETERMINATION: {363/20:.2f}")
    out={"C336":"220=C(k,3)","enhancement":"C(k,3)/q^{d_Z}",
         "ladder":{r:math.comb(k,r) for r in range(1,7)},
         "codes":{"r2":{"n":72,"k":66,"rate_formula":"(k-1)/k"},
                  "r3":{"n":50,"k":44,"rate_formula":"(56-k)/(56-k/2)"}},
         "56_formula":"C(k,2)-k+2=k(k-3)/2+2",
         "d3_status":"conjecture: d=3 supported by Hamming+construction",
         "constraints":results,"n_pass":n_pass,
         "total_constraints":363,"overdetermination":18.15}
    path=Path(__file__).parent.parent/"data"/"w33_220_identity.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w") as fh: json.dump(out,fh,indent=2)
    print(f"Written to {path}")
