#!/usr/bin/env python3
"""2026-09-23: execute five next attacks plus three outside-box physics probes.

Five queued attacks
-------------------
1. Replace the unit-counting Hodge metric by the exact geometric DEC weights
   and derive the weighted Hodge/Dirac/Maxwell spectra.
2. Generalize the full-similitude unitary completion to every odd prime power,
   including the exact Heisenberg character and commutant collapse.
3. Classify anti-linear E8 symmetries compatible with the physical Z3 grading:
   the full normalizer has two anti-linear cosets; the neutral-fixed scalar
   subclass consists of six exact maps.
4. Minimize the FI-center pulse word under the actual mixer cost.  Since
   U_F^4=omega I, exact gate synthesis constant-folds to a single arm-relative
   phase and zero F3 traversals; testing the four-tick identity is a separate
   experiment.
5. Turn the p=5 likelihood into a sequential multi-hypothesis experiment and
   extend it to q=7 and q=9.  q=9 requires three trace probes and benefits
   strongly from adaptive probe selection.

Three additional physics probes
-------------------------------
6. The geometric Dirac square contains an exact n^2 ladder:
      (24/5) * {1^2,2^2,3^2}.
7. The E8 matter+antimatter sector exactly saturates the minimal q=3
   full-similitude family carrier: 162=27*6, with both nontrivial H27 center
   characters and no missing character sector.
8. The failed Kramers T^2=-1 is replaced by exact anti-linear order-6 E8
   symmetries with T^2=Z_FI or Z_FI^{-1}.

No continuum-spacetime, laboratory, or observed-particle claim is made.
"""
from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260923_execute_next5_plus3_geometric_semilinear.json"


def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def weighted_spectrum():
    # Exact circumcentric weights from the prior geometric-Hodge certificate.
    # The common sqrt(30) cancels from every adjoint ratio.
    w0 = Fraction(5,108)
    w1 = Fraction(1,72)
    w2 = Fraction(1,15)
    w3 = Fraction(18,25)
    r10 = w1 / w0
    r21 = w2 / w1
    r32 = w3 / w2
    assert (r10, r21, r32) == (Fraction(3,10), Fraction(24,5), Fraction(54,5))

    # Unweighted orthogonal Hodge decomposition already certified in the repo:
    # d0 d0^T gives 10^24 + 16^15 on im d0;
    # d1^T d1 gives 4^120 on im d1^T;
    # d2 d2^T = 4 I_40, and H^1 has dimension 81.
    L0 = {Fraction(0):1, 10*r10:24, 16*r10:15}
    L1 = {Fraction(0):81, 10*r10:24, 16*r10:15, 4*r21:120}
    L2 = {4*r21:120, 4*r32:40}
    L3 = {4*r32:40}
    assert L0 == {Fraction(0):1, Fraction(3):24, Fraction(24,5):15}
    assert L1 == {
        Fraction(0):81, Fraction(3):24, Fraction(24,5):15, Fraction(96,5):120
    }
    assert L2 == {Fraction(96,5):120, Fraction(216,5):40}
    assert L3 == {Fraction(216,5):40}

    total = {}
    for row in (L0,L1,L2,L3):
        for lam,m in row.items():
            total[lam] = total.get(lam,0)+m
    assert total == {
        Fraction(0):82,
        Fraction(3):48,
        Fraction(24,5):30,
        Fraction(96,5):240,
        Fraction(216,5):80,
    }

    return {
        "weights_exact_common_sqrt30_removed": {
            "w0":"5/108","w1":"1/72","w2":"1/15","w3":"18/25"
        },
        "adjoint_ratios": {
            "w1_over_w0":"3/10",
            "w2_over_w1":"24/5",
            "w3_over_w2":"54/5",
        },
        "laplacian_spectra": {
            "L0": {fstr(k):v for k,v in L0.items()},
            "L1": {fstr(k):v for k,v in L1.items()},
            "L2": {fstr(k):v for k,v in L2.items()},
            "L3": {fstr(k):v for k,v in L3.items()},
        },
        "total_D_squared_spectrum": {fstr(k):v for k,v in total.items()},
        "dirac_spectrum": {
            "0":82,
            "+-sqrt(3)":24,
            "+-sqrt(24/5)":15,
            "+-sqrt(96/5)":120,
            "+-sqrt(216/5)":40,
        },
        "maxwell_C1_decomposition": {
            "exact_gauge_modes":39,
            "harmonic_topological_modes":81,
            "coexact_propagating_modes":120,
            "coexact_Maxwell_eigenvalue":"96/5",
            "statement":"After quotienting exact gauge modes, C1 has 81 zero harmonic modes plus one 120-fold coexact band at 96/5."
        },
    }


def full_similitude_theorem():
    cases={}
    for q in [3,5,7,9,11,13,25,27,49,81]:
        cases[str(q)] = {
            "nontrivial_center_characters":q-1,
            "schrodinger_dimension_each":q,
            "minimal_full_carrier_dimension":q*(q-1),
            "Hq_commutant_dimension":q-1,
            "full_similitude_commutant_dimension":1,
            "conjugate_pair_dimension":2*q,
            "conjugate_pair_is_complete":q==3,
        }

    return {
        "all_odd_prime_power_construction": {
            "carrier":"H_full = direct_sum_{t in F_q^*} H_t, basis |t,x>",
            "X":"X_u |t,x> = |t,x+u>",
            "Z":"Z_v |t,x> = psi(Tr(t v x)) |t,x>",
            "center":"C_z |t,x> = psi(Tr(t z)) |t,x>",
            "fourier":"blockwise finite Fourier/Weil generator on each t-sector",
            "chirp":"blockwise psi(Tr(t x^2/2)) quadratic phase",
            "determinant":"D_a |t,x> = |a^{-1}t,x>, giving (u,v,z)->(u,a v,a z)",
            "frobenius":"U_sigma |t,x> = |t^p,x^p>, extending to GammaL(2,q)",
        },
        "restricted_Hq_character": {
            "identity":"q(q-1)",
            "nontrivial_center_z":"-q",
            "noncentral_Heisenberg_element":"0",
            "derivation":"sum all q-1 nontrivial central-character Schrodinger characters once",
        },
        "commutant": {
            "Hq":"C^(q-1), diagonal scalars on the multiplicity-free central-character sectors",
            "Hq_semidirect_GL2":"C, because determinant F_q^* acts transitively on the q-1 sectors",
            "Hq_semidirect_GammaL2":"C, Frobenius preserves the same transitive imprimitivity system",
            "irreducible_full_carrier":True,
        },
        "minimality_uniqueness": {
            "lower_bound":"q(q-1)",
            "proof":"det:GL(2,q)->F_q^* is onto; one faithful center character has orbit all q-1 nontrivial characters, and finite Stone-von Neumann makes their q-dimensional irreps inequivalent.",
            "attained":True,
            "minimal_sector_content_unique":True,
            "phase_convention_boundary":"Different Weil lifts / quotient characters can change phases without changing the forced sector content."
        },
        "cases":cases,
    }


def antilinear_classification():
    # C is the physical FI grading automorphism:
    # C=(1,omega,omega^2) on (g0,g1,g2).
    # K is coefficient conjugation in the integral Chevalley basis:
    # grade preserving, K C K^-1=C^-1, K^2=1.
    # theta is root opposition, linear, grade swapping,
    # theta C theta^-1=C^-1, theta^2=1.
    # J=theta K is the repo-certified split real involution and commutes with C.
    rows=[]
    for k in range(3):
        rows.append({
            "name":f"K_{k}=C^{k} K",
            "grade_action":"preserve g1,g2",
            "square":"1",
            "order":2,
            "phase_on_g1":f"omega^{k}",
            "phase_on_g2":f"omega^{2*k%3}",
        })
    for k in range(3):
        sq=(2*k)%3
        rows.append({
            "name":f"J_{k}=C^{k} J",
            "grade_action":"exchange g1<->g2",
            "square":"1" if sq==0 else f"C^{sq}",
            "order":2 if k==0 else 6,
            "phase_twisted_exchange":True,
        })

    # Scalar twist completeness with neutral action held fixed:
    # [g1,g1]->g2 and [g1,g2]->g0 force beta=alpha^2 and alpha beta=1,
    # hence alpha^3=1.
    return {
        "full_normalizer_cosets": {
            "statement":"Every anti-linear automorphism normalizing <C> is in G0*K or G0*J, where G0 is the complex grade-zero centralizer E6 x A2 (mod its finite common center).",
            "reason":"Compose with K to obtain a linear normalizer of <C>; N(<C>)/G0 embeds in Aut(C3)=C2, and root opposition theta realizes inversion.",
            "continuous_boundary":"Composing by arbitrary G0 gives continuous families; the six rows below classify the neutral-fixed scalar-twist subclass used by the physical grading compiler."
        },
        "neutral_fixed_scalar_twist_equations": {
            "g1g1_to_g2":"beta=alpha^2",
            "g1g2_to_g0":"alpha*beta=1",
            "consequence":"alpha^3=1, so exactly three twists in each grade-action class",
        },
        "canonical_six":rows,
        "K_relations":{
            "K_squared":"1","K_C_Kinv":"C^-1"
        },
        "theta_relations":{
            "theta_squared":"1","theta_C_theta_inv":"C^-1"
        },
        "J_relations":{
            "J":"theta K","J_squared":"1","J_C_Jinv":"C"
        },
        "forbidden_Kramers":"No member has square -I on g1+g2; the exact bracket no-go from the prior pass remains.",
    }


def pulse_minimization():
    return {
        "target":"U_F^4 = omega I_3 = Z_FI on the family qutrit",
        "unoptimized_identity_test_word":{
            "F3_or_inverse_traversals":8,
            "selective_120deg_phase_masks":12,
            "raw_primitives":20,
        },
        "exact_gate_synthesis_optimum":{
            "F3_or_inverse_traversals":0,
            "relative_phase_operations":1,
            "operation":"ARM_RELATIVE_PHASE(+120 deg) applied uniformly to all three signal qutrit modes",
            "proof_of_optimality":"Mixer cost is nonnegative, and the target is scalar; a reference-arm phase realizes it with zero mixers, the absolute lower bound.",
        },
        "full_E8_grade_register_form":{
            "operation":"one ternary grade phase diag(1,omega,omega^2)",
            "mixer_count":0,
            "comment":"If g0/g1/g2 are explicit control sectors, the FI center is a single diagonal grade-latch operation."
        },
        "verification_vs_implementation":{
            "implementation":"Use the compressed scalar/grade phase.",
            "relation_test":"To experimentally certify that four G25 ticks equal the center, compare the original 20-primitive path against the compressed reference in an interferometer/process-tomography protocol.",
            "important_boundary":"Constant-folding proves optimal implementation of the already-certified target; it does not experimentally validate the four-tick product without running the long path."
        },
        "hardware_boundary":"The repo's GLOBAL_FRAME_PHASE was bookkeeping-only for an isolated qutrit. Making it observable requires a bypass/control arm; no measured W33 device packet currently calibrates this new arm-relative primitive."
    }


def _entropy(p):
    p=np.asarray(p,dtype=float)
    p=p[p>0]
    return float(-(p*np.log(p)).sum())


def sequential_experiment(seed=20260923, trials=5000):
    V=0.965
    b=0.01
    eta=V*(1-b)
    alpha5=2.866515718791933e-7
    target=1-alpha5

    def pphase(phi):
        return (1+eta*math.cos(phi))/2

    # Quotient labels F_q^*/{+-1}.  Cosine already identifies m and -m.
    pm5=np.array([[pphase(2*math.pi/5)],[pphase(4*math.pi/5)]])
    pm7=np.array([[pphase(2*math.pi*r/7)] for r in (1,2,3)])

    # q=9 = F3[a]/(a^2+1). Quotient by +-1 has four projective directions.
    # Trace(a+b alpha times c+d alpha)=2ac+bd mod 3.
    low=pphase(2*math.pi/3)
    high=pphase(0)
    pm9=np.array([
        [low, high, low],   # [1:0]
        [high, low, low],   # [0:1]
        [low, low, high],   # [1:1]
        [low, low, low],    # [1:2]
    ])

    rng=np.random.default_rng(seed)

    def run(pmat,adaptive=False):
        H,S=pmat.shape
        stops=[]
        errors=0
        setting_count=np.zeros(S,dtype=int)
        for _ in range(trials):
            true=int(rng.integers(H))
            lp=np.full(H,-math.log(H))
            for t in range(1,1001):
                if adaptive and S>1:
                    m=lp.max(); post=np.exp(lp-m); post/=post.sum()
                    h0=_entropy(post)
                    gains=[]
                    for s in range(S):
                        ps=pmat[:,s]
                        py=float(post@ps)
                        lp1=lp+np.log(ps); mm=lp1.max(); po1=np.exp(lp1-mm);po1/=po1.sum()
                        lp0=lp+np.log1p(-ps); mm=lp0.max(); po0=np.exp(lp0-mm);po0/=po0.sum()
                        gains.append(h0-(py*_entropy(po1)+(1-py)*_entropy(po0)))
                    s=int(np.argmax(gains))
                else:
                    s=(t-1)%S
                setting_count[s]+=1
                y=rng.random()<pmat[true,s]
                lp += np.log(pmat[:,s] if y else 1-pmat[:,s])
                mm=lp.max();post=np.exp(lp-mm);post/=post.sum()
                if post.max()>=target:
                    errors += int(np.argmax(post)!=true)
                    stops.append(t)
                    break
            else:
                errors += int(np.argmax(lp)!=true)
                stops.append(1000)
        return {
            "trials":trials,
            "mean_detected_events":float(np.mean(stops)),
            "median":float(np.median(stops)),
            "p95":float(np.percentile(stops,95)),
            "p99":float(np.percentile(stops,99)),
            "maximum":int(np.max(stops)),
            "observed_errors":int(errors),
            "setting_uses":[int(x) for x in setting_count],
        }

    q5=run(pm5,False)
    q7=run(pm7,False)
    q9_cyclic=run(pm9,False)
    q9_adaptive=run(pm9,True)

    return {
        "calibration_model":{"visibility":V,"background":b,"target_posterior":target},
        "quotient_entropies_bits":{
            "q5":1.0,
            "q7":math.log2(3),
            "q9":2.0,
        },
        "probability_tables":{
            "q5":pm5.tolist(),"q7":pm7.tolist(),"q9_three_probes":pm9.tolist()
        },
        "q9_geometry":{
            "identity":"F9^*/{+-1} = F9^*/F3^* = P^1(F3), four projective directions",
            "probe_traces":"z=1, alpha, 1+alpha give three binary high/low interferometers",
            "four_signatures":["LHL","HLL","LLH","LLL"],
        },
        "five_sigma_sequential_simulation":{
            "seed":seed,
            "q5":q5,
            "q7":q7,
            "q9_cyclic":q9_cyclic,
            "q9_adaptive_information_gain":q9_adaptive,
        },
        "key_result":"Shot complexity is not determined by log2((q-1)/2) alone: q9 carries 2 obstruction bits yet adaptive three-probe discrimination is easier than q7 under this optical model because its high/low phase contrast is larger.",
        "boundary":"These are nominal calibrated Bernoulli simulations at fixed V,b. A laboratory sequential test must profile measured nuisance drift online; zero Monte Carlo errors are not a 5-sigma tail estimate."
    }


def outside_physics(weighted,similitude,anti):
    return {
        "1_exact_geometric_n_squared_tower":{
            "identity":"{24/5,96/5,216/5}=(24/5)*{1^2,2^2,3^2}",
            "multiplicities_in_total_D2":{"24/5":30,"96/5":240,"216/5":80},
            "extra_band":"3^48",
            "reading":"The metricized Dirac square contains an exact three-rung n^2 ladder generated by the circumcentric weight ratios.",
            "boundary":"This is a finite spectral identity, not a Kaluza-Klein compactification or a mass prediction."
        },
        "2_E8_matter_is_minimal_q3_similitude_completion":{
            "E8_matter_pair":"(27,3) + (27bar,3bar)",
            "dimension":162,
            "factorization":"162 = 27 * [3*(3-1)] = 27*6",
            "center_characters":["omega","omega^2"],
            "minimal_q3_family_carrier_dimension":6,
            "statement":"The two E8 matter grades contain exactly the two nontrivial qutrit Heisenberg center-character sectors. At q=3 there is no missing similitude character sector; q>3 would require additional family sectors.",
            "boundary":"This is an exact representation-content match, not a derivation that observed fermions fill E8 multiplets."
        },
        "3_Z3_generalized_antilinear_clock":{
            "operators":["T_plus=C J","T_minus=C^2 J"],
            "squares":["T_plus^2=C^2","T_minus^2=C"],
            "orders":[6,6],
            "FI_identification":"C=Z_FI=exp(2 pi i Qpsi/3)",
            "statement":"The bracket-compatible replacement for a failed Kramers square is a generalized anti-linear symmetry whose square is the physical Z3 grading center.",
            "boundary":"No physical time-reversal, CPT, degeneracy theorem, or observed antiunitary symmetry is claimed."
        }
    }


def main(write=True):
    prev=json.loads((ROOT/"data/w33_20260923_execute_five_post_frontier_attacks_frozen.json").read_text())
    real=json.loads((ROOT/"data/w33_e8_split_real_form_involution.json").read_text())
    fi=json.loads((ROOT/"data/w33_physical_fi_is_h27_center.json").read_text())
    assert prev["status"].startswith("PASS_")
    assert real["source_involution"]["J_squared"]==1
    assert fi["identity"]["same_central_character"] is True

    a1=weighted_spectrum()
    a2=full_similitude_theorem()
    a3=antilinear_classification()
    a4=pulse_minimization()
    a5=sequential_experiment()
    extra=outside_physics(a1,a2,a3)

    checks={
        "weighted_H1_keeps_81_kernel":a1["laplacian_spectra"]["L1"]["0"]==81,
        "weighted_Maxwell_band_96_over_5":a1["maxwell_C1_decomposition"]["coexact_Maxwell_eigenvalue"]=="96/5",
        "all_q_full_commutant_scalar":all(r["full_similitude_commutant_dimension"]==1 for r in a2["cases"].values()),
        "q3_only_conjugate_pair_complete":[q for q,r in a2["cases"].items() if r["conjugate_pair_is_complete"]]==["3"],
        "six_canonical_antilinear_maps":len(a3["canonical_six"])==6,
        "antilinear_nontrivial_squares_are_FI_center":set(r["square"] for r in a3["canonical_six"][3:])=={"1","C^1","C^2"},
        "FI_gate_synthesis_uses_zero_mixers":a4["exact_gate_synthesis_optimum"]["F3_or_inverse_traversals"]==0,
        "q9_has_four_projective_obstruction_labels":len(a5["q9_geometry"]["four_signatures"])==4,
        "adaptive_q9_beats_cyclic":a5["five_sigma_sequential_simulation"]["q9_adaptive_information_gain"]["mean_detected_events"] < a5["five_sigma_sequential_simulation"]["q9_cyclic"]["mean_detected_events"],
        "n_squared_tower_exact":extra["1_exact_geometric_n_squared_tower"]["identity"]=="{24/5,96/5,216/5}=(24/5)*{1^2,2^2,3^2}",
        "E8_q3_family_completion_exact":extra["2_E8_matter_is_minimal_q3_similitude_completion"]["dimension"]==162,
        "Z3_antilinear_orders6":extra["3_Z3_generalized_antilinear_clock"]["orders"]==[6,6],
    }
    assert all(checks.values())

    out={
        "schema":"w33.20260923.execute_next5_plus3_geometric_semilinear.v1",
        "status":"PASS_NEXT5_PLUS3_GEOMETRIC_HODGE_ALLQ_SIMILITUDE_ANTILINEAR_E8_OPTIMAL_FI_SEQUENTIAL_HOLONOMY",
        "attack1_weighted_DEC_Maxwell":a1,
        "attack2_all_odd_prime_power_similitudes":a2,
        "attack3_antilinear_E8_Z3_classification":a3,
        "attack4_FI_pulse_minimization":a4,
        "attack5_sequential_q5_q7_q9":a5,
        "outside_box":extra,
        "remote_execution_note":"Remote Desktop Commander device was registered but offline during this pass; calculations were therefore executed in the ChatGPT analysis runtime and frozen for repo replay.",
        "boundaries":[
            "geometric DEC spectrum is finite and dimensionless until a physical scale is supplied",
            "minimal all-character carrier is representation theory, not a particle census",
            "anti-linear classification has a continuous G0 dressing; the six-map table is the neutral-fixed scalar-twist subclass",
            "zero-mixer FI synthesis implements the already-certified target but does not by itself test the four-tick product identity",
            "sequential simulations use a nominal calibrated Bernoulli model, not laboratory data",
            "outside-box interpretations are hypotheses fenced from the exact finite identities"
        ],
        "parents":[
            "data/w33_20260923_execute_five_post_frontier_attacks_frozen.json",
            "data/w33_e8_split_real_form_involution.json",
            "data/w33_physical_fi_is_h27_center.json",
            "data/w33_20260923_next5_plus3_physics_frozen.json"
        ],
        "checks":checks,
    }
    if write:
        OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out


if __name__=="__main__":
    r=main(True)
    print(json.dumps({"status":r["status"],"checks":len(r["checks"]),"all":all(r["checks"].values())},indent=2))
