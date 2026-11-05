#!/usr/bin/env python3
"""TOE front A: exact Abelian-charge obstruction to protecting scalar PQ.

Gauge/other Abelian selection laws compatible with the following
renormalizable seesaw operators:
   S N_e N_e,  T N_e N_mu, N_mu N_mu (bare).
They NECESSARILY permit S^dagger T^2 under every additive Abelian
selection rule, continuous or finite. Replacing the bare N_mu mass by
R N_mu N_mu NECESSARILY permits S^dagger T^2 R^dagger.
This is a CONDITIONAL operator-identity theorem, not a no-go for
all axion constructions, non-Abelian flavor or changed neutrino textures.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_abelian_seesaw_pq_operator_no_go.json"
def theorem():
    e,m=sp.symbols("e m",integer=True)
    s=-2*e;t=-(e+m);r=-2*m
    cubic=sp.expand(-s+2*t)
    quartic=sp.expand(-s+2*t-r)
    assert cubic==-2*m
    assert quartic==0
    return {"N_e":str(e),"N_mu":str(m),"S":str(s),"T":str(t),
            "possible_replacement_R":str(r),
            "cubic_charge":str(cubic),"quartic_with_Rdag_charge":str(quartic)}
def exhaustive_mod():
    counts={}
    for n in range(2,51):
        with_bare=without_bare=0
        for e,m in itertools.product(range(n),repeat=2):
            S=(-2*e)%n;T=(-e-m)%n;R=(-2*m)%n
            assert (S+2*e)%n ==(T+e+m)%n==(R+2*m)%n==0
            assert (-S+2*T-R)%n==0
            without_bare+=1
            if 2*m%n==0:
                with_bare+=1
                assert (-S+2*T)%n==0
        assert with_bare==n*math.gcd(n,2)
        counts[str(n)]={"charge_pairs_checked":n*n,
            "bare_mass_compatible_pairs":with_bare,
            "cubic_allowed_when_bare_mass":True,
            "quartic_allowed_with_R_when_mass_is_from_R":True}
    return counts
def continuous():
    rows=[]
    for e,m in itertools.product((-5,-2,0,2,5),repeat=2):
        S=-2*e;T=-e-m;R=-2*m
        assert -S+2*T-R==0
        if m==0:assert -S+2*T==0
        rows.append({"e":e,"m":m,"S":S,"T":T,"R":R,
          "cubic_charge":-S+2*T,"quartic_charge":-S+2*T-R})
    return rows
def high_dim_scalar_single_U1():
    # Independent toy scalar-only charge examples: charges (N,N+1)
    # have phase-sensitive primitive invariant degree N+(N+1).
    # This CAN delay scalar invariants, but DOES NOT include necessary
    # neutrino/fermion Yukawas and mixed operators.
    out=[]
    for q in (3,5,7,10,13):
        a,b=q,q+1
        best=None
        for degree in range(1,2*q+3):
            for nA in range(-degree,degree+1):
                nB=degree-abs(nA)
                for nBB in (nB,-nB):
                    if nA==nBB==0:continue
                    if a*nA+b*nBB==0:
                        best=(degree,nA,nBB);break
                if best:break
            if best:break
        assert best and best[0]==2*q+1
        out.append({"charge_A":a,"charge_B":b,"first_scalar_phase_sensitive_degree":best[0],
                    "one_primitive_exponent_pair":[best[1],best[2]]})
    return out
def main():
    out={"status":"PASS_SEESAW_ABElIAN_SELECTION_RULE_PQ_OPERATOR_IDENTITY",
      "operator_premises":["S N_e N_e","T N_e N_mu","bare N_mu N_mu"],
      "derived":"Allowed three seesaw monomials force Sdag T^2 to be allowed by EVERY additive abelian symmetry, even an arbitrary product of U(1)s and Z_n factors.",
      "second_premises":["S N_e N_e","T N_e N_mu","R N_mu N_mu"],
      "second_derived":"Replacing bare mass by R instead forces Sdag T^2 Rdag to be invariant; degree 4 if all S,T,R are elementary complex scalars.",
      "formal_charge_identities":theorem(),
      "exhaustive_Zn_charge_assignments_n2_through50":exhaustive_mod(),
      "integer_continuous_examples":continuous(),
      "delayed_scalar_only_comparators_without_yukawa_constraints":high_dim_scalar_single_U1(),
      "physics_boundary":"An allowed operator can have a protected zero coefficient under some further non-Abelian, SUSY holomorphic, nonperturbative or UV selection. These identities do not exclude an unrelated PQ combination involving additional scalar/fermion phases. They do show the minimal advertised two-singlet relative phase is not automatically high quality.",
      "prior_art":"Generic linear Abelian charge constraints and operator selection are elementary. Davighi-Greljo-Ponce Diaz arxiv:2609.01712 achieves high quality with a different full heavy spectrum."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("ABELIAN_NO_GO",theorem(),"Zn assignments",sum(n*n for n in range(2,51)),flush=True)
    return out
if __name__=="__main__":main()
