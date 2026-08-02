#!/usr/bin/env python3
"""Pass 2422: all-q SRG algebra closure with permutation-rank firewall."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
FINITE = ROOT / "data" / "w33_pass2064_regular_spread_rank3_family_q357.json"
RANK = ROOT / "data" / "w33_pass2311_regular_spread_rank_three_obstruction.json"
OUT = ROOT / "data" / "w33_pass2422_regular_spread_srg_algebra_closure.json"
EXPECTED = "TO_BE_FROZEN"


def digest(d):
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def F(x):
    return str(sp.factor(sp.simplify(x)))


def build():
    finite = json.loads(FINITE.read_text())
    rank = json.loads(RANK.read_text())
    assert finite["sha256_without_hash_field"] == "28c28d5078aa495c3022a6a6153b0e83d55a70a9160179c15cd23a4d8a25a60e"
    assert rank["sha256_without_hash_field"] == "88071605fd38c0438928e94d8b0ad35508a5e5fe7de91f19c9450c26973f5663"

    q = sp.symbols("q", integer=True, positive=True)
    v = q**2 * (q**2 - 1) / 2
    k = q * (q - 2) * (q**2 + 1) / 2
    r = q * (q - 2)
    s = -q
    mu = sp.factor(k + r * s)
    lam = sp.factor(mu + r + s)
    mr = sp.factor((-k - (v - 1) * s) / (r - s))
    ms = sp.factor(v - 1 - mr)
    kc = sp.factor(v - 1 - k)
    lamc = sp.factor(v - 2 - 2 * k + mu)
    muc = sp.factor(v - 2 * k + lam)
    rc, sc = -1 - s, -1 - r

    formulas = {
        "vertices": v,
        "valency_qplus1_relation": k,
        "lambda": lam,
        "mu": mu,
        "nontrivial_eigenvalue_r": r,
        "nontrivial_eigenvalue_s": s,
        "multiplicity_r": mr,
        "multiplicity_s": ms,
        "complement_valency": kc,
        "complement_lambda": lamc,
        "complement_mu": muc,
        "complement_eigenvalue_r": rc,
        "complement_eigenvalue_s": sc,
    }
    checks = {
        "srg_counting_identity": sp.simplify(k * (k - lam - 1) - (v - k - 1) * mu) == 0,
        "eigen_sum": sp.simplify(r + s - (lam - mu)) == 0,
        "eigen_product": sp.simplify(r * s - (mu - k)) == 0,
        "multiplicities_sum": sp.simplify(1 + mr + ms - v) == 0,
        "trace_zero": sp.simplify(k + mr * r + ms * s) == 0,
        "trace_square": sp.simplify(k**2 + mr * r**2 + ms * s**2 - v * k) == 0,
        "complement_parameters": sp.simplify(kc - (q - 1) * (q**2 + 1)) == 0 and sp.simplify(lamc - (q - 1) * (q + 2)) == 0 and sp.simplify(muc - 2 * q * (q - 1)) == 0,
        "complement_eigenvalues": sp.simplify(rc - (q - 1)) == 0 and sp.simplify(sc + (q - 1) ** 2) == 0,
    }

    u = sp.symbols("u", integer=True, nonnegative=True)
    odd_forms = {name: sp.expand(expr.subs(q, 2 * u + 1)) for name, expr in formulas.items()}
    checks["odd_q_integrality"] = all(sp.denom(expr) == 1 for expr in odd_forms.values())

    reconciliation = {}
    for qs in (3, 5, 7):
        row = finite["complete_finite_results"][str(qs)]
        calculated = {name: int(expr.subs(q, qs)) for name, expr in formulas.items()}
        assert calculated["vertices"] == row["spreads"]
        assert calculated["valency_qplus1_relation"] == row["qplus1_relation"]["k"]
        assert calculated["lambda"] == row["qplus1_relation"]["lambda_"]
        assert calculated["mu"] == row["qplus1_relation"]["mu"]
        reconciliation[str(qs)] = calculated
    checks["q357_exact_reconciliation"] = True

    H = 2 * q**2 * (q**4 - 1)
    quotient = sp.factor(H / k)
    remainder_mod_qminus2 = sp.rem(4 * q * (q**2 - 1), q - 2, domain=sp.ZZ)
    checks["rank_three_divisibility_remainder_24"] = remainder_mod_qminus2 == 24
    checks["rank_three_odd_q_only_3_5"] = rank["divisibility"]["odd_q_consequence"].endswith("q in {3,5}.")
    checks["q7_exact_not_single_suborbit"] = not rank["divisibility"]["sample_table"][2]["divides"]
    assert all(bool(x) for x in checks.values())

    d = {
        "schema": "w33.pass2422.regular_spread_srg_algebra_closure.v1",
        "status": "PASS_CONDITIONAL_ALL_Q_SRG_CLOSURE_WITH_GROUP_RANK_FIREWALL",
        "sources": {
            "complete_q357": {"path": str(FINITE.relative_to(ROOT)), "sha256_without_hash_field": finite["sha256_without_hash_field"]},
            "rank_obstruction": {"path": str(RANK.relative_to(ROOT)), "sha256_without_hash_field": rank["sha256_without_hash_field"]},
        },
        "conditional_input": {
            "orbit_size": F(v),
            "relation_valency": F(k),
            "two_nontrivial_eigenvalues": [F(r), F(s)],
            "scope": "The input is exact at q=3,5,7 and conjectural as a uniform geometric spectrum beyond those complete cases.",
        },
        "forced_srg_formulas": {name: F(expr) for name, expr in formulas.items()},
        "odd_q_integral_forms": {name: str(expr) for name, expr in odd_forms.items()},
        "q357_reconciliation": reconciliation,
        "permutation_rank_firewall": {
            "point_stabilizer_order": F(H),
            "stabilizer_order_over_relation_valency": F(quotient),
            "remainder_mod_q_minus_2": int(remainder_mod_qminus2),
            "consequence": "If the valency formula holds, a single stabilizer suborbit is possible for odd q only at q=3 or q=5.",
            "q7_exact_consequence": "The exact q=7 strongly regular relation is a fusion of at least two finer PGSp stabilizer suborbits; it is not a rank-three permutation action.",
        },
        "checks": checks,
        "theorem": "Once the regular-spread orbit size, q+1-relation valency and two nontrivial eigenvalues are supplied, all strongly regular parameters, multiplicities and complement parameters are forced symbolically for every odd q. This association-scheme closure is compatible with, but logically distinct from, permutation rank: under the same valency formula the PGSp action can be rank three only for q=3,5.",
        "remaining_geometric_problem": "Prove or refute the uniform two-eigenvalue relation spectrum beyond q=7, while allowing the relation to fuse multiple stabilizer suborbits.",
        "boundary": "This is a conditional algebra theorem and terminology correction. It neither proves the all-q geometric spectrum nor revives the refuted all-q rank-three group-action claim.",
    }
    d["sha256_without_hash_field"] = digest(d)
    return d


def main():
    d = build()
    if EXPECTED != "TO_BE_FROZEN":
        assert d["sha256_without_hash_field"] == EXPECTED
        assert d == json.loads(OUT.read_text())
    print(json.dumps({"status": d["status"], "certificate": d["sha256_without_hash_field"], "rank_three_possible_odd_q": [3, 5]}, sort_keys=True))


if __name__ == "__main__":
    main()
