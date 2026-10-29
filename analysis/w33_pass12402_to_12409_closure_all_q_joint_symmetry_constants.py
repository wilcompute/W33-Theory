"""Passes 12402-12409: the closure theorem for every odd q, the joint symmetry of the two i's, the twin obstruction, and constants as
exchange rates between counting and transfer (Claude track).

12402 -- the twin obstruction over all 59 radius-safe, exotic-free candidates of 12373-12375 (colour-only vs colour + Y-neutral hidden).
12403 -- joint symmetry on F_3^4.  The stabilizer of a Kahler structure J of W(3,3) in Sp(4,3) has order 96 = |GU(2,3)| (the finite
  U(2)); centre Z4 (the norm-1 'phase circle'); derived subgroup of order 24 with element orders 1, 2, 3^8, 4^6, 6^8 = SL(2,3), the
  binary tetrahedral group (the finite SU(2)).  Adding a light cone commuting with J: the joint stabilizer is the centre Z4 for every
  non-null cone (192 of 288) and abelian of order 8 for the 96 null ones.  [I] U(2) ~ (SU(2) x U(1))/Z2 is the electroweak group; a
  generic light cone leaves only the phase circle (hypercharge-like centre, not U(1)_em).
12404-12405 -- the closure theorem for every odd q.  Sampling (closure solutions drawn uniformly as rational nondegenerate 3-spaces for
  q = 1 mod 4, as nondegenerate generators of the Hermitian polar space H(5, q^2) for q = 3 mod 4) + a finite Urbantke reconstruction
  (inverse-metric density from the self-dual bivectors; control: random metrics recovered exactly):  q = 5: 400/400, q = 13: 200/200
  metric, all HYPERBOLIC;  q = 7: 200/200, q = 11 (when present): all metric, all ELLIPTIC;  q = 3: exact enumeration (12369), elliptic.
  Group orders: #(closure solutions) = #(metric Hodge stars of the predicted type) for q = 3 ... 13, from the exceptional isomorphisms
  O+(6, q) ~ SL(4, q) (Klein) and O-(4, q) ~ PSL(2, q^2) ~ O(3, q^2) -- the finite form of SO(3,1) ~ SO(3, C).
  Statement: closure kappa^2 = -1 always produces a metric; it is elliptic ('Lorentzian') iff -1 is a non-square (q = 3 mod 4), as over R.
12406-12408 -- constants as exchange rates (established physics, re-derived numerically from CODATA): wideband Shannon limit
  Eb/N0 -> ln 2 = Landauer k T ln 2;  alpha = Z0 / (2 R_K);  a Schwarzschild hole saturates the Bekenstein bound and equals A/(4 l_P^2);
  Smarr: M c^2 = 2 x bits x k T_H ln 2;  Margolus-Levitin 2/(pi hbar) updates/s/J;  Compton clock;  Pendry constant = 2 g0/T;  Unruh.
12409 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12402_to_12409_closure_all_q_joint_symmetry_constants.json"
A = ROOT / "analysis"


def go(n, q, eps=0):
    """orders of GO^eps(n, q): odd n -> eps = 0; even n -> eps = +-1"""
    if n % 2:
        m = (n - 1) // 2
        r = 2 * q ** (m * m)
        for i in range(1, m + 1):
            r *= q ** (2 * i) - 1
        return r
    m = n // 2
    r = 2 * q ** (m * (m - 1)) * (q ** m - eps)
    for i in range(1, m):
        r *= q ** (2 * i) - 1
    return r


def gl(n, q):
    r = 1
    for i in range(n):
        r *= q ** n - q ** i
    return r


def main():
    checks, res = {}, {}
    js = json.loads((A / "search_drivers_12403" / "joint_stab.json").read_text())
    res["12403"] = js
    jt = {k: v for k, v in js["joint"].items()}
    checks["12403: Stab(J) = 96 with centre Z4 and derived SL(2,3) (order 24); joint stabilizers Z4 (192 non-null cones), order 8 (96 null)"] = (
        js["info"]["order_SJ"] == 96 and js["info"]["centre_order"] == 4 and js["info"]["derived_order"] == 24
        and js["info"]["derived_element_orders"] == {"1": 1, "4": 6, "6": 8, "3": 8, "2": 1} and js["cones"] == 288
        and sum(v for k, v in jt.items() if k.startswith("(4,")) == 192 and sum(v for k, v in jt.items() if k.startswith("(8,")) == 96)
    U = {}
    for q in (5, 7, 11, 13):
        p = A / "search_drivers_12404" / f"urbantke_q{q}.json"
        if p.exists():
            U[q] = json.loads(p.read_text())
    res["12404_sampling"] = U
    good = True
    for q, d in U.items():
        want = "elliptic" if q % 4 == 3 else "hyperbolic"
        good &= d["metric"] == d["sampled"] and d["reconstructed_types"] == {want: d["sampled"]}
        good &= all(v[1] == v[0] for kk, v in d["controls"].items() if "closure: True" in kk)
    checks["12404: every sampled closure solution is metric; type elliptic iff q = 3 mod 4 (q = 5, 7, 13 at least); controls recovered"] = (
        good and {5, 7, 13} <= set(U))
    counts = {}
    for q in (3, 5, 7, 9, 11, 13):
        if q % 4 == 3:
            sol = go(6, q, +1) // go(3, q * q)                     # one orbit, stabiliser O(3, q^2)
            met = 2 * gl(4, q) // ((q - 1) * go(4, q, -1))         # elliptic forms, (q - 1)/2 scalars per (+-kappa)
        else:
            sol = 2 * (go(6, q, +1) // (go(3, q) ** 2))            # two discriminant classes of U, stabiliser O(U) x O(U^perp)
            met = 2 * gl(4, q) // ((q - 1) * go(4, q, +1))         # hyperbolic forms
        counts[q] = dict(solutions_group_count=sol, metric_count=met)
    res["12405_counts"] = counts
    checks["12405: group-order count of closure solutions = metric Hodge stars of the predicted type for q = 3, 5, 7, 9, 11, 13; q = 3 matches 16848"] = (
        all(v["solutions_group_count"] == v["metric_count"] for v in counts.values()) and counts[3]["metric_count"] == 16848)
    ci = json.loads((A / "search_drivers_12406" / "constants_info.json").read_text())
    res["12406"] = ci
    checks["12406: Shannon -> Landauer (ln 2), alpha = Z0/2R_K, Bekenstein = Bekenstein-Hawking, Smarr = 2 x bits x kT ln 2, Pendry = 2 g0"] = (
        ci["1_shannon_wideband_Eb_over_N0"]["limit_rel_err"] < 1e-6 and ci["2_alpha"]["rel_err"] < 1e-9
        and ci["3_bekenstein_vs_hawking"]["rel_err"] < 1e-12 and ci["8_smarr_bits"]["rel_err"] < 1e-12 and ci["6_pendry"]["same_constant_rel_err"] < 1e-12)
    tw = A / "search_drivers_12402" / "twin.json"
    if tw.exists():
        t = json.loads(tw.read_text())
        rows = [r for v in t.values() for r in v]
        res["12402"] = dict(candidates=len(t), pairings=len(rows),
                            colour_only_feasible=sum(r["colour_only_feasible"] for r in rows),
                            colour_plus_hidden_feasible=sum(r["colour_plus_hidden_feasible"] for r in rows),
                            twin_present=sum(1 for r in rows if r["twin_net_32"] > 0))
        checks["12402: colour + Y-neutral hidden sector infeasible in every pairing of every candidate"] = (
            len(t) == 59 and res["12402"]["colour_plus_hidden_feasible"] == 0)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
