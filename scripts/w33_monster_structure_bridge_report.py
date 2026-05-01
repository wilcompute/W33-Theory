#!/usr/bin/env python3
"""Monster structure bridge report: (2X,3Y) selection -> cofactor actions -> stabilizers.

This is a deterministic, offline reporting script that ties together:
  - the Ogg-prime pipeline (Δ(2,3,p) support + mass / structure selection), and
  - the centralizer-cofactor recognition + permutation-degree hits.

The script also supports optional analysis of monomial "phase" lifts for a
handful of known permutation classes (e.g. 11A → 2·M12); additional factories
can be registered programmatically via :func:`register_monomial_factory`.
An optional CE2 anomaly search flags whether the global 2-cocycle gives a
nontrivial U/V result.

The goal is to make the *group-theoretic content* of the "structure-best" pair
explicit: when r_p := n/p lands in a cofactor permutation degree, we can read
off a stabilizer magnitude |K| = |H|/r_p (often recognizable by order).

Run:
  & .venv\\Scripts\\python.exe -X utf8 scripts\\w33_monster_structure_bridge_report.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
for p in (ROOT, SCRIPTS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def _find_perm_hit_for_pair(perm_hits: object, pair_x: str) -> dict[str, Any] | None:
    if not isinstance(perm_hits, list):
        return None
    for h in perm_hits:
        if not isinstance(h, dict):
            continue
        try:
            r = int(h.get("r", 0) or 0)
        except Exception:
            r = 0
        if r <= 1:
            continue
        if str(h.get("pair") or "").replace("×", "x") == str(pair_x):
            return dict(h)
    return None


from scripts.derive_m12_p144_suborbits import compose, inv, perm_from_cycles
from scripts.monomial_utils import find_sign_lifts_for_group, monomial_group_order

# monomial factory registry (filled ahead of any analysis)
# these generators are defined at module load time to make the registry
# available to external tests and helpers.
from tools.s12_universal_algebra import (
    enumerate_linear_code_f3,
    ternary_golay_generator_matrix,
)


def _factory_11A() -> list[tuple[int, ...]]:
    b11 = perm_from_cycles(12, [[1, 4], [3, 10], [5, 11], [6, 12]])
    b21 = perm_from_cycles(12, [[1, 8, 9], [2, 3, 4], [5, 12, 11], [6, 10, 7]])
    return [b11, b21]


def _factory_identity() -> list[tuple[int, ...]]:
    """Trivial identity generator set (useful for testing)."""
    return [tuple(range(12))]


_MONOMIAL_FACTORIES: dict[str, Any] = {
    "11A": _factory_11A,
    "identity": _factory_identity,
}


def register_monomial_factory(name: str, factory: Any) -> None:
    """Register a new monomial factory under the given class name.

    ``factory`` should be a zero‑argument callable returning a list of
    permutations (each a tuple of ints).  This allows external code or tests
    to add additional permutation sets without editing this module directly.
    """
    if not isinstance(name, str) or not name:
        raise ValueError("factory name must be a nonempty string")
    _MONOMIAL_FACTORIES[name] = factory


def unregister_monomial_factory(name: str) -> None:
    """Remove a previously registered monomial factory if present."""
    if not isinstance(name, str) or not name:
        raise ValueError("factory name must be a nonempty string")
    _MONOMIAL_FACTORIES.pop(name, None)


def get_monomial_factories() -> dict[str, Any]:
    """Return the current monomial factory registry (name -> factory).

    The returned dict is a shallow copy to discourage direct mutation.
    """
    return dict(_MONOMIAL_FACTORIES)


def analyze(*, max_q_exp: int = 3) -> dict[str, Any]:
    from scripts.w33_monster_ogg_pipeline import analyze as analyze_pipeline

    rep = analyze_pipeline(max_q_exp=int(max_q_exp))
    if rep.get("available") is not True:
        return {"available": False, "reason": rep.get("reason")}

    results = rep.get("results", [])
    if not isinstance(results, list):
        return {"available": False, "reason": "unexpected pipeline payload"}

    rows: list[dict[str, Any]] = []

    # generic Golay code data for monomial/phase-lift detection
    from tools.s12_universal_algebra import (
        enumerate_linear_code_f3,
        ternary_golay_generator_matrix,
    )

    gen = ternary_golay_generator_matrix()
    generator_rows = [tuple(int(x) % 3 for x in row) for row in gen]
    code_set = set(enumerate_linear_code_f3(gen))
    for rec in results:
        if not isinstance(rec, dict):
            continue
        p = int(rec.get("p", 0) or 0)
        best_mass = str(rec.get("best_pair") or "?")
        best_struct = rec.get("best_pair_by_structure")
        why = rec.get("best_pair_by_structure_reason")

        masses = rec.get("mass_by_pair", {})
        m_mass = (
            float(masses.get(best_mass, {}).get("float", 0.0) or 0.0)
            if isinstance(masses, dict)
            else 0.0
        )
        m_struct = (
            float(masses.get(str(best_struct), {}).get("float", 0.0) or 0.0)
            if isinstance(masses, dict) and isinstance(best_struct, str)
            else 0.0
        )

        per_class: list[dict[str, Any]] = []
        cof = rec.get("cofactor_perm_hits", {})
        if isinstance(cof, dict) and isinstance(best_struct, str):
            for cls_name, info in cof.items():
                if not isinstance(cls_name, str) or not isinstance(info, dict):
                    continue
                perm_hit = _find_perm_hit_for_pair(info.get("perm_hits"), best_struct)
                per_class.append(
                    {
                        "class_name": cls_name,
                        "cofactor_group": info.get("cofactor_group_recognized"),
                        "cofactor_order": info.get("cofactor_order"),
                        "perm_hit_for_structure_pair": perm_hit,
                    }
                )

        rows.append(
            {
                "p": p,
                "best_by_mass": best_mass,
                "best_by_structure": best_struct,
                "best_by_structure_reason": why,
                "mass_best": m_mass,
                "mass_structure": m_struct,
                "mass_ratio_best_over_structure": (
                    (m_mass / m_struct) if (m_mass > 0 and m_struct > 0) else None
                ),
                "classes": (
                    list(rec.get("classes", []))
                    if isinstance(rec.get("classes"), list)
                    else []
                ),
                "bridge": per_class,
            }
        )

    return {
        "available": True,
        "scan_primes": rep.get("scan_primes"),
        "replicability_max_q_exp": rep.get("replicability_max_q_exp"),
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-q-exp", type=int, default=3)
    parser.add_argument(
        "--include-monomial-lifts",
        action="store_true",
        help="Add slow, explicit monomial-lift checks (for each registered class) to the report.",
    )
    parser.add_argument(
        "--include-ce2",
        action="store_true",
        help="Also run a quick CE2 anomaly search and report whether any anomalies exist.",
    )
    parser.add_argument("--out-json", type=Path, default=None)
    args = parser.parse_args()

    rep = analyze(max_q_exp=int(args.max_q_exp))
    if rep.get("available") is not True:
        raise SystemExit(str(rep.get("reason") or "analysis unavailable"))

    lift_data: dict[str, dict[str, Any]] | None = None
    ce2_flag = bool(args.include_ce2)
    if bool(args.include_monomial_lifts) or ce2_flag:
        # compute monomial lift info for every registered factory
        from scripts.monomial_utils import (
            find_sign_lifts_for_group,
            monomial_group_order,
        )
        from tools.s12_universal_algebra import (
            enumerate_linear_code_f3,
            ternary_golay_generator_matrix,
        )

        # prepare Golay code data
        gen_mat = ternary_golay_generator_matrix()
        gen_rows = [tuple(int(x) % 3 for x in row) for row in gen_mat]
        code_set = set(enumerate_linear_code_f3(gen_mat))

        # optional CE2 anomaly detector
        def _check_ce2_anomaly() -> bool:
            from scripts.ce2_global_cocycle import predict_ce2_uv

            for a in [(i, j) for i in range(3) for j in range(3)]:
                for b in [(i, j) for i in range(3) for j in range(3)]:
                    for c in [(i, j) for i in range(3) for j in range(3)]:
                        try:
                            uv = predict_ce2_uv(a, b, c)
                        except ValueError as exc:
                            if "zero direction" in str(exc):
                                continue
                            raise
                        if uv is not None and (uv.U or uv.V):
                            return True
            return False

        ce2_anomaly = _check_ce2_anomaly() if ce2_flag else False
        lift_data = {}
        for cls_name, factory in _MONOMIAL_FACTORIES.items():
            perms = factory()
            lifts = find_sign_lifts_for_group(perms, gen_rows, code_set)
            info: dict[str, Any] = {"lift_exists": lifts is not None}
            if lifts is not None:
                order = monomial_group_order(list(zip(perms, lifts)))
                info["monomial_group_order"] = order
                info["ce2_anomaly"] = ce2_anomaly if order > 1 else False
            lift_data[cls_name] = info

    else:
        lift_data = None

    print("=" * 78)
    print(
        "MONSTER STRUCTURE BRIDGE: structure-best pair -> cofactor perm degree -> stabilizer"
    )
    print("=" * 78)
    print(f"Primes: {rep.get('scan_primes')}")
    print()

    rows = rep.get("rows", [])
    if not isinstance(rows, list):
        raise SystemExit("Unexpected report payload.")

    for row in rows:
        if not isinstance(row, dict):
            continue
        p = int(row.get("p", 0) or 0)
        mass = str(row.get("best_by_mass") or "?")
        struct = row.get("best_by_structure")
        why = row.get("best_by_structure_reason")
        r = row.get("mass_ratio_best_over_structure")
        tag = ""
        if isinstance(struct, str) and struct and struct != mass:
            # avoid non-ascii '≈' to keep output safe under default Windows encoding
            tag = (
                f"  (ratio best/structure ~ {float(r):.3g})"
                if isinstance(r, (int, float))
                else ""
            )
        print(f"p={p:2d}: mass={mass}  structure={struct} ({why}){tag}")

        bridge = row.get("bridge", [])
        if isinstance(bridge, list):
            for b in bridge:
                if not isinstance(b, dict):
                    continue
                cls = str(b.get("class_name") or "?")
                H = b.get("cofactor_group")
                hit = b.get("perm_hit_for_structure_pair")
                if not isinstance(hit, dict):
                    continue
                rr = int(hit.get("r", 0) or 0)
                stab = int(hit.get("stabilizer_order", 0) or 0)
                stab_grp = hit.get("stabilizer_group_recognized")
                line = f"      {cls}: H={H}  r={rr}  |K|={stab}"
                if isinstance(stab_grp, str) and stab_grp:
                    line += f" ({stab_grp})"
                # append monomial/CE2 info if we computed it
                if lift_data is not None and cls in lift_data:
                    info = lift_data[cls]
                    if info.get("lift_exists"):
                        order = info.get("monomial_group_order")
                        line += f"  [monomial order={order}]"
                        if ce2_flag:
                            line += f" (CE2? {bool(info.get('ce2_anomaly'))})"
                print(line)
        print()

    # print monomial lift summary if computed
    if lift_data is not None:
        print("=" * 60)
        print("MONOMIAL LIFT SUMMARY")
        print("=" * 60)
        for cls_name, info in lift_data.items():
            if not info.get("lift_exists"):
                print(f"{cls_name}: no sign lift found")
                continue
            order = info.get("monomial_group_order")
            ce2 = info.get("ce2_anomaly")
            line = f"{cls_name}: monomial group order = {order}"
            if ce2_flag:
                line += f"  (CE2 anomaly? {bool(ce2)})"
            print(line)
        print()

    if args.out_json is not None:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(rep, indent=2), encoding="utf-8")
        print(f"Wrote {args.out_json}")


if __name__ == "__main__":
    main()
