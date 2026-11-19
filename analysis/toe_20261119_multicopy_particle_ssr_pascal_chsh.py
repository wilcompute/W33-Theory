#!/usr/bin/env python3
"""2026-11-19: Exact n-copy CHSH under strict local U(1) number SSR.

For n copies of (|10>+|01>)/sqrt(2), no borrowed phase reference,
no postselection, arbitrary ideal locally number-preserving dichotomic
measurements, and fixed source total photon number n:

S_n^max = 2 + (2sqrt2-2) [1 - 2^(popcount(n)-n)].

Constructs explicit block-diagonal observables; separately proves upper
bound via Jordan's lemma in each maximally entangled charge sector.
The Pascal/Sierpinski parity count follows from Lucas' theorem.

NOT a scalable photonic computer, efficiency/loss theorem, or new
fundamental quantum mechanics.
"""
from __future__ import annotations
import json
import math
from functools import lru_cache
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_multicopy_particle_ssr_pascal_chsh.json"

def sector_table(n:int):
    if n<0:raise ValueError("n must be nonnegative")
    D=1<<n
    rows=[]
    for k in range(n+1):
        dim=math.comb(n,k)
        odd=dim%2
        pairs=dim//2
        val=(2*math.sqrt(2)*(dim-odd)+2*odd)/dim
        rows.append({"local_A_photons":k,"local_B_photons":n-k,
                     "sector_dim":dim,"sector_probability":dim/D,
                     "CHSH_sector_optimum":val,
                     "number_2d_Jordan_blocks":pairs,
                     "number_1d_classical_blocks":odd})
    assert sum(x["sector_dim"] for x in rows)==D
    return rows

def formula(n:int):
    D=1<<n
    odd_count=sum(math.comb(n,k)%2 for k in range(n+1))
    lucas_count=1<<n.bit_count()
    assert odd_count==lucas_count
    direct=sum(row["sector_probability"]*row["CHSH_sector_optimum"]
               for row in sector_table(n))
    closed=2+(2*math.sqrt(2)-2)*(1-lucas_count/D)
    assert abs(direct-closed)<2e-12
    return {"n_copies":n,
       "n_odd_binomial_entries":odd_count,
       "number_odd_from_Lucas":lucas_count,
       "fraction_unpaired_classical_dimension":lucas_count/D,
       "fraction_paired_entangled_dimension":1-lucas_count/D,
       "SSR_CHSH_supremum":closed,
       "independent_sector_weighted_sum":direct}

def explicit_observables(n:int):
    """Local 2^n x 2^n (not joint) Hermitian involutions.

    Each local Hamming-weight sector k is maximally entangled with the
    opposite party's weight n-k sector. Pair equal-Schmidt-weight basis
    vectors into 2D Bell blocks, leaving one +1 classical block for odd d.
    """
    D=1<<n;full=D-1
    obs=[np.zeros((D,D),dtype=float) for _ in range(4)]
    A0,A1,B0,B1=obs
    root=math.sqrt(2)
    for k in range(n+1):
        aa=[a for a in range(D) if a.bit_count()==k]
        bb=[full^a for a in aa]
        assert len(aa)==math.comb(n,k)
        for j in range(0,len(aa)-1,2):
            a,a2=aa[j:j+2]
            b,b2=bb[j:j+2]
            # Bell Φ+ has <ZZ>=<XX>=+1, <ZX>=<XZ>=0.
            A0[a,a]=+1; A0[a2,a2]=-1
            A1[a,a2]=A1[a2,a]=+1
            B0[b,b]=+1/root;B0[b2,b2]=-1/root
            B1[b,b]=+1/root;B1[b2,b2]=-1/root
            B0[b,b2]=B0[b2,b]=+1/root
            B1[b,b2]=B1[b2,b]=-1/root
        if len(aa)%2:
            a=aa[-1];b=bb[-1]
            for O,idx in ((A0,a),(A1,a),(B0,b),(B1,b)):
                O[idx,idx]=+1
    # Independent checks: local number conservation and dichotomic outputs.
    number=np.diag([a.bit_count() for a in range(D)])
    for O in obs:
        assert np.linalg.norm(O@O-np.eye(D))<1e-11
        assert np.linalg.norm(number@O-O@number)<1e-11
    return obs

def correlator_full_n_copy(A,B,n):
    """Direct exact expectation on |psi_n>=2^-n/2 Σ_a |a>_A|~a>_B.

    Uses a compact Schmidt representation, not a huge 4^n density matrix.
    """
    D=1<<n
    complement=np.array([(D-1)^a for a in range(D)])
    return float(np.sum(A*B[np.ix_(complement,complement)].T)/D)

def explicit_chsh(n):
    A0,A1,B0,B1=explicit_observables(n)
    E=lambda A,B:correlator_full_n_copy(A,B,n)
    value=E(A0,B0)+E(A0,B1)+E(A1,B0)-E(A1,B1)
    theory=formula(n)["SSR_CHSH_supremum"]
    assert abs(value-theory)<1e-11,(n,value,theory)
    return {"n_copies":n,"explicit_number_conserving_CHSH":value,
            "theoretical_maximum":theory,"error":abs(value-theory)}

def chsh_with_independent_copy_loss(n,eta):
    """No postselection: each of n photons survives independently at eta.

    The physical state is a classical mixture over surviving copy subsets C.
    On each C, the state is 2^-|C|/2 Σ_{a subset C}|a>_A|C\a>_B.
    Reuse the SAME number-conserving settings optimized for eta=1.
    This is a fixed-measurement engineering falsifier, NOT the loss-optimized
    Bell threshold or a loophole-free implementation.
    """
    sector_vals=conditional_sector_chsh_values(n)
    return sum((eta**mask.bit_count())*
               ((1-eta)**(n-mask.bit_count()))*val
               for mask,val in enumerate(sector_vals))

@lru_cache(maxsize=None)
def conditional_sector_chsh_values(n):
    A0,A1,B0,B1=explicit_observables(n)
    D=1<<n
    def chsh_conditional(mask):
        sites=[i for i in range(D) if i&mask==i]
        bsites=[mask^a for a in sites]
        denom=len(sites)
        E=lambda A,B:float(np.sum(A[np.ix_(sites,sites)]*
                                B[np.ix_(bsites,bsites)].T)/denom)
        return E(A0,B0)+E(A0,B1)+E(A1,B0)-E(A1,B1)
    return tuple(chsh_conditional(mask) for mask in range(D))

def fixed_setting_loss_gate(n_max=6):
    """Numerically locate survival thresholds of a specified setting family."""
    from scipy.optimize import brentq
    rows=[]
    for n in range(2,n_max+1):
        high=chsh_with_independent_copy_loss(n,1.)
        low=chsh_with_independent_copy_loss(n,0.)
        assert abs(high-formula(n)["SSR_CHSH_supremum"])<1e-12
        assert abs(low-2)<1e-12
        xs=np.linspace(.0001,.999999,300)
        signs=np.array([chsh_with_independent_copy_loss(n,x)-2 for x in xs])
        roots=[brentq(lambda x:chsh_with_independent_copy_loss(n,x)-2,
                      float(xs[i]),float(xs[i+1]))
               for i in range(len(xs)-1) if signs[i]<0 and signs[i+1]>0]
        rows.append({"n":n,"unconditional_zero_loss_CHSH":high,
            "fixed_settings_positive_thresholds":roots,
            "at_eta_90pct":chsh_with_independent_copy_loss(n,.9),
            "at_eta_95pct":chsh_with_independent_copy_loss(n,.95)})
    return {"status":"PASS",
      "loss_model":"Independent erasure of each distinguishable photon into vacuum; all runs included; no phase reference; same local block observables optimized for eta=1.",
      "survival_efficiency_records":rows,
      "not_optimized":"Arbitrary Bell settings or POVMs might lower a threshold; detector loopholes and scalable device resources remain unmodeled."}

def proof_summary():
    return {
      "state":"[ (|1_A0_B> + |0_A1_B>)/sqrt2 ] tensor to n copies",
      "local_U1_SSR":"Each local dichotomic observable commutes with total local photon number.",
      "charge_sector":"At local Alice number k, Schmidt rank d_k=C(n,k) and weight d_k/2^n; state is |Phi_(d_k)> on paired mode-subsets.",
      "odd_dim_CHSH_bound":"For a maximally entangled |Phi_d> and binary projective observables: max CHSH=2sqrt2 if d even; [2sqrt2(d-1)+2]/d if d odd. Jordan block lemma gives an unavoidable 1D classical block in odd d, all remaining 2D blocks achieve Tsirelson.",
      "Lucas_parity":"C(n,k) odd iff k's 1-bits are a subset of n's 1-bits. Number of odd coefficients in row n is 2^popcount(n).",
      "exact_many_copy_law":"S_n=2+(2sqrt2-2)(1-2^(popcount(n)-n))",
      "pair_plateau":"S_(2m)=S_(2m+1) exactly for any m>=0; odd extra copy alone does not improve this ideal optimal CHSH figure.",
      "power_of_two_advantage":"At n=2^r, only two binomial coefficients are odd, giving S_n=2sqrt2-(2sqrt2-2)*2/2^n.",
      "limitations":"Ideal distinguishable copies and joint local number-preserving observables, no shared phase reference, no loss, no detector imperfections or circuit compilation. Collective observables can demand severe resources. This does not derive the Born rule or show universal single-photon BQP.",
      "prior_art":["https://doi.org/10.1103/PhysRevA.82.042116",
                   "https://arxiv.org/abs/1905.02652",
                   "https://mathworld.wolfram.com/LucasCorrespondenceTheorem.html",
                   "https://arxiv.org/abs/2511.21819"]
    }

def calculate(n_max=14):
    rows=[formula(n) for n in range(n_max+1)]
    explicit=[explicit_chsh(n) for n in range(0,9)]
    for m in range(n_max//2):
        assert abs(rows[2*m]["SSR_CHSH_supremum"]-
                   rows[2*m+1]["SSR_CHSH_supremum"])<1e-12
    assert abs(rows[1]["SSR_CHSH_supremum"]-2)<1e-12
    assert abs(rows[2]["SSR_CHSH_supremum"]-(1+math.sqrt(2)))<1e-12
    return {"date":"2026-11-19",
       "status":"PASS: analytical SSR-CHSH multi-copy Lucas law and explicit local observables",
       "TOE_solved":False,"physical_photonic_universality_derived":False,
       "closed_form_results_n_0_to_14":rows,
       "explicit_local_number_preserving_matrix_checks":explicit,
       "fixed_setting_independent_photon_loss":fixed_setting_loss_gate(),
       "proof_and_scope":proof_summary()}

def main():
    result=calculate()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS","n_explicit":len(result["explicit_local_number_preserving_matrix_checks"]),
       "n2":result["closed_form_results_n_0_to_14"][2]["SSR_CHSH_supremum"],
       "n4":result["closed_form_results_n_0_to_14"][4]["SSR_CHSH_supremum"],
       "n8":result["closed_form_results_n_0_to_14"][8]["SSR_CHSH_supremum"],
       "output":str(OUT)}))

if __name__=="__main__": main()
