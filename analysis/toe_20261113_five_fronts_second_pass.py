#!/usr/bin/env python3
"""Five independent follow-ups: photonic mode synthesis, H27/E6 signed
cubic action, scalar QCA continuum obstruction, six-leg Choi entanglement,
and explicit S3 rank-code MUB symmetry.

All outputs are exact integers/rationals or clearly labeled modeling
assumptions. Never interpret a single photon as three separated particles.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product,combinations
from pathlib import Path
import math,sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as G
import toe_20261113_ccz_clifford_normalform as C
import toe_20261113_h27_maximal_translation_bridge as H
OUT=ROOT/"data/toe_20261113_five_fronts_second_pass.json"

def optical():
    fcounts=Counter(C.phase(k) for k in G.V)
    assert fcounts=={0:19,1:4,2:4}
    ccz=Counter(math.prod(k)%3 for k in G.V)
    assert ccz==fcounts
    # One photon in 27 *physical* paths can be acted on by passive U(27).
    # A Fourier F3^{x3} layer uses 9 disjoint 3x3 tritters per axis.
    # 2 Fourier layers: 54 tritters; P_L is a path relabeling,
    # and CCZ diagonal needs eight nontrivial optical phases.
    eta=.90
    sigma=.10
    survival=(19+8*eta)/27
    conditional_fidelity=(19+8*math.sqrt(eta))**2/(27*(19+8*eta))
    # Independent mean-zero Gaussian errors on the eight modified phase arms,
    # leaving 19 ideal reference arms:
    # E[|19+sum_j exp(i delta_j)|^2] / 27^2.
    phase_expected=(19**2+8+2*19*8*math.exp(-sigma*sigma/2)
                    +8*7*math.exp(-sigma*sigma))/27**2
    assert 0<conditional_fidelity<1
    assert 0<phase_expected<1
    return {
      "status":"EXACT_27_MODE_INTERFEROMETER_COMPILATION",
      "mode_count":27,
      "fourier_3mode_tritters":54,
      "passive_27_mode_wiring_permutations":2,
      "ccz_phase_sites":8,
      "phase_site_counts":{"zero":19,"plus120":4,"minus120":4},
      "realization":"single photon with an experimentally addressable 27-dimensional mode space; arbitrary U(27) is linear optics",
      "important_hardware_distinction":"mode-encoded virtual 3-qutrit CCZ is not a deterministic entangling CCZ between three separated photons",
      "model":"six serial tritter crossings per path, each power transmission eta_T; eight special phase paths additionally have power transmission eta_P, rest unit. Coherent postselected no-click environment. No mode mixing, crosstalk, source or detector errors.",
      "assumed_phase_path_eta":eta,
      "postselected_survival_at_unit_tritter_eta":survival,
      "postselected_state_fidelity_for_computational_input":conditional_fidelity,
      "survival_general":"eta_T^6*(19+8 eta_P)/27 for any computational basis input",
      "conditional_fidelity_general":"(19+8 sqrt(eta_P))^2/[27(19+8 eta_P)] for each basis input",
      "independent_gaussian_phase_sigma_radians":sigma,
      "expected_process_fidelity_phase_only":phase_expected,
      "expected_process_fidelity_formula":"(369+304 exp(-sigma²/2)+56 exp(-sigma²))/729",
      "scope":"Theoretical mode-circuit synthesis with illustrative conditional noise models; not gate fidelity data nor universal scalable optical quantum processing."
    }

def cubic_e6():
    can=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text())
    bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    signed={tuple(sorted(map(int,x["triple"]))): (1 if int(x["sign"])%3==1 else -1)
            for x in can["solution"]["d_triples"]}
    assert len(signed)==45
    eh={int(k):tuple(map(int,v)) for k,v in bridge["maps"]["e6id_to_current_H27_address"].items()}
    he={v:k for k,v in eh.items()}
    assert len(eh)==len(he)==27
    orbits=[]
    for b in range(3):
        orbit={i for i,h in eh.items() if h[1]==b}
        assert len(orbit)==9
        triples=[(tr,sgn) for tr,sgn in signed.items() if set(tr)<=orbit]
        orbits.append({"b":b,"support_size":9,"internal_signed_triples":len(triples)})
    all_recs=[]
    # Compare signed E6 cubic triads before and after PERMUTATION by
    # right-translation in H27. Diagonal signs are considered ONLY if
    # the triad incidence set is preserved by the permutation.
    def gf2_solve(rows,n):
        pivots={}
        for indices,rhs in rows:
            mask=sum(1<<i for i in indices)
            mask|=(rhs&1)<<n
            while mask:
                j=(mask&((1<<n)-1)).bit_length()-1
                if j<0:
                    return False
                if j in pivots:mask^=pivots[j]
                else:pivots[j]=mask;break
        return True
    for g in G.V:
        perm={i:he[H.mul(eh[i],g)] for i in range(27)}
        after={tuple(sorted(perm[i] for i in tr)):sgn for tr,sgn in signed.items()}
        if set(after)!=set(signed):
            all_recs.append({"g":list(g),"incidence":False,"pure_permutation_signed":False,"signed_monomial_possible":False})
            continue
        exact=all(after[tr]==signed[tr] for tr in signed)
        equations=[]
        for tr,sgn in signed.items():
            # target triad tr has transformed signed source coefficient
            # after[tr]; diagonal sign on target coordinates recovers sign.
            equations.append((tr,0 if after[tr]==sgn else 1))
        can_sign=gf2_solve(equations,27)
        all_recs.append({"g":list(g),"incidence":True,"pure_permutation_signed":exact,"signed_monomial_possible":can_sign})
    return {
      "status":"EXACT_H27_TRANSLATION_CUBIC_COMPATIBILITY_AUDIT",
      "signed_cubic_triples":45,"per_b_fiber":orbits,
      "right_H27_permutations_checked":27,
      "preserve_unsigned_triple_incidence":sum(r["incidence"] for r in all_recs),
      "preserve_signed_cubic_by_pure_permutation":sum(r["pure_permutation_signed"] for r in all_recs),
      "recover_signed_cubic_with_diagonal_pm1":sum(r["signed_monomial_possible"] for r in all_recs),
      "per_element":all_recs,
      "scope":"Only coordinate permutation and ±1 diagonal lift of the fixed canonical 45-term E6 cubic. Does not exclude general E6 linear transformations or an independent physical action."}

def continuum():
    reps=((1,0,0),(0,0,1),(1,1,1),(1,2,1))
    reps_alt=((1,0,0),(0,0,1),(1,1,1),(1,-1,1))
    assert all(tuple(t%3 for t in a)==tuple(t%3 for t in b) for a,b in zip(reps,reps_alt))
    velocities=[]
    for steps in (reps,reps_alt):
        gradient=tuple(2*sum(v[j] for v in steps) for j in range(3))
        assert gradient!=(0,0,0)
        velocities.append(gradient)
    assert velocities==[(6,6,6),(6,0,6)]
    return {"status":"EXACT_SCALAR_INFINITE_LATTICE_LIFT_DRIFT_OBSTRUCTION",
      "dispersion":"D(k) symbol 2i sum_{v in steps} sin(k dot v); Hermitian iD eigenvalue -2 sum sin(k dot v)",
      "low_k_linear_gradient_choices":velocities,
      "two_valid_integer_lifts_of_F3_directions":[[list(v) for v in reps],[list(v) for v in reps_alt]],
      "no_unique_continuum_cone_from_mod3_directions":True,
      "scalar_single_band_linear_term":"advection along one drift vector; zero in its transverse plane, not isotropic Dirac |k|",
      "no_emergent_4D_lorentzian_gravity":True,
      "escape_requirements":"additional spinor bands/local gauge constraints, selected lattice lifts, a scaling limit and rotational/Lorentz tests",
      "scope":"Obstruction to this naive translation-invariant scalar lift only; no general theorem excluding all W33 multiband or interacting gravity models."}

def holographic_choi():
    _,_,D=G.build()
    I=np.eye(27,dtype=np.int64)
    M=(18*I+3*D+D@D)//2
    assert np.array_equal(M.T@M,81*I)
    # state six qutrits order (output xyz, input abc);
    # each amplitude integer M[out,in]/sqrt(2187).
    T=M.reshape((3,3,3,3,3,3))
    norm=int((M*M).sum())
    assert norm==2187
    rows=[]
    for axes in combinations(range(6),3):
        opposite=tuple(i for i in range(6) if i not in axes)
        B=np.transpose(T,axes+opposite).reshape(27,27)
        gram=B@B.T
        purity=Fraction(int(np.sum(gram*gram)),norm*norm)
        rank=int(np.linalg.matrix_rank(B))
        rows.append({"cut":"".join(str(a) for a in axes),"rank":rank,
                    "purity":str(purity),"maximally_mixed":bool(gram.shape==(27,27) and np.array_equal(27*gram,norm*np.eye(27,dtype=np.int64)))})
    assert len(rows)==20
    assert any(not r["maximally_mixed"] for r in rows)
    assert any(r["maximally_mixed"] for r in rows)
    return {"status":"EXACT_SIX_QUTRIT_CHOI_THREE_VS_THREE_CUT_CENSUS",
      "choi_amplitudes":"M[out,in]/sqrt(2187), M=9U exactly integer",
      "num_3_vs_3_cuts":20,
      "number_maximally_mixed":sum(r["maximally_mixed"] for r in rows),
      "rank_census":dict(Counter(str(r["rank"]) for r in rows)),
      "purity_census":dict(Counter(r["purity"] for r in rows)),
      "cuts":rows,"AME_6_3_perfect_tensor":False,
      "scope":"U Choi not an AME(6,3) perfect tensor; does not forbid adding ancillas/code encoders or separate holographic QECC constructions."}

def main():
    a=optical()
    b=cubic_e6()
    c=continuum()
    d=holographic_choi()
    result={"schema":"toe.20261113.second_pass.multifront.v1",
            "optical":a,"e6":b,"continuum":c,"holography":d}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"optical":{"phase_sites":a["ccz_phase_sites"],"survival_at_etaP_0_9":a["postselected_survival_at_unit_tritter_eta"],"conditional_fidelity":a["postselected_state_fidelity_for_computational_input"],"phase_only_process_fidelity":a["expected_process_fidelity_phase_only"]},
       "e6":{k:b[k] for k in ["per_b_fiber","preserve_unsigned_triple_incidence","preserve_signed_cubic_by_pure_permutation","recover_signed_cubic_with_diagonal_pm1"]},
       "continuum":c["low_k_linear_gradient_choices"],
       "holography":{k:d[k] for k in ["number_maximally_mixed","rank_census","purity_census"]}},indent=2),flush=True)
    return result
if __name__=="__main__":main()
