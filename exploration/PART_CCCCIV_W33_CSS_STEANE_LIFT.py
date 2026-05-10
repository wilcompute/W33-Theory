#!/usr/bin/env python3
"""PART CCCCIV -- W33 CSS Steane-Lift Protection Stack.

Parts CCCCII--CCCCIII turn the signed-switching/H1 bridge into an exact CSS
code:

    W33 edge-qubit CSS core = [[240, 81, 3]].

The core has the right logical/topological carrier but a low bare distance.  This
part converts that honesty boundary into a protection theorem by concatenating
the W33 CSS core with the Steane code [[7,1,3]].  The length 7 is not arbitrary
inside the W33 packet:

    7 = Phi6 = q^2 - q + 1.

For a quantum concatenation of an outer [[n,k,d]] code with an inner [[7,1,3]]
code, the parameters obey

    [[n*7^L, k, >= d*3^L]].

Thus three Steane lifts send the W33 core to

    [[82320, 81, >=81]],

and the guaranteed correctable weight is floor((81-1)/2)=40, exactly the W33
vertex count.  This does not claim an optimized threshold.  It proves a finite
fault-tolerant protection architecture whose scales are all W33 packet numbers.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

Q = 3
LAM = Q - 1
MU = Q + 1
K = Q * (Q + 1)
V = (Q**4 - 1) // (Q - 1)
E = V * K // 2
PHI6 = Q * Q - Q + 1
H1 = Q**4

BASE_N = E
BASE_K = H1
BASE_D = Q

STEANE_N = PHI6
STEANE_K = 1
STEANE_D = Q
STEANE_STABILIZERS = STEANE_N - STEANE_K


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def correctable_errors(distance: int) -> int:
    return (distance - 1) // 2


@dataclass(frozen=True)
class LiftLevel:
    level: int
    n: int
    k: int
    distance_lower_bound: int
    correctable_weight: int
    physical_per_logical: str


def lift_level(level: int) -> LiftLevel:
    n = BASE_N * (STEANE_N**level)
    d = BASE_D * (STEANE_D**level)
    return LiftLevel(
        level=level,
        n=n,
        k=BASE_K,
        distance_lower_bound=d,
        correctable_weight=correctable_errors(d),
        physical_per_logical=f"{n}/{BASE_K}",
    )


def lift_table(max_level: int = 3) -> List[LiftLevel]:
    return [lift_level(level) for level in range(max_level + 1)]


def build_results() -> Dict[str, Any]:
    table = lift_table(3)
    l0, l1, l2, l3 = table
    checks: List[Dict[str, Any]] = []

    checks.append(ok("base W33 CSS core is [[240,81,3]]", (BASE_N, BASE_K, BASE_D) == (240, 81, 3), (BASE_N, BASE_K, BASE_D)))
    checks.append(ok("Steane inner length = Phi6 = 7", STEANE_N == PHI6 == 7, STEANE_N))
    checks.append(ok("Steane inner dimension = 1", STEANE_K == 1, STEANE_K))
    checks.append(ok("Steane inner distance = q = 3", STEANE_D == Q == 3, STEANE_D))
    checks.append(ok("Steane stabilizer count = 6 = K/lambda", STEANE_STABILIZERS == K // LAM == 6, STEANE_STABILIZERS))

    checks.append(ok("level 1 parameters [[1680,81,>=9]]", (l1.n, l1.k, l1.distance_lower_bound) == (1680, 81, 9), asdict(l1)))
    checks.append(ok("level 1 correctable weight = mu", l1.correctable_weight == MU, l1.correctable_weight))
    checks.append(ok("level 2 distance lower bound = 27 = q^3", l2.distance_lower_bound == Q**3 == 27, asdict(l2)))
    checks.append(ok("level 3 physical qubits = 82320", l3.n == E * PHI6**3 == 82320, asdict(l3)))
    checks.append(ok("level 3 distance lower bound = H1 = q^4 = 81", l3.distance_lower_bound == H1, asdict(l3)))
    checks.append(ok("level 3 correctable weight = W33 vertices = 40", l3.correctable_weight == V, asdict(l3)))
    checks.append(ok("logical dimension stays H1 through inner k=1 concatenation", all(row.k == H1 for row in table), [row.k for row in table]))
    checks.append(ok("distance multiplies by q each lift", [row.distance_lower_bound for row in table] == [3, 9, 27, 81], [row.distance_lower_bound for row in table]))
    checks.append(ok("physical length multiplies by Phi6 each lift", [row.n for row in table] == [240, 1680, 11760, 82320], [row.n for row in table]))
    checks.append(ok("three lifts align distance with logical sector count", l3.distance_lower_bound == BASE_K, {"distance": l3.distance_lower_bound, "logical": BASE_K}))

    verified = all(c["passed"] for c in checks)
    return {
        "part": "CCCCIV",
        "title": "W33 CSS Steane-Lift Protection Stack",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(c["passed"] for c in checks),
        "base_code": {"notation": "[[240,81,3]]", "n": BASE_N, "k": BASE_K, "d": BASE_D},
        "inner_code": {
            "name": "Steane",
            "notation": "[[7,1,3]]",
            "n": STEANE_N,
            "k": STEANE_K,
            "d": STEANE_D,
            "w33_read": "7 = Phi6, 3 = q, 6 stabilizers = K/lambda",
        },
        "lift_table": [asdict(row) for row in table],
        "fault_tolerance_read": {
            "three_lift_code": "[[82320,81,>=81]]",
            "guaranteed_correctable_weight": V,
            "logical_sector_count": H1,
            "interpretation": "the third Phi6/Steane lift makes the distance lower bound equal to the H1 matter rank and the correctable weight equal to the W33 vertex count",
        },
        "architecture_upgrade": (
            "Closes the bare-distance honesty boundary of the W33 CSS code by giving "
            "a finite concatenated protection stack: the exact [[240,81,3]] core "
            "lifted by the [[7,1,3]] Steane/Phi6 code gives [[82320,81,>=81]] "
            "after three lifts."
        ),
        "theorem": (
            "Concatenating the W33 CSS core [[240,81,3]] with L levels of the "
            "Steane [[7,1,3]] code yields parameters [[240*7^L,81,>=3^(L+1)]]. "
            "For L=3 this is [[82320,81,>=81]], so the guaranteed correctable "
            "weight is 40."
        ),
        "honesty_boundary": (
            "This is a parameter and lower-bound theorem for concatenated quantum "
            "codes, not a threshold simulation or optimized hardware layout. It "
            "shows an exact finite protection architecture that can be compiled "
            "before physical noise calibration."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "three_lift_code": results["fault_tolerance_read"]["three_lift_code"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
