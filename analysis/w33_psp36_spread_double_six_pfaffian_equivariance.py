#!/usr/bin/env python3
"""One PSp(4,3)-equivariant certificate for the 36-object chain.

This joins, objectwise and under the same five PSp generators,

    36 W33 spreads
      <-> 36 Schlaefli double-sixes
      <-> 36 doily complements
      <-> 36 signed Pfaffian sections of the 27-coordinate E6 Cartan cubic.

The local Pfaffian sign choices are gauges: each 15-variable restriction has
five free sign bits.  Accordingly the equivariance proved here is the correct
gauge-covariant statement.  PSp sends each section support to the section
support attached to the transported double-six, and each PSp generator lifts
to a signed monomial automorphism of the *full* Cartan cubic.  Source and target
supports independently carry exact Pfaffian gauges by the all-36 theorem.

No claim is made that the arbitrary free-bits-zero local gauges themselves are
fixed by PSp.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

from w33_pass4992_4999_common import build_base, build_group, closure
from w33_pfaffian_doily_e6_cubic_bridge import E6, E6_POINTS
from w33_all36_pfaffian_double_six_sections import e6_graph, build_sections, gf2_solve

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_psp36_spread_double_six_pfaffian_equivariance.json"


def signed_cubic_lift(p: tuple[int, ...]) -> tuple[list[int], int, list[dict]]:
    """Solve signs s_i with y_i -> s_i y_{p(i)} preserving C_E6 exactly."""
    rows, rhs = [], []
    for support, coeff in sorted(E6.items()):
        target = tuple(sorted(p[i] for i in support))
        assert target in E6
        target_coeff = E6[target]
        mask = sum(1 << i for i in support)
        rows.append(mask)
        rhs.append(0 if coeff == target_coeff else 1)
    bits, rank = gf2_solve(rows, rhs, 27)
    signs = [-1 if b else 1 for b in bits]
    checks = []
    for support, coeff in sorted(E6.items()):
        target = tuple(sorted(p[i] for i in support))
        transported = coeff
        for i in support:
            transported *= signs[i]
        ok = transported == E6[target]
        assert ok
        checks.append({
            "source": list(support),
            "target": list(target),
            "sourceCoefficient": coeff,
            "transportedCoefficient": transported,
            "targetCoefficient": E6[target],
            "equal": ok,
        })
    return signs, rank, checks


def build() -> dict:
    base = build_base()
    group = build_group(base)
    assert len(group["gp"]) == len(group["DPp"]) == len(group["SpP"])
    assert len(group["gp"]) == 5

    psp36 = closure(group["DPp"], 36)
    assert len(psp36) == 25920
    orbit0 = {g[0] for g in psp36}
    assert len(orbit0) == 36
    stabilizer0 = sum(1 for g in psp36 if g[0] == 0)
    assert stabilizer0 == 720

    # D's exact all-36 theorem, rebuilt here rather than trusted as a label file.
    section_summary, section_detail = build_sections()
    assert section_summary["sections"] == 36
    assert all(r["signedRestrictionEqualsPfaffian"] for r in section_detail["records"])
    phi = {int(k): int(v) for k, v in section_detail["phiE6ToBaseG27"].items()}
    invphi = {v: k for k, v in phi.items()}
    assert len(phi) == len(invphi) == 27

    Ge = e6_graph()
    assert all(base["G27"].has_edge(phi[a], phi[b]) == Ge.has_edge(a, b)
               for a in range(27) for b in range(27))

    gen_records = []
    rank_counter = Counter()
    flip_counter = Counter()
    total_section_checks = 0
    total_intertwiner_checks = 0

    for gi, (g27, dp, sp) in enumerate(zip(group["gp"], group["DPp"], group["SpP"])):
        p = tuple(invphi[g27[phi[i]]] for i in range(27))
        assert sorted(p) == list(range(27))
        signs, rank, term_checks = signed_cubic_lift(p)
        assert rank == 21
        flips = sum(s < 0 for s in signs)
        rank_counter[rank] += 1
        flip_counter[flips] += 1

        section_checks = []
        for d in range(36):
            d2 = dp[d]
            source_base = set(range(27)) - set(base["DS"][d])
            target_base = set(range(27)) - set(base["DS"][d2])
            source_e6 = {invphi[v] for v in source_base}
            target_e6 = {invphi[v] for v in target_base}
            mapped = {p[i] for i in source_e6}
            support_ok = mapped == target_e6
            assert support_ok

            s0 = base["iso_ds_sp"][d]
            s1 = base["iso_ds_sp"][d2]
            spread_ok = sp[s0] == s1
            assert spread_ok
            # The exact graph intertwiner also means the source and target are
            # the same 36-object action, not two independently recognized copies.
            total_intertwiner_checks += 1
            total_section_checks += 1
            section_checks.append({
                "sourceDoubleSix": d,
                "targetDoubleSix": d2,
                "sourceSpread": s0,
                "targetSpread": s1,
                "spreadIntertwiner": True,
                "E6SectionSupportTransport": True,
                "sourcePfaffianExact": section_detail["records"][d]["signedRestrictionEqualsPfaffian"],
                "targetPfaffianExact": section_detail["records"][d2]["signedRestrictionEqualsPfaffian"],
            })

        gen_records.append({
            "generator": gi,
            "E6CoordinatePermutation": list(p),
            "negativeE6Coordinates": [i for i, s in enumerate(signs) if s < 0],
            "cubicSignEquationRank": rank,
            "cubicSignGaugeDimension": 27 - rank,
            "cubicTermsChecked": len(term_checks),
            "fullCartanCubicPreserved": all(x["equal"] for x in term_checks),
            "all36SectionSupportsTransported": all(x["E6SectionSupportTransport"] for x in section_checks),
            "all36SpreadDoubleSixIntertwiners": all(x["spreadIntertwiner"] for x in section_checks),
            "sectionChecks": section_checks,
        })

    # Directly verify the frozen double-six -> spread graph bijection.
    graph_intertwiner = all(
        base["iso_ds_sp"][dp[d]] == sp[base["iso_ds_sp"][d]]
        for dp, sp in zip(group["DPp"], group["SpP"])
        for d in range(36)
    )
    assert graph_intertwiner

    checks = {
        "PSp_action_on_36_has_order_25920": len(psp36) == 25920,
        "PSp_action_on_36_is_transitive": len(orbit0) == 36,
        "local_stabilizer_has_order_720": stabilizer0 == 720,
        "five_PSp_generators_used": len(gen_records) == 5,
        "all_five_generators_have_signed_E6_cubic_lifts": all(r["fullCartanCubicPreserved"] for r in gen_records),
        "all_cubic_lift_sign_systems_have_rank_21": rank_counter == Counter({21: 5}),
        "double_six_to_spread_map_intertwines_all_generators": graph_intertwiner,
        "all_180_generator_section_pairs_transport_supports": total_section_checks == 5 * 36 and all(r["all36SectionSupportsTransported"] for r in gen_records),
        "all_180_generator_spread_pairs_intertwine": total_intertwiner_checks == 5 * 36 and all(r["all36SpreadDoubleSixIntertwiners"] for r in gen_records),
        "all_36_source_and_target_sections_are_exact_pfaffians": all(r["signedRestrictionEqualsPfaffian"] for r in section_detail["records"]),
    }
    assert all(checks.values())

    return {
        "schema": "w33.psp36-spread-double-six-pfaffian-equivariance.v1",
        "status": "PASS",
        "checks": checks,
        "group": {
            "name": "PSp(4,3)",
            "order": 25920,
            "degree": 36,
            "transitive": True,
            "pointStabilizerOrder": 720,
            "localInterpretation": "720 = |S6|, the classical local relabeling symmetry of one double-six/doily/Pfaffian six-set",
        },
        "chain": "W33 spread <-> Schlaefli double-six -> 15-point doily complement -> signed Pfaffian section of C_E6",
        "doubleSixSpreadIntertwiner": {str(k): int(v) for k, v in base["iso_ds_sp"].items()},
        "cubicLiftSummary": {
            "generators": 5,
            "signEquationRankDistribution": {str(k): v for k, v in sorted(rank_counter.items())},
            "signGaugeDimension": 6,
            "negativeCoordinateCountDistribution": {str(k): v for k, v in sorted(flip_counter.items())},
            "generatorRecords": gen_records,
        },
        "sectionFamily": section_summary,
        "equivarianceStatement": "The same five PSp generators act on double-sixes and W33 spreads through an explicit intertwiner; after transport to the 27 Cartan coordinates each generator has a signed monomial lift preserving all 45 cubic coefficients and sends every Pfaffian-section support S_D to S_{gD}.",
        "gaugeBoundary": "The local 15-variable Pfaffian sign solutions have five free bits, and the 27-variable cubic lift has six sign-gauge bits. Equivariance is therefore asserted for the signed-section family/gauge orbit, not for an arbitrary free-bits-zero local orientation.",
        "theorem": "The 36 W33 spreads, 36 Schlaefli double-sixes, 36 doily complements and 36 exact Pfaffian sections form one PSp(4,3)-equivariant 36-object family. The local stabilizer is S6-sized (720), and the PSp generators lift to exact signed automorphisms of the full E6 Cartan cubic.",
        "boundary": "Exact finite group/cubic/incidence theorem. It does not identify gauge choices as observables or infer a physical symmetry implementation.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    out = build()
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "group": out["group"],
        "cubicLiftSummary": {k: v for k, v in out["cubicLiftSummary"].items() if k != "generatorRecords"},
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
