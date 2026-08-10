#!/usr/bin/env python3
"""Passes 4697-4698 -- one repackaging caught before it became a mechanism, and one
coincidence reported as a coincidence.

  4697  Pass 4684 produced relay fractions for seven quadrangles and Passes 4562/4563
        produced Ramanujan signing densities for six.  The two columns look strongly
        anti-correlated, and Pass 4564 already showed block size b explains most of the
        density.  The tempting claim is that relay fraction explains the RESIDUAL -- a
        second mechanism.  Before writing that, ask what would make the comparison invalid.

  4698  Pass 4688 found 26 local-complementation classes at six qubits.  26 is a small
        integer in a repository full of small integers, and "26 appears in W(3,3) too" is
        the cheapest possible false result.  Search for it, then say plainly what the search
        licenses.

    py -3 analysis/w33_pass4697_4698_relay_residual_and_a_number_that_means_nothing.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

# (name, s, t, Ramanujan line-signing density %, source pass)
DATA = [
    ("Q(5,2)", 2, 4, 85.2, "4562"),
    ("H(3,4)", 4, 2, 0.0, "4562"),
    ("W(3,3)", 3, 3, 26.9, "4563"),
    ("Q(4,3)", 3, 3, 27.8, "4563"),
    ("Q(5,3)", 3, 9, 7.2, "4562"),
    ("H(3,9)", 9, 3, 0.0, "4562"),
]


def points(s, t):
    return (s + 1) * (s * t + 1)


def relay_fraction(s, t):
    """Fraction of point pairs that are NOT collinear -- a pure incidence count."""
    n = points(s, t)
    return 1.0 - (s * (t + 1)) / (n - 1)


def block_size(s):
    """Edges per gauge block: a line has s+1 points, so C(s+1,2) edges."""
    return (s + 1) * s // 2


def main() -> int:
    print("=" * 78)
    print("Passes 4697-4698")
    print("=" * 78)

    print("\n  PASS 4697 -- does relay fraction explain anything block size does not?\n")
    print(f"  {'geometry':9s} {'s':>2s} {'t':>2s} {'b':>3s} {'relay %':>8s} "
          f"{'Ramanujan %':>12s}")
    rows = []
    for name, s, t, dens, src in DATA:
        r = relay_fraction(s, t)
        b = block_size(s)
        rows.append({"geometry": name, "s": s, "t": t, "b": b,
                     "relay_fraction": r, "ramanujan_pct": dens, "source": src})
        print(f"  {name:9s} {s:2d} {t:2d} {b:3d} {100*r:7.1f}% {dens:11.1f}%")

    # the honest question: within a fixed block size, is there residual variation?
    print("\n  Within fixed b, does relay still track density?\n")
    groups = {}
    for r in rows:
        groups.setdefault(r["b"], []).append(r)
    residual = []
    for b in sorted(groups):
        g = sorted(groups[b], key=lambda x: x["relay_fraction"])
        if len(g) < 2:
            print(f"    b = {b:2d}   only {len(g)} geometry, no within-group comparison")
            continue
        print(f"    b = {b:2d}")
        for x in g:
            print(f"        {x['geometry']:9s} relay {100*x['relay_fraction']:5.1f}%  "
                  f"density {x['ramanujan_pct']:5.1f}%")
        mono = all(g[i]["ramanujan_pct"] >= g[i + 1]["ramanujan_pct"]
                   for i in range(len(g) - 1))
        residual.append({"b": b, "monotone_decreasing": bool(mono),
                         "members": [x["geometry"] for x in g]})
        print(f"        higher relay -> lower density: {mono}")

    b6 = next((r for r in residual if r["b"] == 6), None)
    print(f"""
    THE STRICT TEST FAILS AT b = 6, AND SAYING OTHERWISE WOULD HAVE BEEN EASY. The verdict
    printed above is {b6['monotone_decreasing'] if b6 else 'n/a'}, because W(3,3) and Q(4,3) have the SAME relay fraction
    (69.2%, they are parameter-equal) and densities 26.9% vs 27.8% -- so relay does not order
    that pair at all, in either direction. Only the third member separates: Q(5,3) at 73.0%
    relay drops to 7.2%.

    So the within-group evidence at b = 6 is ONE contrast, not three: a tied pair against a
    single higher-t geometry. Something beyond block size does appear to move the density,
    and one contrast is what supports it.

    But relay fraction is 1 - s(t+1)/((s+1)(st+1) - 1), a BIJECTIVE function of (s,t), and
    b is a function of s alone. So "relay explains the residual after b" is, exactly and
    only, "t explains the residual after s." Relay fraction contributes no information the
    parameters did not already contain -- it is a reparametrisation, and calling it a second
    mechanism would dress a coordinate change as a cause.

    THE HONEST STATEMENT: at fixed s, density falls as t rises, over three geometries at
    b = 6 and one each at b = 3 and b = 10. Three points inside one group is not a law, and
    the two singleton groups contribute no within-group evidence at all. The routing
    interpretation is a story told over that, not a finding.""")

    # ---- 4698: the number ------------------------------------------------
    print("\n  PASS 4698 -- does 26 mean anything here?\n")
    facts = [
        ("W(3,3) points", 40), ("W(3,3) lines", 40), ("degree", 12),
        ("edges", 240), ("|Sp(4,3)|", 51840), ("frames", 81),
        ("eigenvalue multiplicities", 24), ("lines through a point", 4),
    ]
    for n, v in facts:
        print(f"    {n:28s} {v:>7,d}   {'== 26' if v == 26 else ''}")
    print(f"""
    NOTHING IN W(3,3) IS 26, AND THERE IS NO REASON ANYTHING SHOULD BE. The 26 counts
    local-complementation classes of simple graphs on SIX VERTICES. Six is the qubit count of
    a three-copy protocol on two-qubit resources; it is not a number W(3,3) supplies. The
    sequence 1, 2, 3, 6, 11, 26, 59, 182 is a fact about graphs on n vertices and would be
    the same in a repository that had never heard of a generalised quadrangle.

    REPORTED AS A NON-RESULT, WHICH IS THE POINT. A small integer can be matched to
    something in a corpus this size with near-certainty, and a match found by looking is not
    evidence. The check cost two minutes and closes a direction that would otherwise stay
    open as a hunch.""")

    out = {
        "boundary": ("4697's densities are quoted from Passes 4562/4563 (600-1000 samples "
                     "per carrier) and not re-measured; the within-b comparison rests on "
                     "three geometries in one group and one each in two others, which is "
                     "too few for a fitted law and is not fitted. 4698 is a negative result "
                     "about a coincidence and establishes nothing beyond the absence of a "
                     "link that was never predicted"),
        "pass_4697": {
            "rows": rows, "within_block_groups": residual,
            "verdict": ("relay fraction is a bijective function of (s,t) and therefore "
                        "cannot add information beyond the parameters; 'relay explains the "
                        "residual after b' is exactly 't explains the residual after s', "
                        "and is a reparametrisation, not a mechanism"),
            "supported_claim": "at fixed s, Ramanujan density falls as t rises"},
        "pass_4698": {
            "lc_classes_n6": 26,
            "w33_quantities": {n: v for n, v in facts},
            "any_match": False,
            "verdict": ("26 counts local-complementation classes of graphs on six vertices, "
                        "a fact independent of W(3,3); no quantity in the geometry equals "
                        "it and none was predicted to. Coincidence, closed")},
    }
    p = ROOT / "data" / "PART_W33_PASS4697_4698_RELAY_RESIDUAL_AND_26.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
