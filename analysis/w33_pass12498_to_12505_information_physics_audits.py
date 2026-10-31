"""Passes 12498-12505 (Claude track): three information-physics tests.

12498 -- the constants claims, priced in bits.  (a) Under the corpus's own look-elsewhere grammar (w33_alphabet_pool.py) the q = 3
  alphabet hits 1 of 5 headline windows; 2,000 random 13-integer alphabets average ~2.2 and 99.65% do at least as well.  (b) Per claim:
  only m_H (1.8 sigma) and alpha_s (0.5 sigma) of the six headline "predictions" agree with experiment; 1/alpha = 137 and m_p/m_e =
  1836 miss by > 10^6 sigma; of the 54.8 bits the matches nominally claim, 12.6 survive the chance of landing that near an integer or
  small fraction -- before any formula cost.  (c) w33_mdl_shortest.py's null compared substrate observables at 1.5% tolerance with
  random targets at their tight deltas; with one rule for both, the substrate's cost-<=2 fraction (0.50 / 0.70) is matched or beaten by
  ~15% of random alphabets (p ~ 0.15): no significant evidence.
12499 -- contextuality.  Field reduction turns the grids of W(3, 2^h) into 2h-qubit context sets covering every Pauli exactly twice.
  q = 2 is the Mermin-Peres square (sign product -1, a parity proof); q = 4 (4 qubits) and q = 8 (6 qubits) give +1 -- every context
  multiplies to +I.  Reason (proof sketch in the md, checked on random groups): a commuting Hermitian Pauli group of rank >= 4 always
  multiplies to +I; ranks 2 and 3 can give -I.  So the minimal even line sets give state-independent parity proofs only at two qubits.
12500 -- the W(3,3) plaquette Ising model, exactly.  Its high-T series is Pass 173's route code [40,15,10] (enumerator recomputed and
  matched), its Wegner dual is the address code [40,15,8]: not self-dual; specific-heat maxima at K = 0.595 and 0.598.  The site's
  "critical temperature beta_c = log(1+sqrt q) from Kramers-Wannier" (Checks 1150-1163) is the square-lattice Potts value and its check
  in archive/root_scripts/SOLVE_OPEN.py is tautological: it has no derivation for W(3,3).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "analysis" / "search_drivers_12466"
OUT = ROOT / "data" / "w33_pass12498_to_12505_information_physics_audits.json"


def load(name):
    p = D / name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    checks, res = {}, {}
    an, au, mf = load("alphabet_null.json"), load("constants_information_audit.json"), load("mdl_fair_null.json")
    res["12498"] = dict(alphabet_null=an, audit=au, mdl_fair=mf)
    checks["12498a: q = 3 alphabet hits 1 of 5 windows under its own grammar; >= 99% of 2,000 random alphabets do at least as well"] = (
        an["q3"]["matches"] == 1 and an["p_matches"] >= 0.99 and an["n_random"] == 2000)
    tens = {r["name"]: r["tension_sigma"] for r in au["rows"]}
    checks["12498b: only m_H and alpha_s are within 3 sigma; 1/alpha and m_p/m_e miss by > 1e6 sigma; 12.6 of 54.8 bits survive"] = (
        sorted(au["consistent_within_3sigma"]) == ["alpha_s(M_Z)", "m_H [GeV]"] and tens["1/alpha"] > 1e6 and tens["m_p/m_e"] > 1e6
        and abs(au["total_net_bits"] - 12.62) < 0.5 and abs(sum(r["bits_claim"] for r in au["rows"]) - 54.79) < 0.5)
    checks["12498c: with one tolerance rule, ~15% of random alphabets match the substrate's cost-<=2 fraction (no significant signal)"] = (
        0.10 <= mf["loose"]["p_random_alphabet_ge_q3"] <= 0.25 and 0.10 <= mf["tight"]["p_random_alphabet_ge_q3"] <= 0.25
        and mf["tool_as_written"]["substrate"] == 0.7 and mf["tool_as_written"]["random"] < mf["loose"]["random_targets_frac_cost_le2"])
    fr = load("field_reduction_parity.json")
    res["12499"] = fr
    checks["12499: field-reduced grids -- q = 2 is the Mermin-Peres parity proof (-1); q = 4 and 8 give +1 (no parity proof)"] = (
        fr["2"]["parity_proof"] and fr["2"]["contexts"] == 6 and fr["2"]["observables"] == 9
        and not fr["4"]["parity_proof"] and fr["4"]["qubits"] == 4 and fr["4"]["observables"] == 75
        and not fr["8"]["parity_proof"] and fr["8"]["qubits"] == 6 and all(fr[k]["occurrences"] == [2] for k in ("2", "4", "8")))
    rk = load("pauli_rank_sign.json")
    res["12499_rank_signs"] = rk
    checks["12499: commuting Hermitian Pauli groups -- ranks 2, 3 multiply to -I sometimes; ranks 4, 5 always to +I (random samples)"] = (
        rk["2"].get("-1", 0) > 0 and rk["3"].get("-1", 0) > 0 and "-1" not in rk["4"] and "-1" not in rk["5"])
    th = load("w33_plaquette_thermo.json")
    res["12500"] = th
    checks["12500: route enumerator recomputed = Pass 173; address minimum 8 (45 words); not self-dual"] = (
        th["control_route_matches_pass173"] and th["control_address_min_weight_8"] and not th["self_dual"])
    checks["12500: specific-heat maxima at K ~ 0.60 for both models, far from the site's beta_c = log(1+sqrt 3) = 1.005"] = (
        abs(th["specific_heat_peak_K"]["model_A_route"] - 0.6) < 0.02 and abs(th["specific_heat_peak_K"]["model_B_address"] - 0.6) < 0.02
        and abs(th["site_claim_beta_c"] - 1.00505) < 1e-4)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
