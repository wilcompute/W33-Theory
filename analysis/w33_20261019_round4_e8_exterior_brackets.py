"""Round 4 front 4: test all three exterior bilinear bracket TYPES
of standard A8 model E8=sl9 + Lambda3 + Lambda6 for 5 two-qutrit
Clifford generators, with explicit epsilon and det=1 phases.

This is generator-level tensor covariance, NOT a map to the repo's
specific 248-dimensional Chevalley coordinates or a Jacobi proof.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from w33_20261019_nextfive_optics_su9 import GENERATORS,rep,phi
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round4_e8_exterior_brackets.json"
triples=list(itertools.combinations(range(9),3))
sixlets=list(itertools.combinations(range(9),6))
sixix={x:i for i,x in enumerate(sixlets)}
def sgn(word):
    return (-1)**sum(word[i]>word[j] for i in range(len(word))
                     for j in range(i+1,len(word)))
D=np.zeros((84,84),complex) # epsilon complement: Lambda6(V)->Lambda3(V*) for det=1
for ix,t in enumerate(triples):
    s=tuple(z for z in range(9) if z not in t)
    D[ix,sixix[s]]=sgn(t+s)
assert np.linalg.norm(D@D.conj().T-np.eye(84))<1e-14
def wedge3(U):
    return np.array([[np.linalg.det(U[np.ix_(a,b)]) for b in triples]
                      for a in triples])
def normalize_SU9(U):
    det=np.linalg.det(U)
    V=U*np.exp(-1j*np.angle(det)/9)
    return V,complex(np.linalg.det(V))
def wedge(a,b):
    out=np.zeros(84,dtype=complex)
    for i,A in enumerate(triples):
        if abs(a[i])<1e-13:continue
        for j,B in enumerate(triples):
            if abs(b[j])<1e-13 or not set(A).isdisjoint(B):continue
            u=A+B
            out[sixix[tuple(sorted(u))]]+=sgn(u)*a[i]*b[j]
    return out
def tensor(v):
    T=np.zeros((9,9,9),complex)
    for i,t in enumerate(triples):
        for perm in itertools.permutations(range(3)):
            seq=[t[j] for j in perm]
            T[tuple(seq)]=sgn(perm)*v[i]
    return T
def mixed(a,b):
    # [alpha,beta] in sl9 via contraction with epsilon-dual covariant trivector
    x=tensor(a)
    y=tensor(D@b)
    M=np.einsum("iab,jab->ij",x,y)/2
    return M-np.trace(M)*np.eye(9)/9
def bracket33(a,b):return wedge(a,b)
def bracket66(a,b):return D@wedge(D@a,D@b)
def run():
    rng=np.random.default_rng(20261019)
    errs={}
    alpha=rng.normal(size=84)+1j*rng.normal(size=84)
    beta=rng.normal(size=84)+1j*rng.normal(size=84)
    gamma=rng.normal(size=84)+1j*rng.normal(size=84)
    delta=rng.normal(size=84)+1j*rng.normal(size=84)
    e33=max(np.linalg.norm(wedge(alpha,beta)+wedge(beta,alpha)),
            np.linalg.norm(wedge(alpha,alpha)))
    e66=np.linalg.norm(bracket66(gamma,delta)+bracket66(delta,gamma))
    for name,U in GENERATORS.items():
        V,det=normalize_SU9(U)
        V3=wedge3(V)
        Vcov3=wedge3(np.linalg.inv(V).T)
        V6=D.T@Vcov3@D
        # Test exterior6 explicit six-minor matrix on random entries.
        selections=[(int(rng.integers(84)),int(rng.integers(84))) for _ in range(16)]
        minor=max(abs(V6[i,j]-np.linalg.det(V[np.ix_(sixlets[i],sixlets[j])]))
                  for i,j in selections)
        alpha2=V3@alpha;beta2=V3@beta
        gamma2=V6@gamma;delta2=V6@delta
        m0=mixed(alpha,gamma);m1=mixed(alpha2,gamma2)
        eb33=float(np.linalg.norm(bracket33(alpha2,beta2)-V6@bracket33(alpha,beta)))
        eb66=float(np.linalg.norm(bracket66(gamma2,delta2)-V3@bracket66(gamma,delta)))
        emix=float(np.linalg.norm(m1-V@m0@np.linalg.inv(V)))
        ealpha=float(np.linalg.norm(V3.conj().T@V3-np.eye(84)))
        ebeta=float(np.linalg.norm(V6.conj().T@V6-np.eye(84)))
        errs[name]={"det_SU9_residual":abs(det-1),"wedge6_minor_max_error":minor,
            "bracket_3_3_to_6_residual":eb33,
            "bracket_6_6_to_3_residual":eb66,
            "bracket_3_6_to_sl9_residual":emix,
            "wedge3_unitary_residual":ealpha,
            "wedge6_unitary_residual":ebeta}
    worst=max(max(x.values()) for x in errs.values())
    checks={
        "SU9_det_and_exterior_compatibility":all(x["det_SU9_residual"]<1e-11
                  and x["wedge6_minor_max_error"]<1e-11 for x in errs.values()),
        "all_three_bilinear_bracket_types_equivariant":worst<1e-9,
        "antisymmetry_3_3":e33<1e-11,
        "antisymmetry_6_6":e66<1e-11,
        "tested_5_distinct_Clifford_generators":len(errs)==5}
    out={"schema":"w33.round4.e8_exterior_bracket_covariance.v1",
      "model":"standard complex A8 E8 vector space sl9+Lambda3(V)+Lambda6(V), not a repository Chevalley-basis map",
      "generators_tested":list(errs),
      "phase_handling":"Each U(9) gate rephased to determinant 1; a central cubic root-of-unity acts trivially on sl9 and Lambda3/Lambda6 in 248.",
      "brackets_tested":["Lambda3 wedge Lambda3 -> Lambda6",
                         "Lambda6 epsilon dual wedge Lambda6 epsilon dual -> Lambda3",
                         "Lambda3 epsilon contraction Lambda6 -> sl9"],
      "mixed_map":"Use beta_dual^(j a b) = epsilon^(j a b ... six) beta_six, then M^i_j=(1/2)sum_ab alpha^(i a b) beta_dual_(j a b) minus trace/9",
      "exact_scope":"Generator-level numerical equivariance of three bilinear maps and determinant-one epsilon duality. NOT full E8 Jacobi constants, Chevalley-coordinate equivalence, real-form identification or physical gauge action.",
      "errors_by_generator":errs,"worst_numerical_error":worst,
      "antisymmetry_residuals":{"3_3":e33,"6_6":e66},
      "prior_art":"Vinberg E8 trivector model, J. Baez September 2026 E8 9D trivectors; W33 repository temporal_SU9_E8_compiler already has the standard 80+84+84.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"worst_residual":worst,
                      "by_generator":errs},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
