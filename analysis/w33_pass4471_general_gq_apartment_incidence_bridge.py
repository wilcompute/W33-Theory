#!/usr/bin/env python3
"""Pass 4471 -- general GQ apartment/incidence Gram-matching criterion.

Pass 4465 proved for a finite generalized quadrangle GQ(s,t) that if H is the
line/quadrangle incidence matrix and A* is the line-collinearity graph, then

    H H^T = (r-beta) I + (alpha-beta) A* + beta J,

with

    r     = (s+1)s^2 t^2/2,
    alpha = s^2 t,
    beta  = s(s+1)/2.

If N is the point/line incidence matrix (points x lines), then independently

    N^T N = (s+1) I + A*

over the integers: a line has s+1 points and two distinct lines meet in one
point exactly when they are adjacent in the dual collinearity graph.

This pass determines exactly when the two Gram matrices become the SAME binary
form:

    H H^T = N^T N  over F_2

if and only if

    s = 3 (mod 4)  and  t is odd.

Proof from the three Bose--Mesner coefficients:

  beta = 0 (mod 2),
  alpha-beta = 1 (mod 2),
  r-beta = s+1 (mod 2).

The first two force alpha odd, hence s,t odd; beta even with s odd is exactly
s=3 mod4.  Under those conditions (s+1)/2 is even, so r,beta,s+1 are all even
and the diagonal condition follows.  Conversely the criterion makes all three
coefficient congruences hold.

There is then a generic quotient bridge, independent of any CSS interpretation.
For binary matrices H and N with H H^T=N^T N=:G,

    im(H^T)/rad(im(H^T))  ~=  F_2^L/ker(G)
                               --N-->
                             im(N)/(im(N) intersect ker(N^T)),

and the map [b] -> [Nb] preserves the induced nondegenerate alternating form.
This is elementary linear algebra: Nb is in ker(N^T) exactly when Gb=0.

Consequences for the recent examples:

  * GQ(3,3)=W(3,3): PASS, giving Pass 4469's H10 bridge.
  * GQ(3,9)=Q(5,3): PASS in the line-signing orientation.
  * the dual parameter set GQ(9,3): FAIL in that orientation.
  * GQ(q,q) satisfies the criterion precisely for q=3 mod4.

So the new bridge is NOT a generic consequence of having the same number of
points/lines or of duality; it is a characteristic-two orientation effect.
That exact asymmetry is conceptually adjacent to Pass 4457's empirical s/t
line-signing sweep, but it does not explain the Ramanujan success percentages
there and no such claim is made.
"""

from __future__ import annotations

import json
from pathlib import Path

from w33_pass4465_general_gq_line_signing_trace import formulas

ROOT = Path(__file__).resolve().parents[1]


def parity_coefficients(s: int, t: int):
    row = formulas(s, t)
    r = row.quadrangles_per_line
    alpha = row.quadrangles_per_intersecting_line_pair
    beta = row.quadrangles_per_disjoint_line_pair
    return {
        "HHt_I": (r - beta) & 1,
        "HHt_Adual": (alpha - beta) & 1,
        "HHt_J": beta & 1,
        "NtN_I": (s + 1) & 1,
        "NtN_Adual": 1,
        "NtN_J": 0,
        "r": r,
        "alpha": alpha,
        "beta": beta,
    }


def gram_match(s: int, t: int) -> bool:
    c = parity_coefficients(s, t)
    return (
        c["HHt_I"] == c["NtN_I"]
        and c["HHt_Adual"] == c["NtN_Adual"]
        and c["HHt_J"] == c["NtN_J"]
    )


def criterion(s: int, t: int) -> bool:
    return s % 4 == 3 and t % 2 == 1


def main() -> int:
    checks: list[tuple[str, bool]] = []

    def check(name: str, cond) -> None:
        ok = bool(cond)
        checks.append((name, ok))
        if not ok:
            raise AssertionError(name)

    # Exhaustive residue/property sweep well beyond the four motivating rows.
    mismatches = []
    for s in range(1, 65):
        for t in range(1, 65):
            if gram_match(s, t) != criterion(s, t):
                mismatches.append((s, t))
    check("criterion matches coefficient test for 1<=s,t<=64", not mismatches)

    # The proof has only mod-4/mod-2 content, so verify all residue classes.
    residue_table = {}
    for smod4 in range(4):
        for tmod2 in range(2):
            s = smod4 if smod4 else 4
            t = tmod2 if tmod2 else 2
            residue_table[f"s={smod4}mod4,t={tmod2}mod2"] = gram_match(s, t)
    check(
        "unique passing residue class",
        [k for k, v in residue_table.items() if v] == ["s=3mod4,t=1mod2"],
    )

    examples = {}
    for name, s, t in [
        ("GQ(2,2)=W(3,2)", 2, 2),
        ("GQ(3,3)=W(3,3)", 3, 3),
        ("GQ(3,9)=Q(5,3)", 3, 9),
        ("GQ(9,3) dual parameter set", 9, 3),
        ("GQ(5,5)", 5, 5),
        ("GQ(7,7)", 7, 7),
        ("GQ(11,11)", 11, 11),
    ]:
        c = parity_coefficients(s, t)
        examples[name] = {
            "s": s,
            "t": t,
            "criterion": criterion(s, t),
            "HHt_mod2_coefficients_I_A_J": [c["HHt_I"], c["HHt_Adual"], c["HHt_J"]],
            "NtN_mod2_coefficients_I_A_J": [c["NtN_I"], c["NtN_Adual"], c["NtN_J"]],
        }

    check("W33 passes", examples["GQ(3,3)=W(3,3)"]["criterion"])
    check("Q(5,3) orientation passes", examples["GQ(3,9)=Q(5,3)"]["criterion"])
    check("dual GQ(9,3) orientation fails", not examples["GQ(9,3) dual parameter set"]["criterion"])
    check("q=5 symmetric fails", not examples["GQ(5,5)"]["criterion"])
    check("q=7 symmetric passes", examples["GQ(7,7)"]["criterion"])
    check("q=11 symmetric passes", examples["GQ(11,11)"]["criterion"])

    result = {
        "pass": 4471,
        "theorem": "general GQ(s,t) apartment/incidence binary Gram bridge criterion",
        "criterion": "H H^T = N^T N over F_2 iff s == 3 (mod 4) and t is odd",
        "integer_gram_inputs": {
            "apartment": "H H^T = (r-beta)I + (alpha-beta)A_dual + beta J",
            "incidence": "N^T N = (s+1)I + A_dual",
            "r": "(s+1)s^2t^2/2",
            "alpha": "s^2t",
            "beta": "s(s+1)/2",
        },
        "generic_quotient_bridge_when_criterion_holds": [
            "im(H^T)/rad(im(H^T))",
            "F_2^L/ker(N^T N)",
            "im(N)/(im(N) intersect ker(N^T))",
        ],
        "map": "[b] -> [N b]",
        "pairing": "<H^T b,H^T c> = b^T N^T N c = <N b,N c>",
        "residue_table": residue_table,
        "examples": examples,
        "interpretation": (
            "The apartment/incidence bridge is an orientation-sensitive characteristic-two theorem, not a "
            "duality invariant.  W33 and GQ(3,9) satisfy it in the displayed line orientation; GQ(9,3) does not."
        ),
        "boundary": (
            "This criterion does not explain or predict the empirical line-signing Ramanujan success rates of "
            "Pass 4457.  It classifies an exact mod-2 Gram coincidence and the resulting nondegenerate quotient "
            "isometry only.  A CSS/logical interpretation requires the additional code hypotheses of the chosen family."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
        "sweep_mismatches": mismatches,
    }

    out = ROOT / "data" / "PART_W33_PASS4471_GENERAL_GQ_APARTMENT_INCIDENCE_BRIDGE.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4471 -- general GQ apartment/incidence bridge criterion")
    print("  H H^T = N^T N (mod 2) iff s=3 mod4 and t odd")
    print("  W33: PASS; GQ(3,9): PASS; dual GQ(9,3): FAIL")
    print("  generic quotient bridge: apartment parity -> incidence nondegenerate quotient")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
